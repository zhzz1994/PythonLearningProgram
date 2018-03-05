from langconv import *

def simple2tradition(line):
    #将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line

def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line

line = '是不是后面的5'
line = line.encode('utf-8')
print(tradition2simple(line).decode('utf-8'))

print(simple2tradition(line).decode('utf-8'))