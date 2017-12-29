#from mygadgets import concathost
#from mygadgets import buildhosts
from mygadgets import buildhosts
#print(concathost.ConcatHost('11',22,'admin'))
hosts,passwords = buildhosts.BuildHosts(['127.0.0.1'],['22'],['admin'],['admin123'])
print(hosts,passwords)
