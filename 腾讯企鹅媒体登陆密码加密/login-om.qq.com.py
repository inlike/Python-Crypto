
import requests
from json import loads
import execjs
from urllib import parse


def get_token(email):
    email = parse.quote(email)
    token_url = 'https://om.qq.com/userAuth/randomCode?email={}&relogin=1'.format(email)
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "RK=9XA4Hchh7C; ptcz=af27247c2cc54de7b15f949e041525c62102f66aae856e17adac1a7a41f93e21;"
                  " cuid=2366632689; pgv_pvid=8300690180; pgv_pvi=5655952384; o_cookie=2551513277; "
                  "tvfe_boss_uuid=3af2d5ef04df785f; ts_uid=1842616160; pt2gguin=o2551513277; "
                  "ts_refer=www.baidu.com/link; fname=%E5%96%9C%E4%B9%90%E8%A7%81%E9%97%BB; "
                  "fimgurl=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_ls%2F0%2F655036856_200200%2F0; "
                  "uin=o2551513277; ptisp=cm; pgv_si=s3134537728; TSID=ofu1fo74v126dtfhgtellnpb23; "
                  "pgv_info=ssid=s8282530815; skey=@j0RBeBv05; ts_last=om.qq.com/userAuth/index",
        "referer": "https://om.qq.com/userAuth/index",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2767.400",
        "x-requested-with": "XMLHttpRequest"
    }

    tocker_data = requests.get(token_url, headers=headers)
    if tocker_data.status_code == 200:
        token = loads(tocker_data.text)
        return (token['data'], tocker_data.cookies['randomkey'])
    else:
        return False


def login(email, pwd):
    login_url = 'https://om.qq.com/userAuth/SignIn?relogin=1'
    token, randomkey = get_token(email)
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-length": "109",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "RK=9XA4Hchh7C; ptcz=af27247c2cc54de7b15f949e041525c62102f66aae856e17adac1a7a41f93e21; "
                  "cuid=2366632689; pgv_pvid=8300690180; pgv_pvi=5655952384; o_cookie=2551513277; "
                  "tvfe_boss_uuid=3af2d5ef04df785f; ts_uid=1842616160; pt2gguin=o2551513277; "
                  "ts_refer=www.baidu.com/link; fname=%E5%96%9C%E4%B9%90%E8%A7%81%E9%97%BB; "
                  "fimgurl=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_ls%2F0%2F655036856_200200%2F0; "
                  "uin=o2551513277; ptisp=cm; pgv_si=s3134537728; TSID=ofu1fo74v126dtfhgtellnpb23; "
                  "pgv_info=ssid=s8282530815; skey=@j0RBeBv05; ts_last=om.qq.com/userAuth/index; "
                  "randomkey={}".format(randomkey),
        "origin": "https://om.qq.com",
        "referer": "https://om.qq.com/userAuth/index",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2767.400",
        "x-requested-with": "XMLHttpRequest"
    }

    with open("./js.txt", 'r', encoding='utf-8') as f:  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
    jsstr = htmlstr
    ctx = execjs.compile(jsstr)   # 加载JS文件
    pwd = ctx.call("getpwd", pwd, token['token'], token['salt'])
    loginresponse = requests.post(login_url, data={'email': email, 'pwd': pwd, 'token': token['token']}, headers=headers)
    data = loads(loginresponse.text)




