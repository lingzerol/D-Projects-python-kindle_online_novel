from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

import base64
import datetime
import random
import time
from multiprocessing.dummy import threading

_RANDOMSTR_LENGTH = 64


def encrypt(text):
    with open('./config/public_key.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        crypt_text = base64.b64encode(cipher.encrypt(text.encode()))
    return str(crypt_text, "utf-8")


def decrypt(crypt_text):
    random_generator = Random.new().read
    with open('./config/private_key.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(crypt_text), random_generator)
    return str(text, "utf-8")


def create_cookie(info={}):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for _ in range(_RANDOMSTR_LENGTH):
        random_str += base_str[random.randint(0, length)]
    cookie = "{0:%Y%m%d%H%M%S%f}".format(datetime.datetime.now())+random_str
    return cookie

class CookiePool:

    def __init__(self, pool_size=50, max_period=3600):
        self.pool = {}
        self.pool_size = pool_size
        self.max_period = max_period
        self.lock = threading.RLock()
        check_t = threading.Thread(target=self.__inner_check, args=[])
        check_t.start()
        # check_t.join()
    
    def __inner_check(self):
        self.lock.acquire()
        try:
            for key in self.pool:
                if time.time() - self.pool[key] >= self.max_period:
                    del self.pool[key]
        finally:
            self.lock.release()
        time.sleep(self.max_period)

    def add(self, cookie):
        self.lock.acquire()
        try:
            if len(self.pool) < self.pool_size:
                self.pool[cookie] = time.time()
            else:
                if cookie not in self.pool:
                    oldest = None
                    for key in self.pool:
                        if oldest is None or self.pool[oldest] > self.pool[key]:
                            oldest = key
                    if oldest is not None:
                        del self.pool[oldest]
                self.pool[cookie] = time.time()
        finally:
            self.lock.release()

    def update(self, cookie):
        self.add(cookie)
        
    def check(self, cookie):
        self.lock.acquire()
        flag = False
        try:
            if cookie in self.pool:
                flag = True
        finally:
            self.lock.release()
        return flag
