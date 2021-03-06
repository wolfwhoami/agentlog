#coding=utf8
import os
import time
import ConfigParser
import threading
import re
import platform
import sys

#########################
#crontab -e
#1 0 * * * python agentlog.py  
#使用linux计划任务实现连续不间断监控
#########################
if platform.system()!='Windows':
    ostype=1
    import syslog
else:
    ostype=0


def isdebug():
    if len(sys.argv)>1 and sys.argv[1]=='debug':
        return True
    return False

def debugprint(dinfo):
    if isdebug():
        logfile.write("DEBUG: "+str(dinfo)+'\n')
        #print "DEBUG: "+str(dinfo)
        logfile.flush()

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
    srcpath=getreallog(args['source'])
    if srcpath.find('/opt/app/')==0:
        while (not os.path.isfile(srcpath)) and st['run']:
            time.sleep(60)
    if os.path.isfile(srcpath):
        f = open(srcpath)
        if len(sys.argv)==1 or (len(sys.argv)>=3 and sys.argv[2]=='active'):
            f.seek(0,2)
    else:
        debugprint("%s is not exist" %srcpath)
        return
    debugprint("open: "+srcpath)
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
    debugprint("close: "+srcpath)
            
def doit():
    threads=list()
    for key,value in opdict.items():
        if value.get('filter'):
            action=threading.Thread(target=threadfunc,args=(key,value,state))
            action.start()
        elif value.get('regex'):
            value['filter']='filter_regex'
            action=threading.Thread(target=threadfunc,args=(key,value,state))
            action.start()
        else:
            continue
        threads.append(action)
    return threads

 
def  waitthreads(threads):
    [t.join() for t in threads]
     
if __name__ == '__main__':
    fmap={'local1':136,'local2':144,'local3':152,'local4':160,'local5':168,'local6':176}
    mylock=threading.RLock()
    data=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    state={'run':True}
    opdict=read_conf(sys.path[0]+'/agentlog.conf').get_conf_dict()
    opdict['system']['sleep']=float(opdict['system']['sleep'])
    logfile=open(sys.path[0]+'/'+opdict['system']['log'],'a')
    debugprint(opdict)
    debugprint("Now: %s" %data)
    rss=doit()
    debugprint(threading.enumerate())    
    while 1:
        if len(threading.enumerate())== 1:
            exit(1)
        else:
            time.sleep(60)
            now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if data!=now:
                state['run']=False
                waitthreads(rss)
                debugprint("==============the process is over===============")
                
            