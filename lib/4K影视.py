# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import re,sys,urllib3
from base.spider import Spider
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host,dkey = {
        'User-Agent': 'Dart/3.8 (dart:io)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'content-type': 'application/json'
    }, '',{ds.decode('gbk') for ds in [b'\xc2\xd7\xc0\xed',b'\xb8\xa3\xc0\xfb',b'\xcd\xac\xd0\xd4',b'\xc7\xe9\xc9\xab']}

    def init(self, extend=""):
        def_host = 'http://110.42.110.226:9393'
        try:
            response = self.fetch('http://8.155.164.214:9393/domain/current', headers=self.headers, verify=False).json()
            domain = response['data']['domain']
            if domain:
                self.host = f'http://{domain}'
            else:
                self.host = def_host
        except Exception:
            self.host = def_host

    def homeContent(self, filter):
        response = self.fetch(f'{self.host}/api/homeConfig/list', headers=self.headers, verify=False).json()
        classes = []
        for i in response['data']:
            if isinstance(i,dict):
                classes.append({'type_id': i['typeId'], 'type_name': i['typeName']})
        return {'class': classes}

    def homeVideoContent(self):
        response = self.fetch(f'{self.host}/api/recommend/list', headers=self.headers, verify=False).json()
        videos = []
        for i in response['data']:
            response2 = self.fetch(f"{self.host}/api/recommend/contentList?recommendId={i['recommendId']}", headers=self.headers, verify=False).json()
            videos.extend(self.arr2vods(response2['data']))
            break
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        response = self.fetch(f'{self.host}/api/video/list?typeId={tid}&page={pg}&pageSize=20&sort=latest', headers=self.headers, verify=False).json()
        videos = self.arr2vods(response['data'])
        return {'list': videos, 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        response = self.fetch(f'{self.host}/api/video/search?keyword={key}&page={pg}&pageSize=20', headers=self.headers, verify=False).json()
        videos = self.arr2vods(response['data'])
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        response = self.fetch(f'{self.host}/api/video/detail/{ids[0]}', headers=self.headers, verify=False).json()
        data  = response['data']
        shows, play_urls = [], []
        for show, episodes in data['videoListMap'].items():
            name = show
            for k,l in data.get('videoNameMap',{}).items():
                if k == show:
                    if l.lower() != k.lower():
                        name = f"{l}\u2005({k})"
                    else:
                        name = l
                    break
            urls = []
            for j in episodes:
                urls.append(f"{j['episodeName']}${show}@{j['episodeUrl']}")
            play_urls.append('#'.join(urls))
            shows.append(name)
        video = {
            'vod_id': data['vodId'],
            'vod_name': data['vodName'],
            'vod_pic': data['vodPic'],
            'vod_remarks': data['vodRemarks'],
            'vod_year': data['vodYear'],
            'vod_area': data['vodArea'],
            'vod_actor': data['vodActor'],
            'vod_director': data['vodDirector'],
            'vod_content': data['vodContent'],
            'vod_play_from': '$$$'.join(shows),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': data['vodClass']
        }
        return {'list': [video]}

    def playerContent(self, flag, vid, vip_flags):
        jx,url = 0,''
        play_from, raw_url = vid.split('@',1)
        try:
            response = self.fetch(f'{self.host}/api/resolve/getPlayUrl?url={raw_url}&resolveCode={play_from}', headers=self.headers, verify=False).json()
            play_url = response['data']['url']
            if play_url.startswith('http'): url = play_url
        except  Exception:
            pass
        if not url:
            url = raw_url
            if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', vid):
                jx = 1
        return { 'jx': jx, 'parse': '0', 'url': url, 'header': {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'}}

    def arr2vods(self, arr):
        videos = []
        if isinstance(arr, list):
            for i in arr:
                vod_class = i.get('vodClass')
                if not(isinstance(vod_class, str) and any(i in vod_class for i in self.dkey)):
                    videos.append({
                        'vod_id': i.get('vodId',i.get('videoId')),
                        'vod_name': i['vodName'],
                        'vod_pic': i.get('vodPic'),
                        'vod_remarks': i.get('vodRemarks'),
                        'vod_year': i.get('vodYear'),
                        'vod_content': i.get('vodBlurb'),
                        'type_name': vod_class
                    })
        return videos

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    def localProxy(self, param):
        pass