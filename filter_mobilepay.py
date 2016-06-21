import os
import sys
import re

ree=re.compile(r"^\[INFO \] \S+ \S+ \S+?>{10}:(?P<dst>\S+?)(?P<url>\/\S+).*$")


def dict2str(dt):    
    return "%s %s" %(dt['url'],dt['dst'])
    
def myfilter(lines):
    for line in lines:
        line=line.decode('utf8')
        if line[:5]=='[INFO':
            match=ree.match(line)
            if match:
                yield dict2str(match.groupdict())