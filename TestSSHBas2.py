# -*- coding:utf-8 -*-

#import paramiko
import configparser
import os
import pexpect

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

PROMPT = ['#','$','>','\$','>>>']
ip = 'ssh '+username_+'@'+hostname_+' -p '+port_

def connect(host,user,port,password):
	login_command = 'ssh -l -p '+port+' '+user+' '+host
	ssh = pexpect.spawn(login_command)
	res = ssh.expect(['Are you sure you want to continue connecting (yes/no)?', '[P|p]assword:',pexpect.TIMEOUT]+PROMPT)
	if res == 0:
		print('error')
		return
	if res == 1:
		ssh.sendline('yes')
		res = ssh.expect([pexpect.TIMEOUT,'[P|p]assword:'])
		if res == 0:
			print('error')
			return
		if res == 1:
			ssh.sendline(password)
			ssh.expect(PROMPT)
			print(ssh.before)
			return
	if res == 2:
		ssh.sendline(password)
		ssh.expect(PROMPT)
		print(ssh.before)
		return
	ssh.sendline(password)
	#ssh.sendline('ls -l -h')
	#ssh.sendline('echo hello>>test.txt')
	#res = ssh.read()
	#print(res)
	#ssh.sendline('exit')
	#print(ssh.before)
	#ssh.interact()
	#print('ssh %s@%s success!!!'%(username_,hostname_))
	return ssh

def exec_command(sshclient, command):
	sshclient.sendline(command)
	sshclient.expect(PROMPT)
	print(sshclient.before)

ssh = connect(hostname_,username_,port_,password_)
cmd1 = 'echo test>>test2.txt'
exec_command(ssh,cmd1)
#cmd1 = 'ls -l -h'
#ssh.sendline(cmd1)
#res = ssh.read()
#print(res)

#ssh.close()
