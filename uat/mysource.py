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
host_info = concathost.ConcatHost(gate_host_name,gate_host_port,gate_host_username)

upload_path = config.get('remote','upload_path')

# mysql info
db_host = config.get('remote','db_ip')
db_port = config.get('remote','db_port')
db_name = config.get('remote','db_name')
db_username = config.get('remote','db_username')
db_password = config.get('remote','db_passwrod')
db_back_path = config.get('remote','db_back_path')


#env.hosts,env.passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
env.hosts.append(host_info)
env.passwords.setdefault(host_info,host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# deploy to tomcat
def mysource():
	# drop db
	command_drop = 'mysql -h'+db_host+' -P'+db_port+' -u'+db_username+' -p"'+db_password+'" -e "drop database '+db_name+'; create database '+db_name+' default character set utf8 collate utf8_bin;"'
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Drop database[',db_name,']!')
	run(command_drop)
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Empty database[', db_name, '] created!')

	# data
	command_data = 'gunzip < '+db_back_path+'/'+db_name+'_utf8.sql.gz'+' | mysql -h'+db_host+' -P'+db_port+' -u'+db_username+' -p"'+db_password+'" '+db_name
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Data importing started!')
	run(command_data)
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Data importing finished!')

	# func
	command_func = 'gunzip < '+db_back_path+'/'+db_name+'_func_utf8.sql.gz'+' | mysql -h'+db_host+' -P'+db_port+' -u'+db_username+' -p"'+db_password+'" '+db_name
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Functions importing started!')
	run(command_func)
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print(current_time,'Administrator: Functions importing finished!')
