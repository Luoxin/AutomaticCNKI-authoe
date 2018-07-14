# coding:utf-8
from bs4 import BeautifulSoup
import re
from urllib import parse

class HtmlParser(object):
    def parse(self, new_url, html_content):
        print("正在分析页面....")

        soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
        new_urls_search = self.get_new_urls_search(new_url, soup)

        new_urls_download,new_urls_get_url = self.get_new_urls_download( soup)
        print("分析完成，正在整理结果")
        return new_urls_search,new_urls_download,new_urls_get_url

    def get_new_urls_search(self, page_url, soup):
        new_urls = set()  # 定义集合 用于存新urls的
        links = soup.find_all("a", href=re.compile(r"^Search\.aspx\?q=author[\s\S]+&rank=relevant&cluster=all&val=&p=\d+$"))
        for link in links:
            part_url = link["href"]
            print(str(part_url))
            new_full_url = parse.urljoin(page_url,part_url)
            new_urls.add(new_full_url)
        return new_urls


    def get_new_urls_download(self,  soup):
        new_urls = set()  # 定义集合 用于存新urls的
        new_urls_get_url=set()
        #可以直接下载的连接
        links = soup.find_all("a",href=re.compile(r"^http\:\/\/search\.cnki\.net\/down\/default\.aspx\?filename=[\s\S]+&dbcode=CJFD&year=[\d]{4}&dflag=[\s\S]+$"))
        for link in links:
            part_url = link["href"]
            print(str(part_url))
            new_urls.add(part_url)

        print("查找顽固连接......")

        links = soup.find_all("a", href=re.compile(r"^http\:\/\/epub\.cnki\.net\/grid2008\/brief\/detailj\.aspx\?filename=[\s\S]+&dbname=[\s\S]+$"))
        count={}
        for link in links:
            part_url = link["href"]
            print(part_url)
            if part_url not in count.keys():
                count[part_url]=link
            else:
                print("发现顽固页面！")
                new_urls_get_url.add(count[part_url])



        return new_urls,new_urls_get_url