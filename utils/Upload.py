# -*- coding:utf-8 -*-

import os

def upload(SSHClient,src,dst):
	
	try:
		sftp = SSHClient.open_sftp()
	except Exception as e:
		print('open sftp failed:', e)
		os._exit(0)
	
	try:
		print('uploading file: %s --> %s'%(src, dst))
		sftp.put(src, dst)
		print('uploading success!!!')
		sftp.close()
	except Exception as e:
		print('uploading failed:', e)
		os._exit(0)	
