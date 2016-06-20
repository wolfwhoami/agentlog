def myfilter(lines):
    for line in lines:
        line=line.decode('utf8')
        if line[32:41]==u'\u5ba2\u6237\u7aef\u8bf7\u6c42\u53c2\u6570\u5982\u4e0b':
            yield line
    