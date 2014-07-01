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
from os import path, makedirs, remove
from time import gmtime, strftime
from datetime import timedelta, date

# Set the variable
DB_USER = 'example'
DB_PASS = 'example'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_IGNORE = ['', 'Database', 'information_schema', 'performance_schema']
PH_BACKUP = '/tmp'
TM_TODAY = strftime("%Y%m%d", gmtime())
GZ = True
BK_COPY = 7
DEL_TIME =(date.today() + timedelta(days = -abs(BK_COPY))).strftime("%Y%m%d")



ARG = shlex.split("mysql -u%s -p%s -h%s -P%s -e 'show databases'" % (DB_USER, DB_PASS, DB_HOST, DB_PORT))
DB_ALL = Popen(ARG, stdout=PIPE, stderr=STDOUT)
DB_ALL.wait()
DB = DB_ALL.communicate()[0].split('\n')
DB_BACKUP = filter(lambda v: v not in DB_IGNORE, DB)

print "AVAILABLE_DB: %s" % filter(lambda v: v not in '', DB)
print "BACKUP_DB: %s" % DB_BACKUP


def run_backup():
    for db in DB_BACKUP:
        bk_arg = shlex.split("mysqldump -u%s -p%s -h%s -P%s -F %s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, db))
        p1 = Popen(bk_arg, stdout=PIPE)
        if GZ:
            f_gz = open("%s/%s_%s.sql.gz" %(PH_BACKUP, db, TM_TODAY), 'wb')
            p2 = Popen('gzip', stdin=p1.stdout, stdout=f_gz)
            p2.wait()
            p1.wait()
            f_gz.close()
            try:
                print "%s/%s_%s.sql.gz" %(PH_BACKUP, db, DEL_TIME)
                remove("%s/%s_%s.sql.gz" %(PH_BACKUP, db, DEL_TIME))
            except:
                pass
        else:
            f = open("%s/%s_%s.sql" %(PH_BACKUP, db, TM_TODAY), 'w')
            for line in p1.stdout:
                f.write(line)
            p1.wait()
            f.close()
            try:
                print "%s/%s_%s.sql" %(PH_BACKUP, db, DEL_TIME)
                remove("%s/%s_%s.sql" %(PH_BACKUP, db, DEL_TIME))
            except:
                pass



if __name__ == "__main__":
    if not path.exists(PH_BACKUP):
        makedirs(PH_BACKUP)
    run_backup()
