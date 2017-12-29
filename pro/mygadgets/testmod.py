import buildhosts

host_list = ['192.168.1.1','192.168.1.2']
port_list = [22,'22']
username_list = ['admin','root']
password_list = ['admin123','root123']

hosts,passwords = buildhosts.BuildHosts(host_list,port_list,username_list,password_list)
print(hosts,passwords)
