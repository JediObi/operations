from fabric.api import *
from fabric.contrib.console import confirm

env.hosts=['admin@115.159.207.102:22']
env.passwords = {
	'admin@115.159.207.102:22':'ruihua123456',
}

def test():
	result = run('ps aux|grep /home/admin/app/apache-tomcat-8.0.36|grep -v \'grep\'|awk \'{print $2}\'')
	print('result:')
	result=result+'s'
	print(result)
	print('hello')

def testfailed():
	with settings(warn_only=True):
		result = run('rm testdir')
	if result.failed and confirm('Y do some work,N ignore!?'):
		print('deal the error...')
	print('hello')
	result = run('echo hello>>test.txt')
