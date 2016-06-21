def formatset(rs,fs):
    for key,value in rs.items():
        if value:
            fs=fs.replace('%'+key+'%',value)
        else:
            fs=fs.replace('%'+key+'%','')
    return fs



def myfilter(lines,args):
    for line in lines:
        line=line.decode('utf8')
        match=args['regex'].match(line)
        if match:
            rs=match.groupdict()
            yield formatset(rs,args['output'])
    