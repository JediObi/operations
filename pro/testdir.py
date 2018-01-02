# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm
import time

config_file = 'pro.cnf'

config = configparser.ConfigParser()
config.read(config_file)

host_name = config.get('remote','host_name')
host_port = config.get('remote','host_port')
host_username = config.get('remote','host_username')
host_password = config.get('remote','host_password')
# 'admin@127.0.0.1:22'
host_info = concathost.ConcatHost(host_name,host_port,host_username)

upload_path = config.get('remote','upload_path')

# mysql info
db_host = config.get('remote','db_ip')
db_port = config.get('remote','db_port')
db_name = config.get('remote','db_name')
db_username = config.get('remote','db_username')
db_password = config.get('remote','db_password')
db_back_path = config.get('remote','db_back_path')


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
	# mkdire
	command_find_dir = 'ls '+db_back_path+' | grep '+strftime
	with settings(warn_only=True):	
		result = run(command_find_dir)
	print('result:')
	if result.failed:
		print('deal!')
		command_mkdir = 'mkdir '+db_back_path+'/'+strftime
		run(command_mkdir)	
	
	# download
	local_command_find_dir = 'ls ./db_bak/ | grep '+strftime
	with settings(warn_only=True):
		result = local(local_command_find_dir)
	if result.failed:
		local_command_mkdir = 'mkdir ./db_bak/'+strftime
		local(local_command_mkdir)	
	local_path = './db_bak/'
	get(db_back_path+'/'+strftime,local_path)		
