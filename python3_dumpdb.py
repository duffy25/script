#!/usr/bin/env python3

import os
import subprocess
import pymysql
import time

# 数据库连接配置
sql_host = 'localhost'
sql_user = 'root'
sql_pwd = ''

# 存放备份文件的根目录
backup_root_path = './backups/'

# 确保备份目录存在
if not os.path.exists(backup_root_path):
    os.makedirs(backup_root_path)

# 获取所有数据库名称
def get_databases():
    connection = pymysql.connect(host=sql_host, user=sql_user, password=sql_pwd)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            return [db[0] for db in cursor.fetchall() if db[0] not in ('information_schema', 'mysql', 'performance_schema', 'sys')]
    finally:
        connection.close()

# 执行mysqldump备份单个数据库
def dump_database(db_name):
    timestamp = time.strftime('%Y%m%d%H%M%S')
    backup_file = f"{db_name}_{timestamp}.sql"
    backup_path = os.path.join(backup_root_path, backup_file)
    command = f"mysqldump -h{sql_host} -u{sql_user} -p'{sql_pwd}' {db_name} > {backup_path} --default-character-set=utf8"
    return subprocess.call(command, shell=True)

# 主函数，遍历所有数据库并执行备份
def main():
    databases = get_databases()
    for db in databases:
        print(f"Backing up database: {db}")
        result = dump_database(db)
        if result == 0:
            print(f"Database {db} backed up successfully.")
        else:
            print(f"Failed to backup database {db}.")

if __name__ == "__main__":
    main()
