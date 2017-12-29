# -*- coding:utf-8 -*-

import paramiko
import configparser
import os

hostname_ = ''
port_ = ''
username_ = ''
password_ = ''
ssh = ''

config = configparser.ConfigParser()
config.read('pro.cnf')

hostname_ = config.get('remote','host_name')
port_ = config.get('remote','host_port')
username_ = config.get('remote','host_username')
password_ = config.get('remote','host_password')

try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	ssh.connect(hostname=hostname_, username=username_, port=port_, password=password_)
	print('ssh %s@%s success!!!'%(username_,hostname_))
except Exception as e:
	print('ssh %s@%s failed! $s'%(username_,hostname_, e))
	os._exit(0)

cmd1 = 'echo hello>>admin_fc/test.txt'
def exec_command(SSHClient, command):
	stdin, stdout, stderr = SSHClient.exec_command(command)
	
	err_list = stderr.readlines()
	if len(err_list) > 0:
		print('ssh execute remote command [%s] error: %s'%(command,err_list[0]))
	return stdout.read().decode('utf-8')
def exec_command_pwd(SSHClient, command, pwd):
	
	stdin, stdout, stderr = SSHClient.exec_command(command)
	
	#stdin, stdout, stderr = SSHClient.exec_command(pwd)
	err_list = stderr.readlines()
	if len(err_list) > 0:
		print('error! %s'%(err_list[0]))
	#stdin.write(pwd)
	#stdin.flush()
	return stdout.read().decode('utf-8')
print(exec_command(ssh,'echo hello>>test3.txt'))
cmd2 = 'scp -P19573 test2.txt admin@10.88.11.11:/home/admin/admin_fc/'
print(exec_command_pwd(ssh,cmd2,'sys-p1kKz'))

ssh.close()
