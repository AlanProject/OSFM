#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pymysql
import os
import ConfigParser
class mysql_access(object):
    def __init__(self):
        basedir =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_file = basedir+'\config\conn_db.conf'
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.server = config.get('mysqld','db_server')
        self.port = config.get('mysqld','db_port')
        self.user = config.get('mysqld','db_user')
        self.passwd =config.get('mysqld','db_passwd')
        self.db = config.get('mysqld','db_name')
    def run(self,command):
        mysql_conn = pymysql.connect(host=self.server,user=self.user,passwd=self.passwd,db=self.db)
        cur = mysql_conn.cursor()
        data=cur.execute(command)
        cur.close()
        mysql_conn.close()
        return cur.fetchall()
if __name__ == '__main__':
    mysql = mysql_access()
    print mysql.run("""create table hostgroup(id int(5) NOT NULL auto_increment,groupname varchar(20) NOT NULL,PRIMARY KEY(id))""")