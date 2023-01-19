# coding=utf-8
"""异步下载大文件"""

import asyncio
import sys
import traceback

import aiofiles
import aiohttp
from collections import OrderedDict
import os
import requests
import time

from Code.Log import print_


class Download:
    def __init__(self) -> None:
        super(Download, self).__init__()

    def download(self, url, path, parh_cache, ProgressGetModule_=None, SectionSize=4194304):
        self.parh_cache = parh_cache
        self.url = url
        self.path = path
        self.ProgressGetModule_ = ProgressGetModule_
        self.SectionSize = SectionSize
        # 先检查文件大小
        headers={
            "Accept-Encoding": "identity",
            'session':'JSESSIONID',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        r=requests.get(url,stream=True,headers=headers)
        file_size_str_=r.headers['Content-Length'] #提取出来的是个数字str
        self.file_size_str = int(file_size_str_)
        self.file_size_str_MB = int(file_size_str_)//1024/1024
        print(self.file_size_str_MB)
        print(self.file_size_str)

        if self.file_size_str_MB >= 0.2:
            # 如果大于0.2MB 就分段异步下载
             
            self.new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.new_loop)
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.Download_Subsection_Start_Start())
        else:
            r = requests.get(url,stream=True)
            with open(path, 'wb') as fb:
                fb.write(r.content)
               
    async def Download_Subsection_Start_Start(self):
        # 启动用来批量启动协程的协程
        t = time.time()  # 获取时间
        print(t)
        self.parh_cache_ = os.path.join(self.parh_cache,str(t))  # 缓存路径
        file_size_str_l = 0
        file_size_str_l_to = 0
        Download_Number = -1
        # self.Download_Subsection = {}
        self.Download_Subsection_ = []
        self.Download_Subsection__ = []
        self.N_Ok = 0
        self.error_quantity = 0
        while True:
            # file_size_str_l 和 file_size_str_l_to：从…下载到……
            if file_size_str_l < self.file_size_str:
                Download_Number += 1  # 次数加一(用于拼接缓存目录)
                if Download_Number == 0:
                    # 如果是第一次 那么就将开始值设为0
                    file_size_str_l = 0
                else:
                    file_size_str_l = int(file_size_str_l_to)
                    file_size_str_l += 1
                file_size_str_l_to = file_size_str_l+ self.SectionSize
                if file_size_str_l < self.file_size_str:
                    if file_size_str_l_to < self.file_size_str:
                        pass
                    else:
                        # 如果超过了文件大小 就改成最大
                        file_size_str_l_to = self.file_size_str
                    file = os.path.join(self.parh_cache_,str(Download_Number) + '.MOS_Download')
                    if file_size_str_l == file_size_str_l_to:
                        pass
                    else:
                        a = {
                            'Download_Number': Download_Number,  # 下载次数
                            'size_star': file_size_str_l,  # 从……开始
                            'size_to': file_size_str_l_to, # 下载到……
                            'file': file  # 缓存到……
                        }
                    
                        self.Download_Subsection_.append(
                            asyncio.ensure_future(self.Download_Subsection(a))
                            )
            else:
                print(self.Download_Subsection)
                break
        self.ProgressGetModule(['start',len(self.Download_Subsection_)])
        await asyncio.wait([self.Download_Subsection_Start()])
    
    async def Download_Subsection_Start(self):
        async def Cheak():
            await asyncio.wait(self.Download_Subsection_)
            # 检查是否完全完成
            Download_Subsection = list(OrderedDict.fromkeys(self.Download_Subsection_))
            print(Download_Subsection)
            Download_Subsection.remove(None)
            print(Download_Subsection)
            if len(Download_Subsection) != 0:
                print('没有全部完成')
                # await asyncio.wait([Cheak()])
            else:
                print('ooooookkk')
                await asyncio.wait([CombinationFile()])
        async def CombinationFile():
            B = []
            for file_ in os.listdir(self.parh_cache_):
                if os.path.isdir(os.path.join(self.parh_cache_,file_)) == False:
                    file__ = file_.split('.MOS_Download')[0]  # 存储编号
                    B.append(file__)
            print(B)
            B.sort(key=int)  # 排序
            print(B)
            for file_ in B:
                file = os.path.join(self.parh_cache_,file_)  # 缓存文件目录
                file_1 = file + '.MOS_Download'
                with open(file_1, 'rb') as f:
                    r = f.read()
                    with open(self.path, 'ab') as f_1:
                        f_1.write(r)

        await asyncio.wait([Cheak()])
        
        
    
    async def Download_Subsection(self,Download_Subsection):
        print(Download_Subsection)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        headers['Range'] = 'bytes=' + str(Download_Subsection['size_star']) + '-' + str(Download_Subsection['size_to'])
        print(headers)
        # 重试5次
        while True:
            try:
                os.makedirs(self.parh_cache_, exist_ok=True)
                async with aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(connect=3)) as session:
                    async with session.get(self.url, headers=headers, ssl=False, timeout=4) as response:
                        async with aiofiles.open(Download_Subsection['file'], 'wb') as f:
                            await f.write(await response.content.read())

                    self.Download_Subsection_[Download_Subsection['Download_Number']] = None
                    print(self.Download_Subsection_)
                    break

            except aiohttp.client_exceptions.ClientConnectorError:
                print('客户端链接错误'+str(self.error_quantity))
                if self.error_quantity >= 5:
                    print('出现客户端网络错误,正在取消')
                    print_('DeBug', '由于Jar文件下载出错,正在取消安装')
                    self.D_cancel()
                    ErrorKind = sys.exc_info()[1]
                    ErrorCause = '未接入互联网'
                    ErrorInfo = traceback.format_exc()
                    print_('Error', '在下载游戏Jar时出现异常,配置信息:' + str(list))
                    self.ProgressGetModule(['error', ErrorKind, ErrorCause, ErrorInfo])
                else:
                    self.error_quantity += 1
                    await asyncio.sleep(2)
            except aiohttp.client_exceptions.ClientPayloadError:
                print('客户端网络错误'+str(self.error_quantity))
                if self.error_quantity >= 5:
                    print('出现客户端网络错误,正在取消')
                    print_('DeBug', '由于Jar文件下载出错,正在取消安装')
                    self.D_cancel()
                    ErrorKind = sys.exc_info()[1]
                    ErrorCause = '未接入互联网'
                    ErrorInfo = traceback.format_exc()
                    print_('Error', '在下载游戏Jar时出现异常,配置信息:' + str(list))
                    self.ProgressGetModule(['error', ErrorKind, ErrorCause, ErrorInfo])
                else:
                    self.error_quantity += 1
                    await asyncio.sleep(2)
            except aiohttp.client_exceptions.ServerTimeoutError:
                print('error_ServerTimeoutError')
                await asyncio.sleep(2)
            except aiohttp.client_exceptions.ServerDisconnectedError:
                print('error_ServerDisconnectedError')
                await asyncio.sleep(2)
            except aiohttp.client_exceptions.ClientOSError:
                print('error_ClientOSError')
                await asyncio.sleep(2)
            except asyncio.exceptions.CancelledError:
                print('error_CancelledError')
                await asyncio.sleep(2)
            except asyncio.exceptions.TimeoutError:
                print('error_TimeoutError')
                await asyncio.sleep(2)
            except:
                traceback.print_exc()
                print("出现异常")
                break

        print('OK')
        self.N_Ok += 1
        self.ProgressGetModule(['download',self.N_Ok])

    def ProgressGetModule(self,Progress):
        if self.ProgressGetModule_ != None:
            self.ProgressGetModule_(Progress)

    def D_cancel(self):
        try:
            self.new_loop.stop()
            self.loop.stop()
            for a in self.Download_Subsection_:
                a.cancel()
        except AttributeError:
            pass



    #def DownloadAll(List):
    #    """
    #        异步多下载(不是分段下载)
    #        :param List: 列表[['url','path_up','path','…']['url','path_up','path','…']]
    #        :return:
    #    """
    #    li = []
    #    for i in List:
    #        li.append(gevent.spawn(Download.DownloadAll_Download, i))
    #    gevent.joinall(li)

    #def DownloadAll_Download(list):
    #    print(list)
    #    r=requests.get(list[0],stream=True)
    #    os.makedirs(list[1], exist_ok=True)
    #    with open(list[2],'wb') as fb:
    #        fb.write(r.content)
    #        print('ok')


if __name__ == '__main__':
    U = 'https://download-ssl.firefox.com.cn/releases/firefox/107.0/zh-CN/Firefox-latest.dmg'
    #U = 'https://download.moslauncher.tk/Download/java/version_grean/Java_16/Java-16-x64-Mac-jdk-16.0.2_osx-x64_bin.tar.gz'
    #U = 'https://download.moslauncher.tk/Download/java/123.txt'
    #U = 'https://launcher.mojang.com/v1/objects/37fd3c903861eeff3bc24b71eed48f828b5269c8/client.jar'
    F = '/Users/xyj/Documents/临时/J.dmg'
    #F = '/Users/xyj/Documents/临时/1.txt'
    P_F = '/Users/xyj/Documents/临时/Java__'
    a = Download()
    a.download(U,F,P_F)
