import re
ree=re.compile(r"^\w{3} \d{2} \d{2}:\d{2}:\d{2} (?P<ip>[\w\.]+) netpay\[\d+\]: (userId=(?P<uid>\w+),userType=(?P<utp>\d))?\[[\u4e00-\u9fa5]+uri=(?P<url>[\/-\w\.]+),.*$")

def myfilter(lines):
    for line in lines:
        line=line.decode('utf8')
        #
        if len(line)>32 and line[32]==u'\u3010':
            match=ree.match(line)
            yield line[33:-2]
