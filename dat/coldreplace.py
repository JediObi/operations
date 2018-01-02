# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm

config_file = 'dat.cnf'

config = configparser.ConfigParser()
config.read(config_file)

host_name = config.get('remote','host_name')
host_port = config.get('remote','host_port')
host_username = config.get('remote','host_username')
host_password = config.get('remote','host_password')
host_info = concathost.ConcatHost(host_name,host_port,host_username)

upload_path = config.get('remote','upload_path')
build_name = config.get('local','build_name')

tomcat_home = config.get('remote','app_tomcat_home')

# replace file info
config_upload_file='./upload/upload.cnf'
config_upload = configparser.ConfigParser()
config_upload.read(config_upload_file)
file_count = config_upload.getint('upload','file_count')

env.hosts.append(host_info)
# add gateway host pass
env.passwords.setdefault(host_info,host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# upload war from gate to app
def coldreplace():
	# stop tomcat
	command_tomcat_pid = 'ps aux | grep '+tomcat_home+' | grep -v \'grep\' | awk \'{print $2}\''
	with settings(warn_only=True):
		result = run(command_tomcat_pid)
	if result.succeeded:
		command_shutdown = 'kill -9 '+ result.strip()
		run(command_shutdown)
	
	# upload files and replace
	for i in range(file_count):
		file_name = config_upload.get('file'+str(i),'file_name')
		file_src = upload_path+'/'+file_name
		# replace
		command_copy = 'cp '+file_src+' '+config_upload.get('file'+str(i),'target_path')
		run(command_copy)
	# start tomcat
	command_startup = '.'+tomcat_home+'/bin/startup.sh'
	run(command_startup)
