# -*- coding: utf-8 -*-
import requests
from V1.LOG_CFG.logHelp import *
from scrapy.selector import Selector
from concurrent.futures import ThreadPoolExecutor
from V1.pipelines.DownPipeline import *
import time
class csdnSpider(object):
    def __init__(self,start_url):
        self.LogUtil = LogUtil() #日志配置文件
        self.LOG = self.LogUtil.getLogger(self.__class__.__name__)  # 用当前类名
        self.start_url=start_url
        self.db = spidersPipeline()
        self.page=1

    def main(self,url):
        response = self.getXpath(url)
        if not response:
            self.LOG.info("程序出现错误，直接退出！")
            return
        lis=response.xpath("//div[@class='article-item-box csdn-tracking-statistics']").extract()
        with ThreadPoolExecutor(max_workers=3) as executor:  # 多线程 线程数为3
            for li in lis:
                item={}
                li = Selector(text=li)
                link=li.xpath("//h4/a/@href").extract()[0]  #链接
                title=li.xpath("//h4/a//text()").extract()[-1].strip() #标题
                Num= li.xpath("//span[@class='read-num']/span[@class='num']/text()").extract()
                readNum=Num[0] #阅读数
                commentNum=Num[1] #评论数
                publishTime=li.xpath("//span[@class='date']/text()").extract()[0].strip() #发布时间
                item["link"]=link
                item["title"]=title
                item["readNum"]=readNum
                item["commentNum"]=commentNum
                item["publishTime"]=publishTime
                executor.submit(self.getContent, item)
        if lis: #翻页 (盲翻)
            self.page=self.page+1
            next_url=self.start_url+"/article/list/{}".format(self.page)
            self.LOG.info("翻页：{} nextUrl：{}".format(self.page,next_url))
            print(next_url)
            self.main(next_url)



    def getContent(self,item):
        link=item["link"]
        response = self.getXpath(link)
        html=response.xpath("//div[@id='content_views']").extract()[0]
        item["content"]=html
        item["table"]="p_news_csdn"
        item["created_at"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.LOG.info(item) #打印日志
        self.db.process_item(item) #入mysql

    def getXpath(self,link):
        try:
            rs = requests.get(link)
            response = Selector(text=rs.text)
            return response
        except Exception as e:
            self.LOG.error("解析网页出错 url={} e={}".format(link,e))
        return ""


if __name__ == '__main__':
    start_url="https://blog.csdn.net/forezp"
    csdn=csdnSpider(start_url)
    csdn.main(start_url)