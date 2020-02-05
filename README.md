#爬虫学习项目 V1.0

# 主要模块说明
* V1(项目一)
    * CSDN（主函数)
    * util（工具类）
    * LOG_CFG (日志模块)
    * pipeline （入库模块)

# 项目一
* CSDN博客数据
    * 网站：https://blog.csdn.net/forezp
    * 字段需求
        * 标题  （String）
        * 发布时间 (yyyy-mm-dd hh:mm:ss)
        * 文章内容（html）  （String）
        * 阅读数  (Int)
        * 评论数  (Int)
        * 入库时间  (yyyy-mm-dd hh:mm:ss)

## 环境
* python3
* bs4
* requests

## 程序启动
* CSDN
    * python run.py

## 启动器注意事项
* 配置setting文件（数据库等信息）

## 数据库表
```mysql
CREATE TABLE `p_news_csdn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(400) NOT NULL COMMENT '链接',
  `title` varchar(400) NOT NULL COMMENT '标题',
  `readNum` varchar(50) NOT NULL COMMENT '阅读数',
  `commentNum` varchar(50) DEFAULT NULL COMMENT '评论数',
  `content` longtext COMMENT '内容html',
  `publishTime` varchar(300) DEFAULT NULL COMMENT '发布时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  KEY `index_title` (`title`),
  KEY `index_link` (`link`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```


