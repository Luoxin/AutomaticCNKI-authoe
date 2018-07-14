import urllib.request


class HtmlDownloader(object):
    def download(self, new_url):
        # new_url=new_url.encode("utf-8")
        print("准备下载页面"+new_url)
        user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        headers = {'User-Agent': user_agent}
        req_timeout = 5
        request = urllib.request.Request(new_url, headers=headers)
        print(request)
        response = urllib.request.urlopen(request, None, req_timeout)  # 这里会有一个返回值 是我们的响应
        print(response.getcode())
        # 我们判断如果不是200就返回None 否则就如数据就行了
        if response.getcode() != 200:
            return None
            # 从响应中读取页面数据
        print("下载完成")
        return response.read()
        # 这里下载就完成了 那么该解析了 所以去写html的parser吧