def myfilter(lines,ree):
    for line in lines:
        line=line.decode('utf8')
        if ree.match(line):
            yield line
    