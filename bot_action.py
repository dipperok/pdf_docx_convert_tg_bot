from docx2pdf import convert
from pdf2docx import parse
import os

def docx2pdf_con(file_name, user_id):
    path = 'dwl_files/' + str(user_id) + '/' + file_name
    if path[-5:] == ".docx":
        convert(path)
        return 1
    elif path[-4:] == ".pdf":
        temp_pdf = file_name[:-4]
        pdf_file = path
        word_file = "dwl_files/" + str(user_id) + '/' + temp_pdf + ".docx"
        parse(pdf_file, word_file, start=0, end=None)
        return 2
    else:
        return 0