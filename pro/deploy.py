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
# 'admin@127.0.0.1:22'
gate_host = concathost.ConcatHost(gate_host_name,gate_host_port,gate_host_username)

gate_upload_path = config.get('remote','upload_path')
build_name = config.get('local','build_name')
# war file path in gate
src = gate_upload_path+'/'+build_name+'.war'

server_name = config.get('remote','server_name')
server_count = config.getint('remote','server_count')

app_tomcat_home = config.get('remote','app_tomcat_home')
app_upload_path = config.get('upload','app_upload_path')

# get server list
host_list = []
port_list = []
username_list = []
password_list = []
# read server info into list
for i in range(server_count):
	host_list.append(config.get(server_name+str(i),'host_name'))
	port_list.append(config.get(server_name+str(i),'host_port'))
	username_list.append(config.get(server_name+str(i),'host_username'))
	password_list.append(config.get(server_name+str(i),'host_password'))
# set host(list) info and pass(dictionary)
env.hosts,env.passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
# set gateway host info
env.gateway = gate_host
# add gateway host pass
env.passwords.setdefault(gate_host,gate_host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# upload war from gate to app
def upload():
	with settings(warn_only=True):
		result = put(src,app_upload_path)
	if result.failed and confirm('put file failed,Y deal, N ignore[Y/N]?'):
		abort('Aborting file put task!')

# deploy to tomcat
def update():
	# stop tomcat
	command = 'ps aux|grep '+app_tomcat_home+' | grep -v \'grep\' | awk \'{print $2}\''
	result = run(command)
	if result:
		command_shutdown = 'kill -9 '+result.strip()
		run(command_shutdown)
	print('Administrator: Tomcat stopped!')
	
	# remove old version
	command_remove_dir = 'rm -rf '+app_tomcat_home+'/webapps/'+build_name
	run(command_remove_dir)
	command_remove_file = 'rm -f '+app_tomcat_home+'/webapps/'+build_name+'.war'
	run(command_remove_file)
	print('Administrator: Old version removed!')

	# copy new version
	command_copy = 'cp '+app_upload_path+'/'+build_name+'.war'+' '+app_tomcat_home+'/webapps/'
	run(command_copy)
	print('Administrator: New version copied!')

	# start tomcat
	command_start = '.'+app_tomcat_version+'/bin/startup.sh'
	run(command_start)
	print('Administrator: Tomcat started!')
	print('Administrator: Deploy complete!')

