# --*- coding：utf-8 -*-

import requests
from lxml import etree

session = requests.Session()


def login(name, password):
    session.headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                      }
    url = 'https://www.linkedin.com/'
    login_url = 'https://www.linkedin.com/uas/login-submit?' \
                'loginSubmitSource=GUEST_HOME'
    page = session.get(url)
    rp = etree.HTML(page.text)
    loginCsrfParam = rp.xpath('//*[@name="loginCsrfParam"]/@value')[0]

    form_data = {
        'session_key': name,
        'session_password': password,
        'loginCsrfParam': loginCsrfParam,
        'isJsEnabled': 'false'
    }
    page_login = session.post(login_url, data=form_data
    )

    login_rp = etree.HTML(page_login.text)
    verify_url = 'https://www.linkedin.com/checkpoint/challenge/verify'
    csrfToken = login_rp.xpath('//*[@name="csrfToken"]/@value')[0]
    pageInstance = login_rp.xpath('//*[@name="pageInstance"]/@value')[0]
    resendUrl = login_rp.xpath('//*[@name="resendUrl"]/@value')[0]
    challengeId = login_rp.xpath('//*[@name="challengeId"]/@value')[0]
    language = 'zh-CN'
    displayTime = login_rp.xpath('//*[@name="displayTime"]/@value')[0]
    challengeSource = login_rp.xpath('//*[@name="challengeSource"]/@value')[0]
    requestSubmissionId = login_rp.xpath('//*[@name="requestSubmissionId"]/@value')[0]
    challengeType = login_rp.xpath('//*[@name="challengeType"]/@value')[0]
    challengeData = login_rp.xpath('//*[@name="challengeData"]/@value')[0]
    failureRedirectUri = login_rp.xpath('//*[@name="failureRedirectUri"]/@value')[0]
    pin = input('请输入验证码')
    verify_data = {
        'csrfToken': csrfToken,
        'pageInstance': pageInstance,
        'resendUrl': resendUrl,
        'challengeId': challengeId,
        'language': language,
        'displayTime': displayTime,
        'challengeSource': challengeSource,
        'requestSubmissionId': requestSubmissionId,
        'challengeType': challengeType,
        'challengeData': challengeData,
        'failureRedirectUri': failureRedirectUri,
        'pin': pin,
        }
    verify_post = session.post(verify_url, data=verify_data)


if __name__ == '__main__':
    login('2551513277@qq.com', 'sdsdsdsd')