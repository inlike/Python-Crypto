# -*- coding:utf-8 -*-

import requests
import execjs


with open("./js.txt", 'r', encoding='utf-8') as f:  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
jsstr = htmlstr
ctx = execjs.compile(jsstr)  # 加载JS文件


def getpwd(pwd):
    password = ctx.call("getpwd", pwd)
    return password


def login(email, pwd):
    session = requests.Session()
    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
    password = getpwd(pwd)
    data = {
        "username": email,
        "pwd": password,
        "imgcode": "",
        "f": "json",
        "userlang": "zh_CN",
        "redirect_url": "",
        "token": "",
        "lang": "zh_CN",
        "ajax": "1"
    }
    rp = session.post(url, data=data)


if __name__ == '__main__':
    login("2551513277@qq.com", "666666")


