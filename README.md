# Python-Crypto
记录平时做js加密解密算法
---
## 新浪微博登陆
  测试的是手机号可以正常登陆，还没遇到验证码问题，后面遇上再加<br>
  post请求之后会被<B>重定向两次</B>才能得到登陆用户信息，发送post请求后还需要正则匹配两次重定向url<br>
  注意请求返回的编码格式post请求后返回编码是<B>GBK</B>，后面还会返回GB2312
  ### 新浪微博的密码加密方式：RSA(非对称加密方式)
    登录前先get请求返回携带有token、pubkey、raskv、servertime等信息的dict字符串，包含在js中需要提取转换
    需要破解的参数是su和sp,sp是密码<br>
    su:是通过封装了RSA源码的一个对象sinaSSOEncoder的base64编码用户名得到的<br>
    sp:加密的密码,通过创建sinaSSOEncoder加密对象，公钥是上面返回的pubkey，偏移量"10001"
    加密内容是servertime + "\t" + nonce + "\n" + pw
    servertime：上面get请求返回的
    nonce：上面get请求返回的
    pw：输入的密码
    

