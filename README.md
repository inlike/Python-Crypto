# Python-Crypto
记录平时做js加密解密算法
---
## 新浪微博登陆
  测试的是手机号可以正常登陆，还没遇到验证码问题，后面遇上再加<br>
  post请求之后会被<B>重定向两次</B>才能得到登陆用户信息，发送post请求后还需要正则匹配两次重定向url<br>
  注意请求返回的编码格式post请求后返回编码是<B>GBK</B>，后面还会返回GB2312
  ### 加密方式：RSA(非对称加密方式)
    登录前先get请求返回携带有token、pubkey、raskv、servertime等信息的dict字符串，包含在js中需要提取转换
    需要破解的参数是su和sp,sp是密码<br>
    su:是通过封装了RSA源码的一个对象sinaSSOEncoder的base64编码用户名得到的<br>
    sp:加密的密码,通过创建sinaSSOEncoder加密对象，公钥是上面返回的pubkey，偏移量"10001"
    加密内容是servertime + "\t" + nonce + "\n" + pw
    servertime：上面get请求返回的
    nonce：上面get请求返回的
    pw：输入的密码
## 腾讯企鹅媒体
  测试的是邮箱登陆，无验证码问题，因为账号问题可能在登陆后被重定向到身份验证页面
  注意在post请求时需要带上cookie，并且cookie中有个参数是登录前Ajax get请求的含有token信息的返回cookie
  ### 加密方式：MD5双重加密（信息摘要算法或签名算法）
    登录前后台会get请求一次，返回含有token和salf等加密参数信息以及一个cookie，该cookie要加在post的请求中
    加密形式：MD5(token + MD5(salt + pwd))双重加密
## 网易云获取评论请求参数加密
   测试是无登陆状态下的请求加密，无登陆状态下csrf_token参数为空，在同一ip过度请求下降不会返回数据；在登陆状态下请求的url和未登录状态下的url是不一样的
   ### 加密方式AES+RSA
      评论请求加密参数是两个：params、encSecKey，传入加密函数的参数是a,b,c,d+内部随机生成的16位参数i
      其中a='"{"rid":"R_SO_4_371362","offset":"160","total":"false","limit":"20","csrf_token":"de097d5986487c4aefe9f52c65e43224"}"}'形式参数
      rid：歌曲id；
      offset：歌词页数计算公式(n-1)*20；
      total：在第一页是TRUE在其他是false；
      csrf_token：在登陆成功后再返回的cookie中可以找到，未登录时是空。
      b、c、d是固定的参数，由js内部定义的文字编码转码并并且得到的类似于
      {"色":"00e0b","流感":"509f6","这边":"259df","弱":"8642d","嘴    唇":"bc356","亲":"62901","开心":"477df"}-->色+嘴唇="00e0bbc356"
      bcd当做固定参数传入
      其中内部随便变量i可以写死，那么encSecKey参数都是由固定参数生成的，可以当做固定参数使用
      params根据页数和歌曲参数的不同是变化的
      params:是内部方法AES CBC模式
      encSecKey：RSA加密
## 微信公众号密码加密
  只分析了微信公众号登陆请求的post密码加密
  ### 加密方式MD5
      加密方式比较简单，取密码的前16位进行MD5加密
      
    

