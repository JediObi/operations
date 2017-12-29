# -*- coding:utf-8 -*-

import paramiko
import configparser
import os
from utils import *
from zipfile import ZipFile

CONFIG_FILE='dat.cnf'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

hostname_ = ''
port_ = 22
username_ = ''
password_ = ''
ssh = ''

hostname_ = config.get('remote','host_name')
port_ = config.get('remote','host_port')
username_ = config.get('remote','host_username')
password_ = config.get('remote','host_password')

# ssh connection
try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	ssh.connect(hostname=hostname_, username=username_, port=port_, password=password_)
	print('ssh %s@%s success!!!'%(username_, hostname_)
except Exception as e:
	print('ssh %s@%s failed!%s'%(username_, hostname_, e))
	os._exit(0)

# upload
project_dir = config.get('local','project_dir')
build_name = config.get('local','build_name')
src = project_dir+'/target/'+build_name+'.war'
# check config
war_file = ZipFile(src,'r')
dbconfig_file = war_file.open('WEB-INF/classes/dbconfig.properties','r')
dbconfig = '[dummy_section]\n'+dbconfig.read().decode('utf-8')
tmp_config = configparser.ConfigParser()
tmp_config.read_string(dbconfig)
if not config.get('remote','db_type')==tmp_config.get('dummy_section','dbtype'):
	print('DB type error!!!')
	ssh.close()
	os._exit()
if not config.get('remote','db_ip')==tmp_config.get('dummy_section','ip'):
	print('DB ip error!!!')
	ssh.close()
	os._exit()
if not config.get('remote','db_port')==tmp_config.get('dummy_section','port'):
	print('DB port error!!!')
	ssh.close()
	os._exit()
if not config.get('remote','db_username')==tmp_config.get('dummy_section','username'):
	print('DB username error!!!')
	ssh.close()
	os._exit()
if not config.get('remote','db_password')==tmp_config.get('dummy_section','password'):
	print('DB password error!!!')
	ssh.close()
	os._exit()
war_file.close()
# check success and upload
upload_dir = config.get('remote', 'host_upload_dir')
dst = upload_dir+'/'+build_name+'.war'
Upload.upload(ssh,src,dst)

# shutdown tomcat
# get tomcat pid
tomcat_home = config.get('remote','host_tomcat_home')
cmd_tomcat_pid = 'ps aux | grep'+' '+tomcat_home+' '+'|'+ ' '+ 'grep -v \'grep\''+' '+'|'+' '+'awk \'{print $2}\''
tomcat_pid = ExecCommand.exec_command(ssh,cmd_tomcat_pid).strip()
# shutdown
if tomcat_pid:
	cmd_tomcat_shutdown = 'kill -9' + ' ' + tomcat_pid
	print(ExecCommand.exec_command(ssh,cmd_tomcat_shutdown).strip())
print('Success!!! Tomcat has been killed!')

# remove old version  
cmd_remove = 'rm -rf'+' '+tomcat_home+'/webapps/'+build_name
print(ExecCommand.exec_command(ssh,cmd_remove))

# copy new version
cmd_copy = 'cp' + ' ' + dst + ' ' + tomcat_home+'/webapps/'
print(ExecCommand.exec_command(ssh,cmd_copy))

# startup tomcat
cmd_tomcat_start = './'+tomcat_home+'/bin/startup.sh'
print(ExecCommand.exec_command(ssh.cmd_copy))

ssh.close()

# test http connection
APP_HTTP_URL = config.get('remote','app_http_url')
HttpConnectionTest.test(APP_HTTP_URL)
