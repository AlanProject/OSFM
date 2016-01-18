#!/usr/bin/env python
#-*- coding:utf-8 -*-
import paramiko
#ssh.connect(hostname='192.168.3.53',port=22,username='root',password='jinher!@#')
transport = paramiko.Transport(('192.168.3.53',22))
transport.connect(username='root',password='jinher!@#')
ssh = paramiko.SSHClient()
ssh._transport = transport
#允许连接不在know_hosts文件中的主机。
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
stdin,stdout,stderr = ssh.exec_command('ifconfig')
print stdout.read()
ssh.close()
if __name__ == '__main__':
    pass