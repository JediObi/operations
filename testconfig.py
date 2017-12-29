# -*- coding:utf-8 -*-

import configparser
from zipfile import ZipFile

config = configparser.ConfigParser()
# config.read('rh.cnf')

war_file = ZipFile('rh.war','r')
dbconfig_file = war_file.open('WEB-INF/classes/dbconfig.properties','r')
dbconfig = '[dummy_section]\n'+dbconfig_file.read().decode('utf-8')
#print(dbconfig)
#for line in dbconfig_file:
#	if(not(line.decode('utf-8').startswith('#'))):
#		print(line.decode('utf-8'))

config.read_string(dbconfig)
#print(config.get('""','IP'))
print(config.items('dummy_section'))
#sections=config.sections()
#print(len(sections))
dbconfig_file.close()
war_file.close()

config2 = configparser.ConfigParser()
config2.read('rh.cnf')
db_type_std = config2.get('remote','db_type')
db_type = config.get('dummy_section','dbtype')


#dbconfig_std = config.get('remote','dbconfig')
