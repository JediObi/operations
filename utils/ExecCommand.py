# -*- coding:utf-8 -*-

def exec_command(SSHClient, command)
	stdin, stdout, stderr = SSHClient.exec_command(command)
	
	err_list = stderr.readlines()
	if len(err_list) > 0:
		print('ssh execute remote command [%s] error:%s'%(command, err_list[0]))
	return stdout.read().decode('utf-8')
