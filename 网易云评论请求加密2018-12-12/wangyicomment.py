# -*- coding:utf-8 -*-
import execjs

with open("./js.txt", 'r', encoding='utf-8') as f:  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
jsstr = htmlstr
ctx = execjs.compile(jsstr)  # 加载JS文件
a = '"{"rid":"R_SO_4_371362","offset":"160","total":"false","limit":"20",' \
    '"csrf_token":"de097d5986487c4aefe9f52c65e43224"}"}'
b = "010001"
c = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17" \
    "a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114" \
    "af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5" \
    "2741d546b8e289dc6935b3ece0462db0a22b8e7"
d = "0CoJUm6Qyw8W8jud"
sp = ctx.call(
        "getdata", a, b, c, d)


