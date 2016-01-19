#!/usr/bin/env python
#-*- coding:utf-8 -*-
from modules import conn_mysql
from modules import conn_ssh
class OSFM_main(object):
    def __init__(self):
        self.conn_mysql = conn_mysql.mysql_access()
        self.handle()
    def handle(self):
        print '\033[5;31;0mWeclome OSFM\033[;0m'.center(50,'-')
        if not self.login():
            exit('认证失败')
        hostgroup =self.conn_mysql.run('select groupname from host_group where id =(select hostgroup from user)')
        data = self.conn_mysql.run('select hostname,ipaddress from hosts where hostgroup=(select hostgroup from user)');
        print '\033[34;0m主机组\t主机名\tIP地址\033[;0m'
        for n,i in enumerate(data,1):
            print '%d\t%s\t%s\t%s'%(n,hostgroup[0][0],i[0],i[1])
        change = int(raw_input('请选择要操作的主机'))-1
        ipaddress = data[change][1]
        sql = "select user,passwd from hosts where ipaddress='%s'"%ipaddress
        user,passwd = self.conn_mysql.run(sql)[0]
        self.conn_ssh = conn_ssh.SSH_REMOTE(ipaddress,user,passwd)
        while True:
            command = raw_input('command >>')
            if command == 'exit':
                break
            else:
                print self.conn_ssh.ssh_run(command)
    def login(self):
        while True:
            user_name = raw_input('请输入用户名：')
            if not user_name:
                continue
            command = 'select * from user where name="%s"'%user_name
            data = self.conn_mysql.run(command)
            if data:
                tage = 0
                while tage < 3:
                    user_passwd = raw_input('请输入密码：')
                    if data[0][2] == user_passwd:
                        return True
                        break
                    else:
                        print 'user or password error'
                        tage +=1
            else:
                exit('uesr not found')
