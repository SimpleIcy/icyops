from django.db import models

import django.utils.timezone as timezone
# Create your models here.

# user login info table

class ConnectionInfo(models.Model):
    ssh_username = models.CharField(max_length=10, default='', verbose_name='ssh用户名', null=True)
    ssh_password = models.CharField(max_length=40, default='', verbose_name='ssh password', null=True)
    ssh_hostip = models.CharField(max_length=40, default='', verbose_name='device or host ip', null=True)
    ssh_host_port = models.IntegerField(max_length=5, default='22', verbose_name='ssh port', null=True)
    ssh_rsa = models.CharField(max_length=64, default='', verbose_name='ssh rsa key')
    rsa_pass = models.CharField(max_length=64, default='', verbose_name='rsa key pass', null=True)
    ssh_status = models.IntegerField(default=0, verbose_name='登录状态，0表示失败，1表示成功')
    ssh_type = models.IntegerField(default=0, verbose_name='ssh类型，0－密码，1－rsa，2－dsa，3－带密码rsa，4－docker成功,5-docker无法登录')
    sn_key = models.CharField(max_length=256, verbose_name='唯一设备ID', default='')

    class Meta:
        verbose_name = '用户登录信息表'
        verbose_name_plural = verbose_name
        db_table = "connectioninfo"

# devices like switch and router
class NetConnectionInfo(models.Model):
    tel_username = models.CharField(max_length=16, default='', verbose_name='用户名', null=True)
    tel_userpasswd = models.CharField(max_length=32, default='', verbose_name='普通用户密码', null=True)
    tel_enpasswd = models.CharField(max_length=32, default='', verbose_name='超级用户密码', null=True)
    tel_host_port = models.IntegerField(max_length=5, default='23', verbose_name='登录端口', null=True)
    tel_hostip = models.CharField(max_length=40, verbose_name='登录IP', null=True)

    tel_status = models.IntegerField(default=0, verbose_name='0-登录失败，1－成功')
    tel_type = models.IntegerField(default=0, verbose_name='0-普通用户，1－超级用户')

    sn_key = models.CharField(max_length=256, default='', verbose_name='唯一设备ID', null=True)

    class Meta:
        verbose_name = '网络设备用户登录信息'
        verbose_name_plural = verbose_name
        db_table = 'netconnectioninfo'

# 机柜信息
class CabinetInfo(models.Model):
    cab_name = models.CharField(max_length=40, verbose_name='机柜编号')
    cab_level = models.IntegerField(max_length=2, verbose_name='机器的位置，从下到上，1－10')

    class Meta:
        verbose_name = "机器所在机柜相关信息表"
        verbose_name_plural = verbose_name
        db_table = "cabinetinfo"


# 物理服务器信息
class PhysicalServerInfo(models.Model):
    server_ip = models.CharField(max_length=40, verbose_name='服务器IP')

    machine_brand = models.CharField(max_length=32, verbose_name='机器品牌')

    sys_ver = models.CharField(max_length=56, verbose_name='操作系统')

    ser_hostname = models.CharField(max_length=64, verbose_name='服务器主机名')

    mac = models.CharField(max_length=256, verbose_name='网卡MAC地址')

    sn = models.CharField(max_length=64, verbose_name='唯一设备ID')

    vir_type = models.IntegerField(max_length=1, verbose_name='寄宿虚拟机类型')
    ser_cabin = models.ForeignKey('cabinetinfo')

    conn_phy = models.ForeignKey('connectioninfo')

    class Meta:
        verbose_name = "物理服务器信息表"
        verbose_name_plural = verbose_name
        db_table = "physicalserverinfo"

# 虚拟服务器信息
class VirtualServerInfo(models.Model):
    server_ip = models.CharField(max_length=40, default='', verbose_name='虚拟机IP')

    server_type = models.IntegerField(max_length=1, verbose_name='0-kvm,1-vmware,2-docker,3-other')

    sys_ver = models.CharField(max_length=56, verbose_name='操作系统')
    ser_hostname = models.CharField(max_length=64, verbose_name='服务器主机名')
    mac = models.CharField(max_length=256, verbose_name='网卡MAC地址')
    sn = models.CharField(max_length=64, verbose_name='唯一设备ID')

    vir_phy = models.ForeignKey('physicalserverinfo')

    conn_vir = models.ForeignKey('connectioninfo')

    class Meta:
        verbose_name = "虚拟服务器信息表"
        verbose_name_plural = verbose_name
        db_table = "virtualserverinfo"





