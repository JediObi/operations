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
# 'admin@127.0.0.1:22'
host_info = concathost.ConcatHost(host_name,host_port,host_username)

upload_path = config.get('remote','upload_path')
build_name = config.get('local','build_name')
src = config.get('local','project_home')+'/target/'+build_name+'.war'

tomcat_home = config.get('remote','app_tomcat_home')

#env.hosts,env.passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
env.hosts.append(host_info)
# add host pass
env.passwords.setdefault(host_info,host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# upload war from gate to app
def upload():
	with settings(warn_only=True):
		result = put(src,upload_path)
	if result.failed and confirm('put file failed,Y deal, N ignore[Y/N]?'):
		abort('Aborting file put task!')

# deploy to tomcat
def update():
	# stop tomcat
	command = 'ps aux|grep '+tomcat_home+' | grep -v \'grep\' | awk \'{print $2}\''
	with settings(warn_only=True):
		result = run(command)
	if result.succeeded:
		command_shutdown = 'kill -9 '+result.strip()
		run(command_shutdown)
	print('Administrator: Tomcat stopped!')
	
	# remove old version
	command_remove_dir = 'rm -rf '+tomcat_home+'/webapps/'+build_name
	run(command_remove_dir)
	command_remove_file = 'rm -f '+tomcat_home+'/webapps/'+build_name+'.war'
	run(command_remove_file)
	print('Administrator: Old version removed!')

	# copy new version
	command_copy = 'cp '+upload_path+'/'+build_name+'.war'+' '+tomcat_home+'/webapps/'
	run(command_copy)
	print('Administrator: New version copied!')

	# start tomcat
	command_start = '.'+tomcat_version+'/bin/startup.sh'
	run(command_start)
	print('Administrator: Tomcat started!')
	print('Administrator: Deploy complete!')

