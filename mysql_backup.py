#!/usr/bin/env python    
#coding=utf8    
#author : mike duffy
#mail   : mikeduffy@qq.com
#source : https://github.com/duffy25/script/blob/master/mysql_backup.py
#version:1.0


'''
backup mysql script

'''


# Import module
import shlex
from subprocess import PIPE, STDOUT, Popen


# Set the variable
DB_USER = 'example'
DB_PASS = 'example'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_IGNORE = ['Database', 'information_schema', 'performance_schema', '']

BF_PATH = '/tmp'

arg = shlex.split("mysql -u%s -p%s -h%s -P%s -e 'show databases'" % (DB_USER, DB_PASS, DB_HOST, DB_PORT))
DBS = Popen(arg, stdout=PIPE, stderr=STDOUT)
DB = DBS.communicate()[0].split('\n')
DB_BACKUP = filter(lambda v: v not in DB_IGNORE, DB)

new_list = filter(lambda v: v not in DB_IGNORE, DB)

for db in new_list:
    f = open("%s/%s.sql" %(BF_PATH,db), 'w')
    bk_arg = shlex.split("mysqldump -u%s -p%s -h%s -P%s -F %s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, db))
    p1 = Popen(bk_arg, stdout=PIPE)
    for line in p1.stdout:
        f.write(line)
    p1.wait()
    f.close()
    #p2 = Popen('gzip', stdin=p1.stdout, stdout=f)
    #p2.wait()
    print  DBS.communicate()[0]

