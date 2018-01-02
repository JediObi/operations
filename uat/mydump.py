# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm
import time

config_file = 'uat.cnf'

config = configparser.ConfigParser()
config.read(config_file)

host_name = config.get('remote','host_name')
host_port = config.get('remote','host_port')
host_username = config.get('remote','host_username')
host_password = config.get('remote','host_password')
# 'admin@127.0.0.1:22'
host_info = concathost.ConcatHost(gate_host_name,gate_host_port,gate_host_username)

upload_path = config.get('remote','upload_path')

# mysql info
db_host = config.get('remote','db_ip')
db_port = config.get('remote','db_port')
db_name = config.get('remote','db_name')
db_username = config.get('remote','db_username')
db_password = config.get('remote','db_passwrod')
db_back_path = config.get('remote','db_back_path')

local_db_back_path = config.get('local','db_back_path')

#env.hosts,env.passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
env.hosts.append(host_info)
env.passwords.setdefault(host_info,host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# deploy to tomcat
def mydump():
	# get date
	localtime = time.localtime()
	strftime = time.strftime('%Y-%m-%d',localtime)
	# mkdir
	command_find_dir = 'ls '+db_back_path+' | grep '+strftime
	with settings(warn_only=True):
		result = run(command_find_dir)
	if result.failed:
		command_mkdir = 'mkdir -p '+db_back_path+'/'+strftime
		run(command_mkdir)	
	# data
	command_data = 'mysqldump -h'+db_host+' -P'+db_port+' -u'+db_username+' -p"'+db_password+'" --default-character-set=utf8 '+db_name+' | gzip > '+db_back_path+'/'+strftime+'/'+db_name+'_utf8.sql.gz'
	current_time = time.strftime(time.localtime())
	print(current_time,'Administrator: Data backup started!')
	run(command_data)
	current_time = time.strftime(time.localtime())
	print(current_time,'Administrator: Data backup finished!')
	# func
	command_func = 'mysqldump -h' + db_host + ' -P' + db_port + ' -u' + db_username + ' -p"' + db_password + '" --default-character-set=utf8 -ndt -R ' + db_name + ' | gzip > ' + db_back_path + '/'+strftime+'/'+db_name+'_func_utf8.sql.gz'
	current_time = time.strftime(time.localtime())
	print(current_time,'Administrator: Functions backup started!')
	run(command_func)
	current_time = time.strftime(time.localtime())
	print(current_time,'Administrator: Functions backup started!')
	
	# download
	get(db_back_path+'/'+strftime,local_db_back_path)
