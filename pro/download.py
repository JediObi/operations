# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm

config_file = 'pro.cnf'

config = configparser.ConfigParser()
config.read(config_file)

gate_host_name = config.get('remote','host_name')
gate_host_port = config.get('remote','host_port')
gate_host_username = config.get('remote','host_username')
gate_host_password = config.get('remote','host_password')
gate_host = concathost.ConcatHost(gate_host_name,gate_host_port,gate_host_username)

gate_download_path = config.get('remote','upload_path')
# build_name = config.get('local','build_name')

server_name = config.get('remote','server_name')
server_count = config.getint('remote','server_count')

app_tomcat_home = config.get('remote','app_tomcat_home')

# download file info
config_download_file='./download/download.cnf'
config_download = configparser.ConfigParser()
config_download.read(config_download_file)
file_count = config_download.getint('download','file_count')


# get server list
host_list = []
port_list = []
username_list = []
password_list = []
# append server info list
for i in range(server_count):
	host_list.append(config.get(server_name+str(i),'host_name'))
	port_list.append(config.get(server_name+str(i),'host_port'))
	username_list.append(config.get(server_name+str(i),'host_username'))
	password_list.append(config.get(server_name+str(i),'host_password'))
# set host info and pass
env.hosts,env.passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
# set gateway host info
env.gateway = gate_host
# add gateway host pass
env.passwords.setdefault(gate_host,gate_host_password)

# print host and pass
def test():
	print(prompt("What hostname?"))

# upload war from gate to app
def download():
	command_get_host = 'ifconfig|grep inet|grep mask|grep cast|awk \'{print $2}\''
	result = run(command_get_host)
	current_host = result.strip()
	for i in range(file_count):
		file_name = config_download.get('file'+str(i),'file_name')
		file_src = config_download.get('file'+str(i),'target_path')+'/'+file_name
		# download
		with settings(warn_only=True):
			result = get(file_src,gate_download_path+'/'+file_name+'.'+current_host)
		if result.failed and confirm('put file failed,Y to deal error, N ignore?'):
			abort('no deal')
