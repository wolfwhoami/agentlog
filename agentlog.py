import os
import time
import ConfigParser
import threading
import re
import platform
import sys

if platform.system()!='Windows':
    ostype=1
    import syslog
else:
    ostype=0

fmap={'local1':136,'local2':144,'local3':152,'local4':160,'local5':168,'local6':176}
mylock=threading.RLock()
data=time.strftime('%Y-%m-%d',time.localtime(time.time()))
state={'run':True}

class read_conf(object):
    def __init__(self, config_file):
        self.config_file = config_file
    def get_conf_dict(self):
        conf = ConfigParser.RawConfigParser()
        conf.read(self.config_file)
        option_dict = {}
        secs = conf.sections()
        for sec in secs:
            option_dict[sec] = {}
            for option in  conf.options(sec):
                key = option
                value = conf.get(sec,key)
                if key=='regex':
                    value=re.compile(value)
                option_dict[sec][key] = value
        return option_dict


def mylog(name,facility,msg):
    mylock.acquire()
    msg=msg.strip()
    if ostype:
        syslog.openlog(name,syslog.LOG_PID,facility)
        syslog.syslog(msg.encode('utf8'))
    if len(sys.argv)>1 and sys.argv[1]=='print':    
        print name,facility,msg
    mylock.release()
    
def getreallog(source):
    source=source.replace('[data]',data)
    return source

def threadfunc(key,args,st):
    args['source']=getreallog(args['source'])
    if os.path.isfile(args['source']):
        f = open(args['source'])
        if len(sys.argv)==1 or (len(sys.argv)>=3 and sys.argv[2]=='active'):
            f.seek(0,2)
    else:
        print "%s is not exist" %args['source']
        return
    myfilter=__import__(args['filter'])
    while st['run']:
        lines = f.readlines()
        if args.get('regex'):
            lines=myfilter.myfilter(lines,args)
        else:
            lines=myfilter.myfilter(lines)
        if lines:
            [mylog(args['name'],fmap[args['facility']],line) for line in lines]
        time.sleep(opdict['system']['sleep'])
            
def doit():
    for key,value in opdict.items():
        if value.get('filter'):
            action=threading.Thread(target=threadfunc,args=(key,value,state))
            action.start()
        elif value.get('regex'):
            value['filter']='filter_regex'
            action=threading.Thread(target=threadfunc,args=(key,value,state))
            action.start()
        
if __name__ == '__main__':
    opdict=read_conf('agentlog.conf').get_conf_dict()
    opdict['system']['sleep']=int(opdict['system']['sleep'])
    doit()
    while 1:
        if len(threading.enumerate())== 1:
            exit(1)
        else:
            time.sleep(60)
            now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if data!=now:
                data=now
                state['run']=False
                time.sleep(opdict['system']['sleep']*2)
                state['run']=True
                doit()
                
            