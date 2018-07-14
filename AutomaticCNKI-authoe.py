
'''
第一次测试版本
'''
from time import sleep
import sqlite3
import sys

import download_html
import url_controller
import html_analyze
from getRandom import getRandom
import download_doc


import urllib.parse

def executeSQL(*args):
    conn = sqlite3.connect("CNKI.db")
    cursor = conn.cursor()
    if args.__len__()==2:
        re = cursor.execute(args[0], args[1])
        re=re.fetchall()
    elif args.__len__()==1:
        re=cursor.execute(args[0])
        re=re.fetchall()
    else:
        re=False
    conn.commit()
    cursor.close()
    conn.close()

    return re

class CNKI:
    def __init__(self,author):
        print("正在初始化......")
        self.search_1="http://search.cnki.net/search.aspx?q=author:"
        self.search_2="&cluster=all&val="

        self.authors=author
        print("已获取作者列表")

        self.url_search=url_controller.UrlControl()#存储获取下载连接的搜索页面
        self.url_download=url_controller.UrlControl()#存储下载连接
        self.url_download_again=url_controller.UrlControl()#存储顽固连接
        self.download_html = download_html.HtmlDownloader()
        self.html_analyze=html_analyze.HtmlParser()
        self.download_html = download_html.HtmlDownloader()

        print("初始化存储器成功")

        self.download="http://search.cnki.net/down/default.aspx?filename=GXJJ201510018&dbcode=CJFD&year=2015&dflag=pdfdown"

        self.heads={'Cookie':'cnkiUserKey=51b05509-5b1d-356a-ad32-9375d09a50a3; UM_distinctid=164944c5b6d0-08e2238e256be1'
                             '-47e1039-144000-164944c5b6e253; Ecp_ClientId=5180713234402853601; LID=WEEvREcwSlJHSldRa1Fhb09'
                             'jSnZqckVUWXFsQkpuTHBoT0wxdXc5Vm51ST0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!'
                             '; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"db0187","ShowName":"%e9%bb%91%e9%be%99%e'
                             '6%b1%9f%e5%a4%a7%e5%ad%a6%e5%9b%be%e4%b9%a6%e9%a6%86","UserType":"bk","r":"vxm3Es"}; '
                             'Ecp_session=1; SID=91005; c_m_expire=2018-07-14 06:56:38',
                    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}


    def save(self):
        file=open("顽固页面.txt","w")
        while self.url_download_again.has_new_url():
            s=str(self.url_download_again.get_new_url())
            # print(s)
            file.writelines(s+"\n")

        file.close()


    def start(self):
        count_author=0
        for author in self.authors:
            count_author+=1
            print("正在准备第{}个作者".format(count_author))

            # author = urllib.parse.quote(author)  # 作者名
            search = self.search_1 + str(urllib.parse.quote(author)) + self.search_2  # 查找连接

            self.url_search.add_new_url(search)#第一个搜索页面

            print("以对第{}个作者的信息转码".format(count_author))

            count_search=0
            while self.url_search.has_new_url():#获取下载连接
                count_search+=1
                new_url = self.url_search.get_new_url()
                print("准备收集第{}个作者的第{}个文件列表".format(count_author,count_search))


                html_content = self.download_html.download(new_url)
                # print(html_content)
                urls_search,urls_download,new_urls_get_url=self.html_analyze.parse(new_url,html_content)

                self.url_search.add_new_urls(urls_search)
                self.url_download.add_new_urls(urls_download)
                self.url_download_again.add_new_urls(new_urls_get_url)

                print("第{}个作者的第{}个文件列表整理完成，获得如下数据：\n搜索页面：\n{}\n待下载文件链接：\n{}\n顽固页面：\n{}\n".format
                      (count_author,count_search,urls_search,urls_download,new_urls_get_url))
                # print(urls_search)
                # print(urls_download)
                # print(new_urls_get_url)

                # self.save()

                temp_sleep=getRandom(20,60)
                print("请耐心等待{}秒，以应对知网的反爬检测({})".format(temp_sleep,author))
                sleep(temp_sleep)

            temp_sleep = getRandom(20, 60)
            print("第{}个作者的所有文件列表已获取完成,请闹心等待{}秒后，进行下一作者的搜索".format(count_author,temp_sleep))
            sleep(temp_sleep)

        print("所有作者的论文下载地址已获取完毕")

        print("正在格式化下载地址")
        url_download=[]
        while self.url_download.has_new_url():
            url_download.append(self.url_download.get_new_url())
        print("格式化完毕，即将启动下载程序")

        #存储已经爬取过的作者
        sql = "insert into author values (?)"
        for i in self.authors:
            try:
                pare =(i,)
                executeSQL(sql,pare)
            except:
                pass

        sql = "insert into download values (?,?)"
        for i in url_download:
            try:
                pare = (i,0)
                executeSQL(sql, pare)
            except:
                pass

        self.download_doc=download_doc.download_pdf(url_download)
        num=self.download_doc.start()

        print("下载完成,共计下载{}篇文档,由于技术限制，顽固文档链接将为您保存".format(num))

        self.save()

        print("保存完毕，正在为您退出系统")



if __name__ == '__main__':
    if sys.argv.__len__()>1:
        authors=sys.argv[1:]
    # authors=["王思斌"]
    else:
        file = open("author.txt", "r")
        authors = []
        for i in file.readlines():
            if i.__len__() > 1:
                authors.append(i[:-1])
        file.close()
    print(authors)
    a=CNKI(authors)
    a.start()





