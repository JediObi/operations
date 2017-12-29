from fabric.api import *

env.gateway='admin@139.199.148.107:19573'

env.hosts=['admin@10.88.11.11:19573']
env.passwords={
	'admin@10.88.11.11:19573':'sys-p1kKz',
	'admin@139.199.148.107:19573':'ruihua123456',
}
def pack():
	local('mvn -f /media/fc/doc/testlog4j/pom.xml clean compile install -DskipTests')

def upload():
	#with settings(warn_only=True):
	#	result = put('/home/admin/test.txt','/home/admin/admin_fc/')	
	run('echo today>>test4.txt')
def shell():
	open_shell(env.hosots)
