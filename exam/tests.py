from exam.langconv import *
import sys

print(sys.version)
print(sys.version_info)

# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line

# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line

line_chs='<>123asdasd把中文字符串进行繁体和简体中文的转换'
line_cht='憂慮'

ret_chs = "%s\n"%cht_to_chs(line_cht)
ret_cht = "%s\n"%chs_to_cht(line_chs)

print("chs='%s'",ret_chs)
print("cht='%s'",ret_cht)