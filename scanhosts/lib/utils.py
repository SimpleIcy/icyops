# -*- coding:utf-8 -*-

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import re

def mac_trans(mac):
    '''
    trans the mac addr
    :param mac:
    :return:
    '''
    if mac:
        mac_lst = mac.split("\n")
        mac_res = [item.replace(":", '').replace("000000000000", '').replace("00000000", '') for item in mac_lst ]
        mac_string = "_".join(mac_res)
        return mac_string
    else:
        return ""

def sn_trans(sn):
    '''
    转化SN序列号，将传递到SN号进行数据格式的转换
    :param sn:
    :return:
    '''
    if sn:
        sn_res = sn.replace(" ", '')
        return sn_res
    else:
        return ""

def machine_type_trans(mt):
    '''
    转化类型，将传递的类型进行数据格式的转换
    :param mt:
    :return:
    '''
    if mt:
        mt_res = mt.replace("\n", '')
        return mt_res
    else:
        return ""


class prpcrypt():
    '''
    用于密钥对于重要的数据加密解密
    '''
    def __init__(self):
        self.key = "iofva0r93184*&^%"
        # 这里的密钥必须是16（AES-128），32（AES-192），64（AES-256）Bytes长度，目前16就够用。
        self.mode = AES.MODE_CBC

    # 加密函数，如果不满16位就用零补足，超过就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')

        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ("\0" * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ("\0" * add)
        self.ciphertext = cryptor.encrypt(text)
        # AES加密后的字串不一定全是ASCII里的，所有要在输出到终端或保存的时候，统一转化成16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

def getsysversion(version_list):
    '''
    提供系统版本
    :param version_list:
    :return:
    '''
    for version_data in version_list:
        v_data_lst = re.findall("vmware|centos|linux|ubuntu|redhat|\d{1, }\.\d{1, }", version_data, re.IGNORECASE)
        if v_data_lst:
            if len(v_data_lst) > 1:
                v_data = " ".join(v_data_lst)
                break
        else:
            v_data = ""
    return  v_data
