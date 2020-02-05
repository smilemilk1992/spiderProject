# -*- coding: utf-8 -*-
__author__ = 'smilemilk'
import sys, time
import datetime

def timeStamp(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def GetNowTime2():
    return time.strftime("%Y-%m-%d 00:00:00",time.localtime(time.time()))

def GetNowDate():
    return time.strftime("%Y-%m-%d",time.localtime(time.time()))


# 规整化发表时间
def regularization_time(publish_time):
    now = GetNowTime()
    if '分钟前' in publish_time: # 22分钟前
        publish_time = publish_time.replace('分钟前','')
        publish_time = time.time() - int(publish_time)*60
        publish_time = time.strftime("%Y-%m-%d %H:%M",time.localtime(publish_time))
        publish_time = publish_time +  ':00'
    if '小时前' in publish_time: # 22分钟前
        publish_time = publish_time.replace('小时前','')
        publish_time = time.time() - int(publish_time)*60*60
        publish_time = time.strftime("%Y-%m-%d %H:%M",time.localtime(publish_time))
        publish_time = publish_time +  ':00'
    elif '今天' in publish_time: # 今天 21:19
        publish_time = publish_time.replace('今天', now) + ':00'
    elif '昨天' in publish_time:
        publish_time = time.time() - 60 * 60*24
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publish_time))
    elif "天前" in publish_time:
        publish_time = publish_time.replace('天前', '')
        publish_time = time.time() - int(publish_time) * 60 * 60*24
        publish_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(publish_time))
        publish_time = publish_time + ':00'
    elif '月' in publish_time or '日' in publish_time: # 02月22日 01:07
        publish_time = publish_time.replace('月','-').replace('日','')
        publish_time = time.strftime("%Y-",time.localtime(time.time())) + publish_time + ':00'
    elif len(publish_time) == 5: # 形如14:58
        publish_time = now + " " + publish_time + ":00"
    elif len(publish_time) == 11: #形如09-29 12:38
        publish_time = time.strftime("%Y-",time.localtime(time.time())) + publish_time + ':00'
    elif len(publish_time.split("-")) and len(publish_time)<=10: #型如2019-4-12
        tm=publish_time.split("-")
        year=tm[0]
        mon = tm[1]
        day = tm[2]
        if len(mon)==1:
            mon="0"+mon
        if len(day)==1:
            day="0"+day
        publish_time=year+"-"+mon+"-"+day+" 00:00:00"
    elif len(publish_time) == 16: #形如2015-09-29 12:38
        publish_time = publish_time.replace("/","-") + ':00'
    else:
        publish_time=now
    return publish_time

print(regularization_time("昨天"))