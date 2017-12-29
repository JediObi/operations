# -*- coding:utf-8 -*-

import configparser
from fabric.api import *
from mygadgets import concathost
from mygadgets import buildhosts
from fabric.contrib.console import confirm

config_file = 'pro.cnf'
upload_config_file = './upload/upload.cnf'

config = configparser.ConfigParser()
config.read(config_file)


gate_host_name = config.get('remote','host_name')
gate_host_port = config.get('remote','host_port')
gate_host_username = config.get('remote','host_username')
gate_host_password = config.get('remote','host_password')
gate_host = concathost.ConcatHost(gate_host_name,gate_host_port,gate_host_username)

gate_upload_path = config.get('remote','upload_path')


config_upload = configparser.ConfigParser()
config_upload.read(upload_config_file)
file_count = config_upload.getint('upload','file_count')

# set host info
env.hosts.append(gate_host)
# add gateway host pass
env.passwords.setdefault(gate_host,gate_host_password)

# print host and pass
def test():
	print(env.hosts,env.passwords)

# upload war from gate to app
def upload():
	for i in range(file_count):
		file_src = './upload/'+config_upload.get('file'+str(i),'file_name')
		with settings(warn_only=True):
			result = put(file_src,gate_upload_path)
		if result.failed and confirm('put file failed, Y deal the error, N ignore! '+file_src):
			print('no deal')
