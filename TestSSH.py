# -*- coding:utf8 -*-

import paramiko
import os

hostname_ = '115.159.207.102'
port_ = 22
username_ = 'admin'
password_ = 'ruihua123456'
ssh = ''

try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	ssh.connect(hostname=hostname_, username=username_, port=port_, password=password_)
	print('ssh %s@%s success!!'%(username_, hostname_))
except Exception as e:
	print('ssh %s@%s failed!!%s'%(username_, hostname_, e))
	os._exit(0)

# execute command
def exec_command(sshClient, command):
	stdin, stdout, stderr = sshClient.exec_command(command)
	
	err_list = stderr.readlines()
	if len(err_list)>0:
		print('ssh exec remote command [%s] error:%s'%(command, err_list[0]))
	#print(stdout.read().decode('utf-8'))
	return stdout.read().decode('utf-8')

# exec_command(ssh,'cd /home/fc')
# exec_command(ssh,'echo testa>>a.txt')
# exec_command(ssh,'exit')
tomcat_pid = exec_command(ssh,'ps aux|grep "/home/admin/app/apache-tomcat-8.0.36"|grep -v "grep"| awk \'{print $2}\' ').strip()
print(tomcat_pid,'a')
if tomcat_pid:
	cmd_shutdown=

exec_command(ssh,'ls | grep tar')
# exec_command(ssh,'hist')
ssh.close()
