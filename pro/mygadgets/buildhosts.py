# -*- coding:utf-8 -*-

import sys
sys.path.append('../')
from mygadgets import concathost

def BuildHosts(host_list,port_list,username_list,password_list):
	length = len(host_list)
	hosts = []
	passwords = {}
	for i in range(length):
		hosts.append(concathost.ConcatHost(host_list[i],port_list[i],username_list[i]))
		passwords.setdefault(hosts[i],password_list[i])	
	return hosts,passwords
