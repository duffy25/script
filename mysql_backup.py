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
from os import path, makedirs
from time import gmtime, strftime

# Set the variable
DB_USER = 'example'
DB_PASS = 'example'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_IGNORE = ['Database', 'information_schema', 'performance_schema', '']
GZ = True
TM_TODAY = strftime("%Y%m%d", gmtime())
PH_BACKUP = '/tmp'

arg = shlex.split("mysql -u%s -p%s -h%s -P%s -e 'show databases'" % (DB_USER, DB_PASS, DB_HOST, DB_PORT))
DBS = Popen(arg, stdout=PIPE, stderr=STDOUT)
DB = DBS.communicate()[0].split('\n')
DB_BACKUP = filter(lambda v: v not in DB_IGNORE, DB)

print "ALL_DB: %s" % DB
new_list = filter(lambda v: v not in DB_IGNORE, DB)


def mkdir():
    if not path.exists(PH_BACKUP):
        makedirs(PH_BACKUP)


for db in DB_BACKUP:
    bk_arg = shlex.split("mysqldump -u%s -p%s -h%s -P%s -F %s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, db))
    p1 = Popen(bk_arg, stdout=PIPE)
    if GZ:
        f_gz = open("%s/%s%s.sql.gz" %(PH_BACKUP, db, TM_TODAY), 'wb')
        p2 = Popen('gzip', stdin=p1.stdout, stdout=f_gz)
        p2.wait()
        p1.wait()
        f_gz.close()
    else:
        f = open("%s/%s%s.sql" %(PH_BACKUP, db, TM_TODAY), 'w')
        for line in p1.stdout:
            f.write(line)
        p1.wait()
        f.close()