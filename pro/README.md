
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
	This command will upload files from ```local``` to ```gate```.
	1) [Local] File must be put in ```./upload```.
	2) [Local] You must config ```file_count``` and ```file_name``` in ```./upload/upload.cnf``` to figure out which files will be uploaded.
	3) [Gate] Files will be uploaded to ```gate_upload_path``` on ```gate```. You can config it in ```pro.cnf```.

+ hotreplace.py
(1) hotreplace
	```~:fab -f hotreplace.py hotreplace```
	This command will upload files from ```gate``` to ```app server```.
	1) [Local] Files you upload to ```app server``` must be uploaded from ```local``` to ```gate``` first. 
	2) [Gate] File location on ```gate``` can be configured in ```pro.cnf``` at ```gate_upload_path```. Ensure the existence of the files in this directory.
	3) [App] File name and upload path on ```app server``` must be configured in ```./upload/upload.cnf``` at ```file_name``` and ```target_path```.

+ coldreplace.py
(1) coldreplace
	```~:fab -f coldreplace.py coldreplace```
	This command will upload files from ```gate``` to ```app server```. It will stop tomcat before uploading and start it after uploading.
	1) [Local] You must upload these files from ```local``` to ```gate``` before to ```app server```.
	2) [Gate] File location on ```gate``` could be configured in ```pro.cnf``` at ```gate_upload_path```. Ensure the existence of files in this directory.
	3) [App] File name and upload path on ```app server```  must be configured in ```./upload/upload.cnf``` at ```file_name``` and ```target_path```.
	4) [App] This command will stop tomcat. You have to config the tomact home in ```pro.cnf``` at ```app_tomcat_home```.

+ downloadgate.py
(1) download
	```~:fab -f downloadgate.py download```
	This command will download files from ```gate``` to ```local```.
	1) [Gate] The file location on ```gate``` can be configured in ```pro.cnf``` at ```gate_upload_path```.
	2) [Local] File will be downloaded to ```./download```
	3) [Local] File count and name must be configured in ```./download/download.cnf```.

+ download.py
(1) download
	```~:fab -f download.py download```
	This command will download files form ```app server``` to ```gate```.
	1) [App] File location on ```app server``` must be configured in ```./download/download.cnf``` at ```target_path```. It would better be absolute path. You also need to config file name and path on app server in download.cnf.
	2) [Gate] File download path on gate can be configured in ```pro.cnf``` at ```gate_upload_path```.
	3) [Gate] File will be renamed of its original name and the server host  after downloading.
