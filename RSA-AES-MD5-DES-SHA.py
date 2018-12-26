# -*- coding：utf-8 -*-
import base64
import rsa
from Crypto.Cipher import AES


class USE_AES:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    def to_16(self, key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB) # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))), encoding='utf8').replace('\n', '')  # 加密

    def decodebytes(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密


class USE_RSA:
    """
    生成密钥可保存.pem格式文件
    1024位的证书，加密时最大支持117个字节，解密时为128；
    2048位的证书，加密时最大支持245个字节，解密时为256。
    https://blog.csdn.net/MTbaby/article/details/80453687
    """
    def __init__(self, number=1024):
        self.pubkey, self.privkey = rsa.newkeys(number)

    def rsaEncrypt(self, text):
        """

        :param test: str
        :return: bytes
        """
        content = text.encode('utf-8')
        crypto = rsa.encrypt(content, self.pubkey)
        return crypto
    
    def rsaDecrypt(self, text):
        """
        
        :param text:bytes 
        :return: str
        """
        content = rsa.decrypt(text, self.privkey)
        con = content.decode('utf-8')
        return con
        
    def savePem(self, path_name, text):
        if "PEM" in path_name.upper():
            path_name = path_name[:-4]
        with open('{}.pem'.format(path_name), 'w') as f:
            f.write(text)


if __name__ == '__main__':
    # aes_test = USE_AES("assssssssdfasasasasa")
    # a = aes_test.encrypt("测试")
    # b = aes_test.decodebytes(a)
    rsa_test = USE_RSA()
    a = rsa_test.rsaEncrypt("测试加密")
    b = rsa_test.rsaDecrypt(a)