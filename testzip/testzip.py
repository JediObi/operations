# -*- coding:utf-8 -*-

from zipfile import ZipFile

myzip = ZipFile('rh.zip','a')
#print('zip.namelist()')
#print(myzip.namelist())
print('zip.printdir()')
myzip.printdir()

namelist = myzip.namelist()
zout = ZipFile('rh2.zip','a')
print("")
for item in namelist:
	buffer = zin.read(item)
	if (item !='WEB-INF/classes/dbconfig'):
		zout.writestr(item,buffer)

#print('zip.write(WEB-INF/classes/dbconfig')
#myzip.extract('WEB-INF/classes/dbconfig','./test')
#myzip.write('WEB-INF/classes/dbconfig','WEB-INF/classes/dbconfig')
#print('zip.open(WEB-INF/classes/dbconfig')
#myfile = myzip.open('WEB-INF/classes/dbconfig',mode='U')
#print(myfile.read().decode('utf-8'))
#myfile.write('test')
#myfile.write('nothing')
#myfile.close()
#print('zip.writestr')
#myzip.writestr('WEB-INF/classes/dbconfig',data='nothing')
myzip.close()
