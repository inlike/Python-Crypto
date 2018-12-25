# -*- coding：utf-8 -*-
import base64

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


if __name__ == '__main__':
    aes_test = USE_AES("assssssssdfasasasasa")
    a = aes_test.encrypt("测试")
    b = aes_test.decodebytes(a)


import hashlib


def hash_demo():
    m = hashlib.md5()
    m.update(b"hello")
    m.update(b"world!")  # = hello + world!

    hash_hex = hashlib.sha3_512(b"luzhuo.me").hexdigest()

    print(m.digest_size)
    print(m.digest())  # 二进制hash
    print(m.hexdigest())  # 十六进制hash
    print(hash_hex)

    # 加盐加密
    hash_bytes = hashlib.pbkdf2_hmac('sha256', b'luzhuo.me', b'80', 100000)
    print(hash_bytes)


def hash_func():
    # hashlib.new(name[, data])  // 创建hashlib(非首选), name=算法名, data:数据
    hash = hashlib.new('ripemd160', b'luzhuo.me')

    # 常量
    dics = hashlib.algorithms_guaranteed  # 所有平台支持的hash算法的名称
    dics = hashlib.algorithms_available  # 在Python解析器中可用的hash算法的名称, 传递给new()时, 可识别

    # hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None) // 加盐加密 hash_name:hash名称, password:数据, salt:盐, iterations:循环次数, dklen:密钥长度
    hash_bytes = hashlib.pbkdf2_hmac('sha256', b'luzhuo.me', b'80', 100000)

    # hash对象
    num = hash.digest_size  # hash结果的大小
    num = hash.block_size  # hash算法的内部块的大小
    strs = hash.name  # hash名称, 可传给new()使用
    hash.update(b"data")  # 字节缓冲区 hash.update(a) hash.update(b) == hash.update(a+b)
    hash_bytes = hash.digest()  # 字节hash
    hash_str = hash.hexdigest()  # 16进制字符串hash
    hash = hash.copy()  # 拷贝hash对象副本


import hmac


def hmac_demo():
    # 加密
    h = hmac.new(b"net")
    h.update(b"luzhuo.me")
    h_str = h.hexdigest()
    print(h_str)

    # 比较密码
    boolean = hmac.compare_digest(h_str, hmac.new(b"net", b"luzhuo.me").hexdigest())
    print(boolean)



def hmac_func():
    # 创建key和内容,再都进行加密
    # hmac.new(key, msg=None, digestmod=None) // 创建新的hmac对象, key:键, msg:update(msg), digestmod:hash名称(同hashlib.new())(默认md5)
    hc = hmac.new(b"key")

    # hmac对象
    hc.update(b"msg")  # 字节缓冲区  hc.update(a) hc.update(b) == hc.update(a+b)
    hash_bytes = hc.digest()  # 字节hash
    hash_str = hc.hexdigest()  # 16进制hash字符串
    hc = hc.copy()  # 拷贝hmac副本
    num = hc.digest_size  # hash大小
    num = hc.block_size  # hash算法内部块大小
    strs = hc.name  # hash名称
    # hmac.compare_digest(a, b) // 比较两个hash密钥是否相同, 参数可为: str / bytes-like object, (注:建议使用,不建议使用a==b)
    boolean = hmac.compare_digest(hmac.new(b"net", b"luzhuo.me").digest(), hmac.new(b"net", b"luzhuo.me").digest())