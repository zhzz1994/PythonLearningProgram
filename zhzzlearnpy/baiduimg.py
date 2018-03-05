from aip import AipFace
import os
import io


APP_ID = 'f28be295cced4fb59bc2c0954b7530a5 '
API_KEY = '014caeebc5704738ad108aec0f80990c'
SECRET_KEY = '3258586a65904692abd35106d8c2bc23'

filePath = 'g:\\pic1.jpg'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

options = {
    'max_face_num': 1,
    'face_fields': "age,beauty,expression,faceshape",
}

result = aipFace.detect(get_file_content('g:\thepic.jpg'), options)
