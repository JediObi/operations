# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm

config_file = 'pro.cnf'

config = configparser.ConfigParser()
config.read(config_file)

host_name = config.get('remote','host_name')
host_port = config.get('remote','host_port')
host_username = config.get('remote','host_username')
host_password = config.get('remote','host_password')
host_info = concathost.ConcatHost(host_name,host_port,host_username)

tomcat_home = config.get('remote','app_tomcat_home')

# download file info
config_download_file='./download/download.cnf'
config_download = configparser.ConfigParser()
config_download.read(config_download_file)
file_count = config_download.getint('download','file_count')

env.hosts.append(host_info)
# add gateway host pass
env.passwords.setdefault(host_info,host_password)

# print host and pass
def test():
	print(prompt("What hostname?"))

# upload war from gate to app
def download():
	for i in range(file_count):
		file_name = config_download.get('file'+str(i),'file_name')
		file_src = config_download.get('file'+str(i),'target_path')+'/'+file_name
		# download
		with settings(warn_only=True):
			result = get(file_src,'./download/')
		if result.failed and confirm('put file failed,Y to deal error, N ignore?'):
			abort('no deal')
