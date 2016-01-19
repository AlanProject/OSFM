#!/usr/bin/env python
#-*- coding:utf-8 -*-
import paramiko
class SSH_REMOTE(object):
    def __init__(self,hostname,user,passwd,port=22):
        self.hostname = hostname
        self.port = port
        self.user = user
        self.passwd = passwd
    def ssh_run(self,command):
        transport = paramiko.Transport((self.hostname,self.port))
        transport.connect(username=self.user,password=self.passwd)
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        #允许连接不在know_hosts文件中的主机。
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin,stdout,stderr = ssh.exec_command(command)
        data = stdout.read()
        ssh.close()
        return data
if __name__ == '__main__':
    pass