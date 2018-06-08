# -*- coding:utf-8 -*-

# import nmap
# import telnetlib
# import re
# import getpass
# from django.db import models
import os

import paramiko
import traceback
from scanhosts.models import Hostscaninfo
from  scanhosts.lib.utils import prpcrypt
import pexpect,datetime

import logging
logger = logging.getLogger("django")
os.environ["DJANGO_SETTING_MODULE"] = 'optools.setting'

class J_ssh_do(object):
    def __init__(self, info=""):
        self.whitelist = ["192.168.31.1", "192.168.31.2", "192.168.31.3", "192.168.31.4", "192.168.31.5"]
        self.result = {'info': info}

    def pass_do(self, login_info, cmd_list=""):
        '''
        用户密码方式登陆
        :param login_info:登录的信息，如ip,port,username,userpass
        :param cmd_list:登录机器后，执行的命令列表
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(login_info[0], login_info[1], login_info[2], login_info[3], timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=6)
                std_result = stdout.read()
                self.result[cmd] = std_result
        except Exception as e:
            print(traceback.print_exc(), login_info)
            logger.exception("use ssh password login exception:%s,%s" % (e, login_info))
            self.result["status"] = "fail"
            self.result["res"] = str(e)
        return self.result

    def rsa_do(self, login_info, cmd_list=""):
        '''
        id_rsa密钥登录
        :param login_info: 登录的信息，如ip,port,username,userlogin_key,key_pass
        :param cmd_list:登录机器后，执行的命令列表
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            key = paramiko.RSAKey.from_private_key_file(login_info[3])
            ssh.connect(login_info[0], login_info[1], login_info[2], pkey=key, timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=6)
                std_result = stdout.read()
                self.result[cmd] = std_result
        except Exception as e:
            print(traceback.print_exc())
            logger.exception("use ssh rsa key login exception:%s,%s" %(e, login_info))
            self.result["status"] = "fail"
            self.result["res"] = e
        return self.result

    def dsa_do(self, login_info, cmd_list):
        '''
        id_dsa密钥登录
        :param login_info: 登录的信息，如ip,port,username,userlogin_key,key_pass
        :param cmd_list: 登录机器后，执行的命令列表
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.DSSKey.from_private_key_file(login_info[3])
            ssh.connect(login_info[0], login_info[1], login_info[2], pkey=key, timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=6)
                std_result = stdout.read()
                self.result[cmd] = std_result
        except Exception as e:
            print(traceback.print_exc())
            logger.exception("use ssh dsa key login exception:%s,%s" % (e, login_info))
            self.result["status"] = "fail"
            self.result["res"] = e
        return self.result

    def run(self, ip, cmd):
        if ip and cmd:
            print('......................ip', ip)
            ip_item = Hostscaninfo.objects.get(ip=ip)
            cn = prpcrypt()
            if ip_item.ssh_type == 0:
                ssh_passwd = cn.decrypt(ip_item.ssh_passwd)
                login_info = (ip_item.ip, int(ip_item.ssh_port), ip_item.ssh_user, ssh_passwd)
                res = self.pass_do(login_info, cmd)
            elif ip_item.ssh_type == 1:
                login_info = (ip_item.ip, int(ip_item.ssh_port), ip_item.ssh_user, ip_item.ssh_rsa)
                res = self.rsa_do(login_info, cmd)
            elif ip_item.ssh_type == 2:
                login_info = (ip_item.ip, int(ip_item.ssh_port), ip_item.ssh_user, ip_item.ssh_dsa)
                res = self.dsa_do(login_info, cmd)
            elif ip_item.ssh_type == 3:
                login_info = (ip_item.ip, int(ip_item.ssh_port), ip_item.ssh_user, ip_item.ssh_rsa, ip_item.rsa_pass)
                res = self.rsa_do(login_info, cmd)
            return res
        else:
            return ""

class J_net_do():
    '''
    登录交换机(cisco)执行，验证登录，执行备份
    '''

    def __init__(self, ip, login_info):
        self.username, self.passwd, self.en_passwd = login_info
        self.ip = ip

    def getToday(self):
        return datetime.date.today()

    def cisco_backup(self, back_server="", sw_backup=False):
        result = {}
        try:
            np = pexpect.spawn('telnet %s' % self.ip)
            re_index = np.expect(['Username:', 'Password:'])

            if re_index == 0:
                np.sendline(self.username)
                np.expect('Password:')
                np.sendline(self.passwd)
                result["level"] == 1
                result["login_info"] = (self.username, self.passwd, self.en_passwd)
            elif re_index == 1:
                np.sendline(self.passwd)
                result["level"] = 1
                result["login_info"] = ("", self.passwd, self.en_passwd)

            su_index = np.expect(['>', '#'])
            if su_index == 0:
                np.sendline('enable')
                np.expect('Password:')
                np.sendline(self.en_passwd)
                np.expect('#')

            if sw_backup:
                np.sendline("copy running config tftp")
                np.expect(".*remote.*")
                np.sendline("%s" % back_server)
                np.expect(".*filename.*")
                np.sendline("%s" % ((self.ip + '_' + str(self.getToday()) + "_runningconfig.cfg")))
                np.expect('#')
                np.sendline("exit")
                result["level"] == 2
            else:
                np.sendline("exit")
                result["level"] == 2
            result["status"] == "success"
        except Exception as e:
            result["status"] = "failed"
            result["res"] = str(e)
            print("Net device ip %s backup error, error info %s" % (self.ip, e))
            logger.error("Net device ip %s backup error, error info %s" % (self.ip, e))
        return result

    def cisco_login(self):
        result = {}

        try:
            np = pexpect.spawn('telnet %s' % (self.ip))
            re_index = np.expect(['Username:', 'Password:'])

            if re_index == 0:
                np.sendline(self.username)
                np.expect('Password:')
                np.sendline(self.passwd)
                result["level"] = 1
                result["login_info"] = (self.username, self.passwd, self.en_passwd)
            elif re_index == 1:
                np.sendline(self.passwd)
                result["level"] = 1
                result["login_info"] = ("", self.passwd, self.en_passwd)

            su_index = np.expect(['>', '#'])
            if su_index == 0:
                np.sendline('enable')
                np.expect('Password:')
                np.sendline(self.en_passwd)
                np.expect('#')
                np.sendline("exit")
                result['level'] = 2
            else:
                np.sendline("exit")
                result['level'] = 2
            result["status"] = "success"

        except Exception as e:
            result['status'] = "failed"
            result["res"] = str(e)
            print("Net Device ip %s login not ok, error:%s" % (self.ip, e))
            logger.error("Net Device ip %s login not ok, error:%s" % (self.ip, e))
        return result









