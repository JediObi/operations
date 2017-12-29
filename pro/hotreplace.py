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

gate_upload_path = config.get('remote','upload_path')
build_name = config.get('local','build_name')
src = gate_upload_path+'/'+build_name+'.war'

server_name = config.get('remote','server_name')
server_count = config.getint('remote','server_count')

app_tomcat_home = config.get('remote','app_tomcat_home')
app_upload_path = config.get('upload','app_upload_path')


# hot replace file info
config_upload_file='./upload/upload.cnf'
config_upload = configparser.ConfigParser()
config_upload.read(config_upload_file)
file_count = config_upload.getint('upload','file_count')


# get server list
host_list = []
port_list = []
username_list = []
password_list = []
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
	print(env.hosts,env.passwords)

# upload war from gate to app
def hotreplace():
	for i in range(file_count):
		file_name = config_upload.get('file'+str(i),'file_name')
		file_src = gate_upload_path+'/'+file_name
		# upload
		with settings(warn_only=True):
			result = put(file_src,app_upload_path)
		if result.failed and confirm('put file failed,Y to deal error, N ignore?'):
			abort('no deal')
		# replace
		command_copy = 'cp '+app_upload_path+'/'+file_name+' '+app_tomcat_home+'/webapps/'+build_name+'/'+config_upload.get('file'+str(i),'relative_path')
		run(command_copy)

