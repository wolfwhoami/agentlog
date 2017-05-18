# agentlog v.1.3
### author:yixuanzi
### date: 2016-6-3
### email: yeying0311@126.com
一个日志处理转发工具，用于日志清洗后集中管理

### 通过配置agentlog.conf实现对源数据日志进行正则清洗取出关键数据后通过syslog转发或文件输出
```
[system]
sleep=1
log=agent.log

[test]
name=test
regex=\S+ \S+ \S+ \S+ \S+ (userId\=(?P<uid>\d+),userType\=(?P<utp>\d))?\S+?uri\=(?P<url>\S+?),
output=%url% %uid% %utp% this is a test
source=x:/t.txt
facility=local3

[netpay]
name=netpay
source=/xxxx
filter=filter_netpay
facility=local1

[mobilepay]
name=mobilepay
source=/xxxx
filter=filter_mobilepay
facility=local2
```
