# coding=utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import datetime
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "http://read.api.duodutek.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "1287", "type_name": "甜宠"},
                            {"type_id": "1288", "type_name": "逆袭"},
                            {"type_id": "1289", "type_name": "热血"},
                            {"type_id": "1290", "type_name": "现代"},
                            {"type_id": "1291", "type_name": "古代"}],
                 }

        return result

    def homeVideoContent(self):
        result = {}
        videos = []
        
        url = f"{xurl}/novel-api/app/pageModel/getResourceById"        
        recommend_cids = ["1287", "1288", "1289", "1290", "1291"]        
        for cid in recommend_cids:
            params = {
                "productId": "2a8c14d1-72e7-498b-af23-381028eb47c0",
                "vestId": "2be070e0-c824-4d0e-a67a-8f688890cadb",
                "channel": "oppo19",
                "osType": "android",
                "version": "20",
                "token": "202509271001001446030204698626",
                "resourceId": cid,
                "pageNum": "1",
                "pageSize": "6"  
            }
            
            try:
                detail = requests.get(url=url, headers=headerx, params=params, timeout=10)
                detail.encoding = "utf-8"
                data = detail.json()
                
                if 'data' in data and 'datalist' in data['data']:
                    data_list = data['data']['datalist']                    
                    for i, vod in enumerate(data_list[:2]):
                        name = vod['name']
                        id = f"{vod['id']}@{vod['introduction']}"
                        pic = vod['icon']
                        remark = f"{vod['heat']}万播放"                        
                        video = {
                            "vod_id": id,
                            "vod_name": name,
                            "vod_pic": pic,
                            "vod_remarks": remark
                        }
                        videos.append(video)
            except Exception as e:
                continue
        
        if len(videos) < 5:
            default_recommends = [
                {"vod_id": "default1@热门短剧推荐", "vod_name": "热门短剧1", "vod_pic": "", "vod_remarks": "推荐"},
                {"vod_id": "default2@热门短剧推荐", "vod_name": "热门短剧2", "vod_pic": "", "vod_remarks": "推荐"},
                {"vod_id": "default3@热门短剧推荐", "vod_name": "热门短剧3", "vod_pic": "", "vod_remarks": "推荐"}
            ]
            videos.extend(default_recommends[:5-len(videos)])
        
        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        url = f"{xurl}/novel-api/app/pageModel/getResourceById"

        params = {
            "productId": "2a8c14d1-72e7-498b-af23-381028eb47c0",
            "vestId": "2be070e0-c824-4d0e-a67a-8f688890cadb",
            "channel": "oppo19",
            "osType": "android",
            "version": "20",
            "token": "202509271001001446030204698626",
            "resourceId": cid,
            "pageNum": str(page),
            "pageSize": "10"
                 }

        detail = requests.get(url=url, headers=headerx, params=params)
        detail.encoding = "utf-8"
        data = detail.json()

        data = data['data']['datalist']

        for vod in data:

            name = vod['name']

            id = f"{vod['id']}@{vod['introduction']}"

            pic = vod['icon']

            remark = f"{vod['heat']}万播放"

            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
                    }
            videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''

        fenge = did.split("@")

        url = f"{xurl}/novel-api/basedata/book/getChapterList"

        params = {
            "bookId": fenge[0],
            "productId": "2a8c14d1-72e7-498b-af23-381028eb47c0",
            "vestId": "2be070e0-c824-4d0e-a67a-8f688890cadb",
            "channel": "oppo19",
            "osType": "android",
            "version": "20",
            "token": "202509271001001446030204698626"
                 }

        detail = requests.get(url=url, headers=headerx, params=params)
        detail.encoding = "utf-8"
        data = detail.json()

        content = f"{fenge[1]}"

        data = data['data']
        
        for index, vod in enumerate(data, 1):
            name = f"第{index}集"
            id = vod['shortPlayList'][0]['chapterShortPlayVoList'][0]['shortPlayUrl']
            bofang = bofang + name + '$' + id + '#'

        bofang = bofang[:-1]

        xianlu = '短剧专线'

        videos.append({
            "vod_id": did,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
                     })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, pg):
        pass

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None