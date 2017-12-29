# -*- coding:utf-8 -*-

import paramiko
import os
import time
import sys
import configparser
import urllib
import urllib.request

from utils import SSHConnection

class Deploy:
	
	__config_file = ''

	def __init__ (self, config_file):
		self.__config_file = config_file

	def deploy(self):
		start = int(round(time.time()*1000))
		
		CONFIG_SECTIONS_GLOBAL = 'global'
		CONFIG_SECTIONS_LOCAL = 'local'
		CONFIG_SECTIONS_REMOTE = 'remote'

		NOW = time.strftime('%Y%m%d_%H%M%S')
		
		print('loading config file:', self.__config_file)
		config = configparser.ConfigParser()
		config.read(self.__config_file)
		print('loading success')

		# global
		PROJECT_NAME = config.get(CONFIG_SECTIONS_GLOBAL, 'project_name')
		SRC = LOCAL_PROJECT_DIR + '/target/rh.war'

		# remote
		REMOTE_HOSTNAME = config.get(CONFIG_SECTIONS_REMOTE, 'hostname')
		REMOTE_PORT = config.getint(CONFIG_SECTIONS_REMOTE, 'port')
		REMOTE_USERNAME = config.get(CONFIG_SECTION_REMOTE, 'username')
		REMOTE_PASSWORD = config.get(CONFIG_SECTIONS_REMOTE, 'pasword')

		REMOTE_DB_USERNAME = config.get(CONFIG_SECTION_REMOTE, 'db_username')
		REMOTE_DB_PASSWORD = config.get(CONFIG_SECTION_REMOTE, 'db_password')
		REMOTE_DB_PORT = config.get(CONFIG_SECTION_REMOTE, 'db_port')
		REMOTE_DB_NAME = config.get(CONFIG_SECTIONS_REMOTE, 'db_name')
		
		TMP_DIR = config.get(CONFIG_SECTIONS_REMOTE, 'tmp_dir')
		BAK_DIR = config.get(CONFIG_SECTIONS_REMOTE, 'bak_dir')
		BAK_DB_DIR = BAK_DIR + '/db'
		BAK_APP_DIR = BAK_DIR + '/app'

		TOMCAT_HOME = config.get(CONFIG_SECTIONS_REMOTE, 'tomcat_home')
		APP_TEST_URL = config.get(CONFIG_SECTIONS_REMOTE, 'app_test_url')
		
		KEY_MAVEN_HOME = 'MAVEN_HOME'
		MAVEN_HOME = os.getenv(KEY_MAVEN_HOME)

		if (MAVEN_HOME == None):
			print('No environment['+KEY_MAVEN_HOME+']')
			os._exit(0)
		
		# mvn package
		cmd = MAVEN_HOME + '/bin/mvn -f' + LOCAL_PROJECT_DIR + '/pom.xml clean compile install -DskipTests'
		print('running local command:', cmd)
		os.system(cmd)
		print('Maven package success, file path:',SRC)

		# remote connection
		ssh = SSHConnection.SSHConnection(REMOTE_HOSTNAME,REMOTE_PORT,REMOTE_USERNAME,REMOTE_PASSWORD)
		ssh.SSHClient()
		
		# upload war
		ssh.upload(SRC, TMP_DIR+'/rh.war')
		
		# backup db
		print('backup database...')
		ssh.exec_commad('mysqldump -u'+REMOTE_DB_USERNAME+' -p"'+REMOTE_DB_PASSWORD+'" -P'+REMOTE_DB_PORT+' '+ REMOTE_DB_NAME+' > '+BAK_DB_DIR+'/'+NOW+'.sql')
		print('backup db success')

		# shutdown tomcat
		print('stop tomcat')
