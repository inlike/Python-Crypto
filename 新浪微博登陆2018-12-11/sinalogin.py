# -*- coding:utf-8 -*-

import requests
from json import loads
import re
import execjs
from urllib import parse

with open("./js.txt", 'r', encoding='utf-8') as f:  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
jsstr = htmlstr
ctx = execjs.compile(jsstr)  # 加载JS文件


def getsu(iphone):
    """
    获取加密参数su
    :param iphone: 传入手机号
    :return:
    """
    iphone = parse.quote(iphone)
    su = ctx.call("getsu", iphone)
    return su


def getkey(iphone):
    """
    获取加密需要的时间戳、公钥等信息
    :param iphone:
    :return: json
    """
    su = getsu(iphone)
    su_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=" \
             "sinaSSOController.preloginCallBack&su={}%3D&rsakt" \
             "=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1544491300471".format(su)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "SINAGLOBAL=10.71.2.96_1537319283.25360; "
                  "UOR=www.baidu.com,news.sina.com.cn,; "
                  "SUB=_2AkMs_o_Sf8NxqwJRmfkVzWnma49-zgDEieKaon4JJRMyHR"
                  "l-yD9kql4ttRB6B36hPXoG3Dc1joQANXyggWcwbJoRDfhG; "
                  "SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhAxrOYgrYDalY30D0XuRdP;"
                  " ULV=1541659821773:4:1:1::1540805170207; "
                  "UM_distinctid=166f21629624c-036b343a4703ce-335e4b78-1fa400-166f216296327a; "
                  "lxlrttp=1541383354; U_TRS1=00000057.2c29756.5c0601f9.ec750a9c;"
                  " Apache=172.16.138.142_1544490894.221870",
        "Host": "login.sina.com.cn",
        "Referer": "https://www.weibo.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 "
                      "Core/1.63.5603.400 QQBrowser/10.1.1775.400"
    }
    jsdata = requests.get(su_url, headers=headers)
    data = re.search('{.+}', jsdata.text).group()
    keys = loads(data)
    keys['su'] = su
    return keys


def login(iphone, password):
    """
    登陆程序
    :param iphone:
    :param password:
    :return: 登陆成功则返回用户信息json格式
    """
    keys = getkey(iphone)
    sp = ctx.call(
        "getsp", keys['pubkey'], keys['servertime'], keys['nonce'], password)
    data = {
        "entry": "weibo",
        "gateway": "1",
        "from": "",
        "savestate": "7",
        "qrcode_flag": "false",
        "useticket": "1",
        "pagerefer": "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r"
                     "=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        "vsnf": "1",
        "su": keys['su'],
        "service": "miniblog",
        "servertime": keys['servertime'],
        "nonce": keys['nonce'],
        "pwencode": "rsa2",
        "rsakv": keys['rsakv'],
        "sp": sp,
        "sr": "1920*1080",
        "encoding": "UTF-8",
        "prelt": "44",
        "url": "https://www.weibo.com/ajaxlogin.php?framelogin=1&callback"
               "=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META"
    }

    log = requests.Session()
    log_url = 'https://login.sina.com.cn/sso/' \
              'login.php?client=ssologin.js(v1.4.19)'
    page = log.post(log_url, data=data)
    """被重定向两次"""
    page.encoding = "GBK"
    url = re.search('replace\([\'"](.*?)[\'"]\)', page.text).group(1)
    page = log.post(url, data=data)
    page.encoding = "GBK"
    url = re.search('replace\([\'"](.*?)[\'"]\)', page.text).group(1)
    page = log.post(url, data=data)
    user_info = re.search('{.+}', page.text).group()
    user_info_json = loads(user_info)
    return user_info_json


if __name__ == '__main__':
    login('1832*****03', '666666')