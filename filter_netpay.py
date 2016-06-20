def myfilter(lines):
    for line in lines:
        line=line.decode('utf8')
        if len(line)>32 and line[32]==u'\u3010' and (line.find(u'\u62e6\u622a\u8bf7\u6c42',30,50)>=0 or line.find('userId=',30,50)>=0):
            yield line
