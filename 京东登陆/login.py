import requests
import execjs
from lxml import etree

URL = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue%26utm_source%3Dbaidu" \
      "-pinzhuan%26utm_medium%3Dcpc%26utm_campaign%3Dt_288551095_baidupinzhuan%26utm_term%3D0f3d30c8dba7459bb52f2eb5eb" \
      "a8ac7d_0_b4ece126b50f487280968f8ddba60aa8"

session = requests.Session()
with open("./js.txt", 'r', encoding='utf-8') as f:  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
jsstr = htmlstr
ctx = execjs.compile(jsstr)  # 加载JS文件


def getform(phone, pwd):
    response = session.get(URL)
    rp = etree.HTML(response.text)
    sa_token = rp.xpath('//input[@id="sa_token"]/@value')[0]
    uuid = rp.xpath('//input[@id="uuid"]/@value')[0]
    eid = rp.xpath('//input[@id="eid"]/@value')[0]
    sessionId = rp.xpath('//input[@id="sessionId"]/@value')[0]
    token = rp.xpath('//input[@id="token"]/@value')[0]
    loginType = rp.xpath('//input[@id="loginType"]/@value')[0]
    pubKey = rp.xpath('//input[@id="pubKey"]/@value')[0]
    slideAppId = rp.xpath('//input[@id="slideAppId"]/@value')[0]
    useSlideAuthCode = rp.xpath('//input[@id="useSlideAuthCode"]/@value')[0]
    loginname = phone
    pwd = ctx.call("getEntryptPwd", pubKey, pwd)
    seqSid = "271726271731661547"
    authcode = None     # 服务器返回的时间戳,还需单独请求
    data = {
        "uuid": uuid,
        "eid": eid,
        "fp": sessionId,
        "_t": token,
        "loginType": loginType,
        "loginname": loginname,
        "nloginpwd": pwd,
        "authcode": authcode,
        "pubKey": pubKey,
        "sa_token": sa_token,
        "seqSid": seqSid,
        "useSlideAuthCode": useSlideAuthCode
    }
    return data


if __name__ == '__main__':
    getform(18328496803, 666666)