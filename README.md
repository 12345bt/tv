## 这是什么？

这个小工具从[「东北大学IPv6视频直播测试站」](http://hdtv.neu6.edu.cn/)爬取电影名称和播放地址，然后用电影名从豆瓣获取海报、简介以及评分，并过滤掉评分低的电影。其实就是个自带展示界面的小爬虫 :)
主要代码都在 `tvcrawler/management/commands/update_movies.py` 里面。

## 解决的问题

我这里无法访问 IPv6 网站，所以最初的目的是用 nginx 在服务器上反代一下那个网站（nginx 配置文件在 `tv.nginx` 里）；后来发现电影质量参差不齐，而且没有电影分类（科幻/喜剧）和简介，每次都要去豆瓣看看太麻烦。
当然，最主要的原因是原来的界面太难看了 :)
