#!/usr/bin/env python
#-*- coding:utf-8 -*-
#auther = Alan
'''
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.17.128',port=22,username='sysadmin',password='wangyufei!@#')
stdin,stdout,stderr = ssh.exec_command('ls / -l')
data = stdout.read()
print data
ssh.close()
'''
import paramiko
import select
import socket
import termios,tty
import sys
tran = paramiko.Transport('192.168.17.128',22)
tran.start_client()
tran.auth_password('sysadmin','wangyufei!@#')
chan=tran.open_session()
chan.get_pty()
chan.invoke_shell()
oldtty = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin.fineno())
chan.settimeout(0.0)
try:
    while True:
        rList,wList,eList = select.select([chan,sys.stdin,],[],[],1)
        if chan in rList:
            try:
                x = chan.recv(1024)
                if len(x) == 0:
                    print '\r\n***EOF\r\n'
                    break
                sys.stdout.write(x)
                sys.stdout.flush()
            except socket.timeout:
                pass
                if sys.stdin in rList:
                    inp = sys.stdin.readline()
                    chan.sendall(inp)
finally:
    termios.tcsetatt(sys.stdin,termios.TCSADRAIN,oldtty)
    chan.close()
    tran.close()