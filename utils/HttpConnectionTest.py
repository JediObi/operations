# -*- coding:utf-8 -*-

import urllib
import urllib.request

def test(http_url):
	print('stat connecting', http_url, '...')
	response = urllib.request.urlopen(http_url)
	print('connection', http_url,'http code:',response.getcode())
	if(response.getcode()==200):
		print('Connect Success!')
	else:
		print('Connect Failed!')
