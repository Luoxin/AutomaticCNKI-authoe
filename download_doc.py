import os

from getRandom import getRandom
import url_controller
import sqlite3

from time import sleep
from selenium import webdriver

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

class download_pdf:

    def __init__(self,url_download):

        self.driver_name = 'chrome'  # 浏览器名称
        self.url_download=url_download
        self.url_will_download=url_controller.UrlControl()
        print("已获取所有下载连接")

    def save(self,url):
        sql="UPDATE download SET \"sgin\" = 1 WHERE \"url\" = \""+url+"\""
        executeSQL(sql)
        # file = open("已下载.txt", "a")
        # file.writelines(str(url) + "\n")
        # file.close()

    def _save(self,url):
        sql = "UPDATE download SET \"sgin\" = 3 WHERE \"url\" = \"" + url + "\""
        executeSQL(sql)

    def get(self):#0未下载，1已下载
        sql = "SELECT * FROM download"
        list = executeSQL(sql)
        for i in list:
            if i[1] == 1:
                self.url_will_download.add_old_url(i[0])
            else:
                self.url_will_download.add_new_url(i[0])

        # file = open("已下载.txt", "r")
        # for i in file.readlines():
        #     if i.__len__()<3:
        #         break
        #     print(i[:-1])
        #     self.url_will_download.add_old_url(i[:-1])
        # file.close()

    def download(self,url):
        self.driver.get(url)
        sleep(3)
        try:
            alert = self.driver.switch_to_alert()
            print(alert.text)
            self._save(url)
        except:
            self.save(url)


    def start(self):
        print("正在初始化下载器...")

        print("正在整理下载列表")
        self.get()
        self.url_will_download.add_new_urls(self.url_download)

        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1200, 800)
        self.driver.get("http://kns.cnki.net/kns/logindigital.aspx?ParentLocation=http://www.cnki.net")

        print("正在登陆，请稍后")
        sleep(getRandom(1, 5))

        js="login('false')"
        self.driver.execute_script(js)

        sleep(getRandom(1, 5))

        print("初始化完成，准备下载")


        count_download_url=0
        try:
            while self.url_will_download.has_new_url():
                url=self.url_will_download.get_new_url()
                count_download_url+=1
                print("正在下载第{}篇文档".format(count_download_url))

                self.download(url)
                temp_sleep = getRandom(30, 120)
                print("请耐心等待{}秒后开始下载下一篇文档".format(temp_sleep))
                sleep(temp_sleep)

                if count_download_url%20==0:
                    cmd = "move.bat"
                    p = os.popen(cmd)

        except:
            pass
        finally:
            return count_download_url



if __name__ == '__main__':
    a=download_pdf([])
    a.start()