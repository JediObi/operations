# -*-coding:utf-8 -*-

import os

def package(project_dir):
	
	cmd = 'mvn -f'+' '+project_dir+'/pom.xml'+' '+'clean compile install -DskipTests'
	print('Running command:',cmd)
	os.system(cmd)
	print('Package success!!')
