# -*- coding:UTF-8 -*-
import requests, json, time, sys
from contextlib import closing

class get_photos(object):

    def __init__(self):
        self.photos_id = []
        # 每张图片的下载URL
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=true'
        # 主页URL，每一页有12张图片，XXX代表第几页
        self.target = 'https://unsplash.com/napi/photos?xxx&per_page=12'
        # self.headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

    """
    函数说明:循环获取每一页的所有图片的id
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """
    def get_ids(self, page):
        # req = requests.get(url=self.target, headers=self.headers, verify=False)
        for i in range(1, page+1):
            self.target = self.target.replace('xxx', str(i))
            req = requests.get(url=self.target, headers=self.headers, verify=False)
            # 响应是JSON格式的字符串，转换为python内置的基本数据类型
            html = json.loads(req.text)
            for each in html:
                self.photos_id.append(each['id'])
            # 每一页之间停顿一秒，拟人化
            time.sleep(1)


    """
    函数说明:给定每一张图片的id, 然后下载
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """
    def download(self, photo_id, filename):
        # 每张图片的下载URL
        target = self.download_server.replace('xxx', photo_id)
        # 将每张图片分别存为.jpg文件
        with closing(requests.get(url=target, stream=True, verify = False, headers = self.headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == '__main__':
    gp = get_photos()
    print('获取图片链接中:')
    page = int(input('请输入要下载的页数：'))
    gp.get_ids(page)
    print('图片下载中:')
    for i in range(len(gp.photos_id)):
        print('  正在下载第%d张图片' % (i+1))
        gp.download(gp.photos_id[i], (i+1))
    print('图片下载完成')
