# -*- coding:utf-8 -*-

from django.core.mail import send_mail

import time

class sendmail():
    def __init__(self, receive_addr, sub_info, content_info):
        sub_data =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.recevive_addr = receive_addr
        self.sub_info = sub_info + sub_data
        self.content_info = content_info

    def send(self):
        try:
            send_mail(from_email="d360478265@163.com",
                      subject=self.sub_info,
                      message=self.content_info,
                      recipient_list=self.recevive_addr,
                      fail_silently=False,
                      )
            return True
        except Exception as e:
            print(e)
            return False
