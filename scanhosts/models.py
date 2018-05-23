# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.

class Hostscaninfo(models.Model):
    TYPE_CHOICE = (
        ('0', 'kvm'),
        ('1', 'docker'),
        ('2', 'vmx'),
    )
    ip = models.CharField(max_length=70, verbose_name='IP地址信息')
    ssh_port = models.CharField(max_length=10, null=True, verbose_name='ssh登陆端口')
    ssh_user = models.CharField(max_length=16, null=True, verbose_name='ssh登陆用户名')
    ssh_pass = models.CharField(max_length=32, null=True, verbose_name='ssh登陆密码', default='')
    ssh_rsa = models.CharField(max_length=64, null=True, verbose_name='私钥', default='')
    rsa_pass = models.CharField(max_length=32, null=True, verbose_name='私钥密码', default='')
    system_ver = models.CharField(max_length=64, null=True, verbose_name='系统类型版本', default='')
    hostname = models.CharField(max_length=64, null=True, verbose_name='主机名', default='')
    ssh_status = models.IntegerField(verbose_name='0：失败 1：成功', default=0)
    ssh_type = models.IntegerField(verbose_name="1：rsa 2:dsa 3:normal_user rsa 4:docker成功 5：docker失败")
    mac_addr = models.CharField(max_length=256, verbose_name="mac地址列表", default="")
    sn = models.CharField(max_length=64, verbose_name="设备SN信息", default="")
    machine_type = models.IntegerField(verbose_name="设备类型 1物理服务器 2网络设备 3其它设备 4虚拟设备", default="")
    machine_id = models.CharField(max_length=64, verbose_name="唯一设备ID", default="")
    host_type = models.CharField(max_length=64, verbose_name="宿主机上的虚拟机类型", choices=TYPE_CHOICE, default="")
    class Meta:
        verbose_name = "初始扫描信息表"
        verbose_name_plural = verbose_name
        db_table = "Hostscaninfo"
