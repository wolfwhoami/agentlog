import os
import sys
import re


ree=re.compile(r"^\[INFO \] \S+ \S+ \S(userId\=(?P<uid>\w+),userType\=(?P<utp>\d))?\S+?uri\=(?P<url>\S+?),.*$")


def uid2ip(uid):
    return "%s.%s.%s.%s" %(uid[0],uid[1:4],uid[4:7],uid[7:10])

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