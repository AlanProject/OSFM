#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import sys
from paramiko.py3compat import u

# wwindows下没有termios模块所以这里通过判断termios模块来判断系统平台
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    #如果是linux则执行linux相关的方法
    if has_termios:
        posix_shell(chan)
    #如果是windows则执行windows相关的方法
    else:
        windows_shell(chan)

#linux终端
def posix_shell(chan):
    #导入select模块
    import select
    #对现有的tty模式进行保存备份
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        #将终端设置成为原始终端
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            #利用selecet监听stdin状态
            r, w, e = select.select([chan, sys.stdin], [], [])
            #如果是socket发生变化则接受数据并做相应的处理
            if chan in r:
                try:
                    #接收用户输入
                    x = u(chan.recv(1024))
                    #如果接收到的值为空（说明已经断开连接）
                    if len(x) == 0:
                        #打印一个字符
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    #如果不为空则在终端显示 并刷新写入
                    sys.stdout.write(x)
                    sys.stdout.flush()
                #socket超时处理
                except socket.timeout:
                    pass
            #如果
            if sys.stdin in r:
                #每隔一个字符
                x = sys.stdin.read(1)
                #如果输入为空则跳出循环
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        #将本地终端状态修改回原来的终端状态
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading
    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
    def writeall(sock):
        while True:
            #接受数据
            data = sock.recv(256)
            #判断数据是否为空
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
