from main import bot, dp
from aiogram.utils.exceptions import BotBlocked
from os import listdir
from aiogram.types import Message
from aiogram import types
from config import ADMIN_ID, INFO
from db import BotDB
from bot_action import docx2pdf_con
from os import mkdir

bd = BotDB('users_data.sqlite')



async def send_to_admin(dp):
    try:
        await bot.send_message(chat_id=ADMIN_ID, text='MFA: ' + 'Бот запущен')
    except BotBlocked:
        print('Адмен блокенул')

@dp.message_handler(commands = ['start'])
async def start(message: Message):
    print('123')
 
    if not bd.user_exists(message.from_user.id,):
        bd.add_user(message.from_user.id, message.from_user.username)
        if message.from_user.id != int(ADMIN_ID):
            await bot.send_message(chat_id=ADMIN_ID, text='MFA: Новый пользователь добавлен в базу данных. \n<i>user id:</i> ' + str(message.from_user.id) + ', <i> username: </i>' + str(message.from_user.username))

        await message.bot.send_message(message.from_user.id, "Добро пожаловать.")
    await message.bot.send_message(message.from_user.id, "Вы не новый пользователь. Чтобы узнать команды и информацию напишите /info.")


@dp.message_handler(commands=["test1"])
async def cmd_test1(message: Message):
    await message.reply("Test 1")

@dp.message_handler(commands=["info"])
async def info(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text= INFO)

@dp.message_handler(commands=["balance"])
async def info(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text= 'В разработке.')

@dp.message_handler(commands=["usage"])
async def info(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text= 'В разработке.')

@dp.message_handler(content_types=['document'])
async def get_file(message: Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = message.document.file_name
    print(file_name)

    if file_name[-4:] == '.pdf':
        try:
            mkdir('dwl_files/' + str(message.from_user.id))
        except:
            print('Папка уже есть')
        await bot.send_message(chat_id=message.from_user.id, text='Ждите')
        await bot.download_file(file_path, 'dwl_files/' + str(message.from_user.id) + '/' + file_name[:-4] + '.pdf')
        print('файл сохранёнен')
        if docx2pdf_con(file_name[:-4] + '.pdf', message.from_user.id) == 2:
            print('конвертация успешна')
            await bot.send_document(message.from_user.id, open('dwl_files/' + str(message.from_user.id) + '/' + file_name[:-4] + '.docx', 'rb'))

            if message.from_user.id != int(ADMIN_ID):
                await bot.send_message(chat_id=ADMIN_ID, text='MFA:\n<i>user id:</i> ' + str(message.from_user.id) + '<i>username:</i> ' + message.from_user.username + ' <i>Отправил файл:</i>' + file_name)
        
    elif file_name[-5:] == '.docx':
        try:
            mkdir('dwl_files/' + str(message.from_user.id))
        except:
            print('Папка уже есть')
        await bot.send_message(chat_id=message.from_user.id, text='Ждите')
        await bot.download_file(file_path, 'dwl_files/' + str(message.from_user.id) + '/'  + file_name[:-5] + '.docx')
        print('файл сохранёнен')
        if docx2pdf_con(file_name[:-5] + '.docx', message.from_user.id) == 1:
            print('конвертация успешна')
            await bot.send_document(message.from_user.id, open('dwl_files/' + str(message.from_user.id) + '/' + file_name[:-5] + '.pdf', 'rb'))

            if message.from_user.id != int(ADMIN_ID):
                await bot.send_message(chat_id=ADMIN_ID, text='MFA:\n<i>user id:</i> ' + str(message.from_user.id) + '<i>username:</i> ' + message.from_user.username + ' <i>Отправил файл:</i>' + file_name)
    else: 
        await bot.send_message(chat_id=message.from_user.id, text='Бот принимает файлы .pdf или .docx до 20 мб.')


@dp.message_handler()
async def echo(message: Message):
    text = f'Привет, чтобы узнать команды напиши /info'
    user_id = message.from_user.id
    await bot.send_message(chat_id=message.from_user.id, text=text)

    if message.from_user.id != int(ADMIN_ID):
        await bot.send_message(chat_id=ADMIN_ID, text='MFA: <i>username:</i> ' + str(message.from_user.username) + ', <i>user first name:</i> ' + str(message.from_user.first_name) + ',<i> message:</i> ' + message.text)
