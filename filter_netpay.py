import os
import sys
import re


ree=re.compile(r"^\[INFO \] \S+ \S+ \S(userId\=(?P<uid>\w+),userType\=(?P<utp>\d))?\S+?uri\=(?P<url>\S+?),.*$")


def getnb(it):
    return it/255,it%255

def uid2ip(uid):
    ip1=int(uid[0])
    if ip1==4:
        ip1_1=64
    else:
        ip1_1=0
    ip2=int(uid[1:4])
    ip3=int(uid[4:7])
    ip4=int(uid[7:10])
    ip2_1,ip2=getnb(ip2)
    ip3_1,ip3=getnb(ip3)
    ip4_1,ip4=getnb(ip4)
    ip1=ip1_1+(ip2_1<<4)+(ip3_1<<2)+ip4_1
    
    return "%s.%s.%s.%s" %(ip1,ip2,ip3,ip4)

def dict2str(dt):
    if dt['uid']:
        return "%s %s %s %s" %(dt['url'],dt['uid'],dt['utp'],uid2ip(dt['uid']))
    else:
        return dt['url']
    
def myfilter(lines):
    for line in lines:
        line=line.decode('utf8')
        if len(line)>32 and line[32]==u'\u3010':
            match=ree.match(line)
            if match:
                yield dict2str(match.groupdict())