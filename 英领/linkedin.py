# --*- coding：utf-8 -*-

import requests
from lxml import etree

session = requests.Session()

def login(name, password):
    session.headers= {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                         }
    url = 'https://www.linkedin.com/'
    page = session.get(url)
    rp = etree.HTML(page.text)
    csrfToken = rp.xpath()