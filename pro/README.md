
### scripts
+ deploy.py
(1) upload
	```~:fab -f deploy.py upload```
	This command will upload the ```project.war``` from ```gate``` to ```app```.

(2) deploy
	```~:fab -f deploy.py deploy```
	This command will deploy ```project.war```.
	Including
		stop tomcat
		remove old project(.war) in tomcat_home/webapps/
		copy new project.war to tomcat_home/webapps/
		start tomcat

+ uploadgate.py
(1) upload
	```~:fab -f uploadgate.py upload```
	This command will upload ```local files``` in ```./upload``` to ```gate```.
	1) file must in ```./upload```
	2) must config ```./upload/upload.cnf```. upload.cnf is info of the files.
	3) This command just upload files in ```gate_upload_path in gate```.

+ hotreplace.py
(1) hotreplace
	```~:fab -f hotreplace.py hotreplace```
	This command will upload files from ```gate``` to ```app``` and then copy them to ```target path``` that configured in local ```./upload/upload.cnf```. Target path can be concat from ```relatvie_path``` in upload.cnf.
	1) You must firstly use ```uploadgate.py``` upload files to gate, then you will be able to replace these files.
	2) You can use this command to upload files to ```target path on app server```

+ coldreplace.py
(1) coldreplace
	```~:fab -f coldreplace.py coldreplace```
	This command is same as hotreplace. But the command will restart tomcat after copy.

