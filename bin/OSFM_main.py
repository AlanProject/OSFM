#!/usr/bin/env python
#-*- coding:utf-8 -*-
from modules import conn_mysql
class OSFM_main(object):
    def __init__(self):
        self.handle()
    def handle(self):
        print '\033[5;31;0mWeclome OSFM\033[;0m'.center(50,'-')
        if self.login():
            print 'seucess'

    def login(self):
        while True:
            user_name = raw_input('请输入用户名：')
            if not user_name:
                continue
            mysql =  conn_mysql.mysql_access()
            #mysql.run("INSERT INTO user(name,passwd) VALUES ('alan','root')")
            command = 'select * from user where name="%s"'%user_name
            data = mysql.run(command)
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
