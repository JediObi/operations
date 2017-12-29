import pexpect

def send_command(child, cmd):  
        child.sendline(cmd)  
        print(child.before.decode('utf-8'))

def send_command2(child, cmd,pwd):
	child.sendline(cmd)
	res = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
	if res ==  0:
		print("[-] Error 2")
		return
	elif res ==  1:
		print('yes')
		pwd = pwd+'\n'
		print(pwd)
		child.sendline(pwd)
	print(child.before.decode('utf-8'))

def connect(user, host, password,port):  
        ssh_newkey = 'Ary you sure you want to continue connecting'  
        connStr = 'ssh -p'+port+' ' + user + '@' + host  
        child = pexpect.spawn(connStr)  
        ''''' 
        ret = child.expect([pexpect.TIMEOUT, ssh_newkey]) 
        if ret == 0: 
                print "[-] Error 1" 
                return 
        elif ret == 1: 
                child.sendline('yes') 
        '''  
        res = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])  
        if res ==  0:  
                print("[-] Error 2")
                return  
        elif res ==  1:  
                child.sendline(password)
        return child  
def main():
	host = '139.199.148.107'
	user = 'admin'
	port='19573'
	password = 'ruihua123456'
	child = connect(user, host, password, port)
	#send_command(child, 'w')
	#send_command(child, '')
	send_command(child, 'echo test>>test2.txt')
	cmd2 = 'scp -P19573 test2.txt admin@10.88.11.11:/home/admin/admin_fc/'
	send_command2(child,cmd2,'sys-p1kKz')
	send_command(child,'exit\n')
	child.close()
main()
