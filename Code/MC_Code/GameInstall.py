# coding=utf-8
import asyncio
import json
import os
import zipfile

import traceback
import aiofiles as aiofiles
import aiohttp
import requests
import sys

from Code.Code import Sha1, Hash
from Code.Download_Big import Download as JarAndBigFileDownload
from Code.Log import print_


class GameInstall():
    def __init__(self, GameFile_M, GameFile_V, File, Download_Source, V_JsonFile,
                 V, Name, V_Forge, V_Fabric, V_Optifine,
                 System, System_V, System_Places,
                 AssetsFileDownloadMethod, Sha1Cleck, MaxConcurrence, ProgressGetModule):
        """
            游戏安装
            :param GameFile_M: 游戏根目录(.minecraft目录)
            :param GameFile_V: 游戏目录
            :param File: MOS缓存目录
            :param Download_Source: 下载源(MCBBS, BMCLAPI, MC)
            :param V_JsonFile: 游戏Json目录(版本列表的)
            :param V: MC版本
            :param Name: 游戏名
            :param V_Forge: Forge版本
            :param V_Fabric: Fabric版本
            :param V_Optifine: Optifine版本
            :param System: 系统种类(Windows, Mac, Linux)
            :param System_V: 系统版本(10,14.4.1)
            :param System_Places: 系统架构位数
            :param AssetsFileDownloadMethod: 资源文件下载方式(A,B-尚未完成)
            :param Sha1Cleck: 是否进行Sha1检查
            :param MaxConcurrence: 最大并发数
            :param ProgressGetModule: 进度通知模块, 在进度改变后自动通知
        """
        self.GameFile_M = GameFile_M
        self.GameFile_V = GameFile_V
        self.File = File
        self.Download_Source = Download_Source
        self.V_JsonFile = V_JsonFile
        self.V = V
        self.Name = Name
        self.V_Forge = V_Forge
        self.V_Fabric = V_Fabric
        self.V_Optifine = V_Optifine
        self.System = System
        self.System_V = System_V
        self.System_Places = System_Places
        self.AssetsFileDownloadMethod = AssetsFileDownloadMethod
        self.Sha1Cleck = Sha1Cleck
        self.MaxConcurrence = MaxConcurrence
        self.ProgressGetModule = ProgressGetModule
        self.Stop_ = False

        if self.Download_Source == 'MC':
            # self.Download_Source_Url_Json_Q = 'http://launchermeta.mojang.com/'
            self.Download_Source_Url_Libraries_Q = 'http://libraries.minecraft.net/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://resources.download.minecraft.net/'  # 资源文件
        elif self.Download_Source == 'MCBBS':
            self.Download_Source_Url_Json_Q = 'http://download.mcbbs.net/'  # json文件
            self.Download_Source_Url_Jar_Q = 'http://download.mcbbs.net/version/'  # Jar文件
            self.Download_Source_Url_Libraries_Q = 'http://download.mcbbs.net/maven/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://download.mcbbs.net/assets/'  # 资源文件
        else:
            self.Download_Source_Url_Json_Q = 'http://bmclapi2.bangbang93.com/'  # json文件
            self.Download_Source_Url_Jar_Q = 'http://bmclapi2.bangbang93.com/version/'  # Jar文件
            self.Download_Source_Url_Libraries_Q = 'http://bmclapi2.bangbang93.com/maven/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://bmclapi2.bangbang93.com/assets/'  # 资源文件

        super(GameInstall, self).__init__()

    def Run(self):
        # 下载MC Json文件
        # 拼接路径
        try:
            if self.Download_Source == 'MC':
                with open(self.V_JsonFile, 'r', encoding='utf_8') as f:
                    b = json.load(f)
                for b_1 in b['versions']:
                    if b_1['id'] == self.V:
                        url = b_1['url']
                        break
            else:
                url = self.Download_Source_Url_Json_Q + 'version/' + self.V + '/json'
            self.Progress(['start', 1, 7])

            # 下载
            V_Json_Get = requests.get(url)
            V_Json = V_Json_Get.json()
            V_Json['id'] = self.Name
            os.makedirs(self.GameFile_V, exist_ok=True)
            V_Json_File = os.path.join(self.GameFile_V, str(self.Name + '.json'))
            with open(V_Json_File, 'w+', encoding='utf-8') as f:
                json.dump(V_Json, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            self.Progress(['start', 2, 7])

            # 下载Assets List Json文件
            AssetsList_Json = V_Json['assetIndex']
            try:
                url = self.Download_Source_Url_Json_Q + AssetsList_Json['url'].split('https://piston-meta.mojang.com/')[1]
            except IndexError:
                url = self.Download_Source_Url_Json_Q + \
                      AssetsList_Json['url'].split('https://launchermeta.mojang.com/')[1]
            except AttributeError:
                url = AssetsList_Json['url']
            id = AssetsList_Json['id']
            path_up = os.path.join(self.GameFile_M, 'assets', 'indexes')
            path = os.path.join(path_up, id + '.json')
            AssetsList_Json_Get = requests.get(url)
            AssetsList_Json = AssetsList_Json_Get.json()
            os.makedirs(path_up, exist_ok=True)
            with open(path, 'w+', encoding='utf-8') as f:
                json.dump(AssetsList_Json, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            self.Progress(['start', 3, 7])

            self.MainJar = []
            self.Libraries = []
            self.Assets = []
            self.Size_All = 0
            self.Size_Ok = 0
            self.Progress(['start', 4, 7])

            # Jar文件解析
            a = V_Json['downloads']['client']
            if self.Download_Source != 'MC':
                url = self.Download_Source_Url_Jar_Q + self.V + '/client'
            else:
                url = a['url']
            self.Size_All += a['size']
            self.MainJar = ['MCJar', url,
                            self.GameFile_V, os.path.join(self.GameFile_V, str(self.Name) + '.jar'),
                            a['sha1'], a['size']]
            self.Progress(['start', 5, 7])

            import re
            # Libraries文件解析
            for L in V_Json['libraries']:
                if 'rules' in L:
                    for R in L['rules']:
                        if len(R) != 1:
                            if R['action'] == 'disallow':
                                # 如果写的是禁止
                                R.pop('action')
                                for a in R:
                                    if R[a]['name'] == 'osx':
                                        if self.System == 'Mac':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m == None:
                                                # 如果不在限制以内,就添加

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['osx']
                                                    A = L['downloads']['classifiers'][b]
                                                Sh = A['sha1']

                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            print('l_on')
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                                    elif R[a]['name'] == 'windows':
                                        if self.System == 'Win':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m == None:
                                                # 如果不在限制以内,就添加

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['windows']
                                                    if self.System_Places == 64:
                                                        # 如果为60位
                                                        c = 'natives-windows-64"'
                                                    else:
                                                        c = 'natives-windows-32'
                                                    if b != 'natives-windows-${arch}':
                                                        A = L['downloads']['classifiers'][b]
                                                    else:
                                                        A = L['downloads']['classifiers'][c]
                                                    Sh = A['sha1']

                                                # 添加
                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                                    elif R[a]['name'] == 'linux':
                                        if self.System == 'Linux':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m == None:
                                                # 如果不在限制以内,就添加

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['linux']
                                                    A = L['downloads']['classifiers'][b]
                                                Sh = A['sha1']


                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                            elif R['action'] == 'allow':
                                # 如果写的是允许
                                R.pop('action')
                                for a in R:
                                    if R[a]['name'] == 'osx':
                                        if self.System == 'Mac':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m != None:
                                                # 如果在允许以内,就添加

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['osx']
                                                    A = L['downloads']['classifiers'][b]
                                                Sh = A['sha1']

                                                # 添加
                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                                    elif R[a]['name'] == 'windows':
                                        if self.System == 'Win':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m != None:
                                                # 如果在允许以内,就添加

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['windows']
                                                    if self.System_Places == 64:
                                                        # 如果为60位
                                                        c = 'natives-windows-64"'
                                                    else:
                                                        c = 'natives-windows-32'
                                                    if b != 'natives-windows-${arch}':
                                                        A = L['downloads']['classifiers'][b]
                                                    else:
                                                        A = L['downloads']['classifiers'][c]
                                                    Sh = A['sha1']

                                                # 添加
                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    if 'artifact' in L['downloads']:
                                                        A = L['downloads']['artifact']
                                                        Zip = False
                                                    else:
                                                        A = L['downloads']['classifiers']['natives-windows']
                                                        Zip = True
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                                    elif R[a]['name'] == 'linux':
                                        if self.System == 'Linux':
                                            # 如果系统匹配就进行正则表达式判断
                                            if 'version' in R[a]:
                                                # 如果写了系统版本限制规则
                                                r = R[a]['version']
                                                m = re.search(r, self.System_V)
                                            else:
                                                m = ''  # 让下面的if, 识别为"允许"

                                            if m != None:
                                                # 如果在允许以内,就添加
                                                URL = self.Download_Source_Url_Libraries_Q + \
                                                      A['url'].split('https://libraries.minecraft.net/')[1]
                                                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                                Path_Up = os.path.abspath(os.path.join(Path, ".."))

                                                if 'artifact' in L['downloads']:
                                                    Zip = False
                                                    A = L['downloads']['artifact']
                                                else:
                                                    Zip = True
                                                    b = L['natives']['linux']
                                                    A = L['downloads']['classifiers'][b]
                                                Sh = A['sha1']

                                                if os.path.exists(Path):
                                                    # 如果目录存在
                                                    if self.Sha1Cleck:
                                                        s = Sha1(Path)
                                                        if s != Sh:
                                                            self.Size_All += A['size']
                                                            self.Libraries.append(
                                                                ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                                                else:
                                                    self.Size_All += A['size']
                                                    self.Libraries.append(
                                                        ['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])

                else:
                    # 没有规则限制
                    if self.System == 'Mac':
                        if 'artifact' in L['downloads']:
                            A = L['downloads']['artifact']
                            Zip = False
                        else:
                            A = L['downloads']['classifiers']['natives-osx']
                            Zip = True
                    elif self.System == 'Win':
                        if 'artifact' in L['downloads']:
                            A = L['downloads']['artifact']
                            Zip = False
                        else:
                            A = L['downloads']['classifiers']['natives-windows']
                            Zip = True
                    elif self.System == 'Linux':
                        if 'artifact' in L['downloads']:
                            A = L['downloads']['artifact']
                            Zip = False
                        else:
                            A = L['downloads']['classifiers']['natives-linux']
                            Zip = True
                    URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                    Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                    Path_Up = os.path.abspath(os.path.join(Path, ".."))
                    Sh = A['sha1']
                    if os.path.exists(Path):
                        # 如果目录存在
                        if self.Sha1Cleck:
                            s = Sha1(Path)
                            if s != Sh:
                                if 'artifact' in L['downloads']:
                                    A = L['downloads']['artifact']
                                    Zip = False
                                else:
                                    A = L['downloads']['classifiers']['natives-linux']
                                    Zip = True
                                self.Size_All += A['size']
                                self.Libraries.append(['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
                    else:
                        self.Size_All += A['size']
                        self.Libraries.append(['Libraries', URL, Path_Up, Path, A['size'], Sh, Zip])
            self.Progress(['start', 6, 7])

            # 如果使用方法A，就进行Assets文件解析
            if self.AssetsFileDownloadMethod == 'A':
                print(AssetsList_Json)
                for A in AssetsList_Json['objects']:
                    # 注意, MC官方这里写的hash其实是sha1算法
                    hash = AssetsList_Json['objects'][A]['hash']
                    url = self.Download_Source_Url_Resources_Q + hash[0:2] + '/' + hash
                    size = AssetsList_Json['objects'][A]['size']
                    path_up = os.path.join(self.GameFile_M, 'assets', 'objects', hash[0:2])
                    path = os.path.join(path_up, hash)
                    if os.path.exists(path):
                        # 如果文件存在就判断hash值
                        h = Sha1(path)
                        if h != hash:
                            self.Size_All += size
                            self.Assets.append(['Assets', url, path_up, path, size, hash])
                    else:
                        self.Size_All += size
                        self.Assets.append(['Assets', url, path_up, path, size, hash])
            self.Progress(['start', 7, 7])

            if self.Stop_ == False:
                print(self.MainJar)
                print('================')
                print(self.Libraries)
                self.Libraries_N = len(self.Libraries)
                print(self.Libraries_N)
                print('================')
                # print(Assets)
                self.Assets_N = len(self.Assets)
                print(self.Assets_N)
                self.Progress(['info', self.Libraries_N, self.Assets_N, self.Size_All])

                self.Libraries_Ok = 0
                self.Assets_Ok = 0

                print('准备下载')

            if self.Stop_ == False:
                # 创建
                import time
                time_start = time.perf_counter()
                print('开始下载')
                self.error_quantity = 0  # 出现特定的error数量
                if len(self.Libraries) != 0 or len(self.Assets) != 0:
                    self.AllList = self.Libraries + self.Assets
                    self.I = len(self.AllList) + 1
                    print('一共' + str(self.I) + '项文件')

                    while True:
                        if len(self.AllList) != 0:
                            # if len(self.AllList) <= len(self.Assets):
                            #    i = 80
                            # else:
                            #    i = 80
                            self.new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(self.new_loop)
                            # asyncio.run(self.DownloadTaskMake(self.MaxConcurrence))
                            self.loop = asyncio.get_event_loop()
                            self.loop.run_until_complete(self.DownloadTaskMake(self.MaxConcurrence))
                        else:
                            break
                else:
                    print('一共' + '1' + '项文件')

                if self.Stop_ == False:
                    self.JarDownload = JarAndBigFileDownload()
                    self.JarDownload.download(self.MainJar[1], self.MainJar[3],
                               os.path.join(self.File, 'Caches'),
                               self.JarProgress)
                print('下载完成')
                import time
                time_stop = time.perf_counter()
                time_ = (time_stop - time_start)
                print('用时' + str(time_))

                # 清理内存
                self.AllList = ''
                self.Libraries = ''
                self.Assets = ''

                self.loop.close()
                self.new_loop.close()

                del self.AllList, a, time_stop, time_, self.new_loop, self.loop, self.Assets, self.Libraries
                print_('Info', '[有可能导致错误]开始进行强制内存清理')
                import gc
                gc.collect()
                print_('Info', '[有可能导致错误]强制内存清理完成')

                self.Progress(['ok'])


        except RuntimeError:
            # 如果取消，则终止
            print_('DeBug','[游戏安装程序]出现RuntimeError错误，这可能是用户点了取消，已忽略')
        except requests.exceptions.ProxyError:
            ErrorKind = sys.exc_info()[1]
            ErrorCause = '出现系统代理错误，请关闭代理再试'
            ErrorInfo = traceback.format_exc()
            self.Progress(['error', self.Name, self.V, ErrorKind, ErrorCause, ErrorInfo])
            self.Stop()
        except:
            ErrorKind = sys.exc_info()[1]
            ErrorCause = 'None'
            ErrorInfo = traceback.format_exc()
            self.Progress(['error', self.Name, self.V,ErrorKind, ErrorCause, ErrorInfo])
            self.Stop()


    async def DownloadTaskMake(self, i: int):
        self.loop_b = []
        for a in self.AllList[0:i]:
            self.loop_b.append(asyncio.ensure_future(self.Download(a)))
        for b_1 in self.loop_b:
            await b_1

    # async def DownloadTask(self, queue,list):
    #    while True:
    #        try:
    #            print('取出')
    #            # 从队列中取出任务
    #            task = await queue.get()
    #            # 处理任务
    #            # await self.Download(task)
    #            await asyncio.wait([self.Download(task)])
    #            if task not in self.AllList:
    #                # 通知队列任务已被处理完成
    #                queue.task_done()
    #        except:
    #            traceback.print_exc()

    async def Download(self, list: list):
        """异步任务"""
        print('任务运行')
        # print(list)
        headers = {}
        url = list[1]
        path_up = list[2]
        path = list[3]
        os.makedirs(path_up, exist_ok=True)
        s = list[4] / 1024 / 1024
        if s < 1:
            timeOut = 3
            One = True
        elif s >= 1 and s < 2:
            # 如果大于等于1MB,小于等于2MB
            timeOut = 5
            One = True
        elif s >= 2 and s < 4:
            timeOut = 10
            One = True
        elif s >= 5:
            timeOut = 15
            One = True
        else:
            timeOut = 30
            One = True

        if One:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(connect=4), trust_env=True) as session:
                    async with session.get(url, headers=headers, ssl=False, timeout=timeOut) as response:
                        async with aiofiles.open(path, 'wb') as f:
                            await f.write(await response.content.read())

                    self.AllList.remove(list)
                    print(str(len(self.AllList)) + 'ok')
                if list[0] == 'Libraries':
                    if list[6] == True:
                        path_z = os.path.join(self.GameFile_V, os.path.basename(path))
                        f = zipfile.ZipFile(path, 'r')  # 压缩文件位置
                        for file in f.namelist():
                            f.extract(file, path_z)  # 解压位置
                        f.close()
                    self.Libraries_Ok += 1
                else:
                    self.Assets_Ok += 1

                print(list)
                self.Size_Ok += list[4]
                self.Progress(['download', self.Libraries_Ok, self.Assets_Ok, self.Size_Ok])
            except aiohttp.client_exceptions.ServerTimeoutError:
                print('error_ServerTimeoutError')
            except aiohttp.client_exceptions.ServerDisconnectedError:
                print('error_ServerDisconnectedError')

            except aiohttp.client_exceptions.ClientConnectorError:
                if self.error_quantity >= 5:
                    # 到达5次进行终止
                    ErrorKind = sys.exc_info()[1]
                    ErrorCause = '未接入互联网'
                    ErrorInfo = traceback.format_exc()
                    print_('Error', '在安装游戏时出现异常,配置信息:' + str(list))
                    print_('DeBug', '由于安装出错,正在取消安装')
                    self.Stop()
                    print_('DeBug', '取消安装完成')
                    self.Progress(['error', self.Name, self.V, ErrorKind, ErrorCause, ErrorInfo])
                else:
                    self.error_quantity += 1


            except aiohttp.client_exceptions.ClientOSError:
                print('error_ClientOSError')
            except asyncio.exceptions.CancelledError:
                print('error_CancelledError')
            except asyncio.exceptions.TimeoutError:
                print('error_TimeoutError')
            except:
                ErrorKind = sys.exc_info()[1]
                ErrorCause = 'None'
                ErrorInfo = traceback.format_exc()
                print_('Error', '在安装游戏时出现异常,配置信息:' + str(list))
                print_('DeBug', '由于安装出错,正在取消安装')
                self.Stop()
                print_('DeBug', '取消安装完成')
                self.Progress(['error', self.Name, self.V, ErrorKind, ErrorCause, ErrorInfo])

        # else:
        #    SectionSize = 4194304
        #    def BigFile_Progress(list):
        #        if list[0] == 'download':
        #            self.Size_Ok += SectionSize
        #    def Run():
        #        a = JarAndBigFileDownload()
        #        a.download(url, path, path_up, BigFile_Progress, SectionSize)
        #    thread1 = threading.Thread(name='t1', target=Run)
        #    thread1.start()  # 启动线程1
        #    thread1.join()

    def Progress(self, Progress_):
        """
            更改安装进度,并且主动通知
            :param Progress_: 进度
        """
        self.ProgressGetModule(Progress_)

    def JarProgress(self, Progress_):
        """
            更改Jar下载进度,并且主动通知
            :param Progress_: 进度
        """
        self.ProgressGetModule(['JarProgress', Progress_])

    def Stop(self):
        try:
            self.Stop_ = True
            self.new_loop.stop()
            self.loop.stop()
            for a in self.loop_b:
                a.cancel()
            self.JarDownload.D_cancel()
        except AttributeError:
            pass
        import shutil
        print_('Info','由于取消安装，正在删除文件夹')
        shutil.rmtree(self.GameFile_V)
        #self.new_loop.close()
        #self.loop.close()



if __name__ == '__main__':
    # a = GameInstall('/Users/xyj/Documents/.minecraft','/Users/xyj/Documents/.minecraft/versions/1.18.1/','/Users/xyj/Documents/.MOS','MCBBS','/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #      '1.18.1','1.18.1',None,None,None,'Mac','11.6.5',True)
    # a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/a1.0.11/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                'a1.0.11', 'a1.0.11', None, None, None,'Mac','11.6.5',True,0)
    # a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.12.2/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                '1.12.2', '1.12.2', None, None, None,'Mac','11.6.5',True,0)
    a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.16.5/',
                    '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
                    '1.16.5', '1.16.5', None, None, None, 'Mac', '11.6.5', 'A', True, 120)
    # a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.9.1/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                '1.9.1', '1.9.1', None, None, None,'Mac','11.6.5',True)
    a.Run()