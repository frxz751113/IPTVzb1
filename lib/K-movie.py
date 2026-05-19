# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import sys,urllib3
from base.spider import Spider
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host = {
        'User-Agent': "Dart/3.1 (dart:io)",
        'Accept-Encoding': "gzip"
    },'https://ksong520.com'

    def homeContent(self, filter):
        if not self.host: return None
        response = self.fetch(f'{self.host}/openapi/template/vod/category', headers=self.headers, verify=False).json()
        classes = []
        for i in response:
            if isinstance(i,dict):
                classes.append({'type_id': i['id'], 'type_name': i['name']})
        return {'class': classes}

    def homeVideoContent(self):
        response = self.fetch(f'{self.host}/openapi/template/vod?hots=true&limit=12&random=true&order=10',headers=self.headers, verify=False).json()
        return {'list': self.json2vods(response)}

    def categoryContent(self, tid, pg, filter, extend):
        if not isinstance(pg,int): pg = int(pg)
        pg2 = pg-1
        if pg2 > 0:
            offset = pg * 10 - 10
        else:
            offset = 0
        response = self.fetch(f'{self.host}/openapi/template/vod?limit=24&offset={offset}&categoryPid={tid}', headers=self.headers, verify=False).json()
        return {'list': self.json2vods(response), 'pagecount': self.page(response['total']), 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        if not isinstance(pg,int): pg = int(pg)
        pg2 = pg-1
        if pg2 > 0:
            offset = pg * 10 - 10
        else:
            offset = 0
        response = self.fetch(f'{self.host}/openapi/template/vod?limit=10&offset={offset}&keyword={key}', headers=self.headers, verify=False).json()
        return {'list': self.json2vods(response), 'pagecount': self.page(response['total']), 'page': pg}

    def detailContent(self, ids):
        response = self.fetch(f"{self.host}/openapi/template/vod/brief/{ids[0]}",headers=self.headers, verify=False).json()
        info = response['info']
        info2 = info['info']
        play_from, play_urls = [], []
        for i in info2['lines']:
            playline = i['playline']
            from_tag = next((j.get('tag') for j in playline if j.get('tag')), None)
            urls = [f"{j['name']}${j['id']}" for j in playline]
            play_urls.append('#'.join(urls))
            play_from.append(from_tag or i['name'])
        video = {
            'vod_id': ids[0],
            'vod_name': info2['title'],
            'vod_pic': info2['surfacePlot'],
            'vod_remarks': info2['note'],
            'vod_year': info2['year'],
            'vod_area': info2['region'],
            'vod_actor': info2['actors'],
            'vod_director': info2['directors'],
            'vod_content': info2['introduce'],
            'vod_play_from': '$$$'.join(play_from),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': info['category']['name']
        }
        return {'list': [video]}

    def playerContent(self, flag, video_id, vip_flags):
        url = ''
        if video_id.startswith('http'):
            url = video_id
        else:
            try:
                response = self.fetch(f'{self.host}/openapi/playline/{video_id}', headers=self.headers, verify=False).json()
                play_url = response['info']['file']
                if play_url.startswith('http'): url = play_url
            except Exception:
                pass
        return { 'jx': 0, 'parse': 0, 'url': url, 'header': {'User-Agent':'ExoPlayer','Connection':'Keep-Alive','Accept-Encoding':'gzip'}}

    def page(self, total, per_page=10):
        if not isinstance(total, int) or total < 0:
            raise ValueError("total 必须是非负整数")
        if not isinstance(per_page, int) or per_page <= 0:
            raise ValueError("per_page 必须是正整数")
        if total == 0: return 0
        div_result = total / per_page
        integer_part = int(div_result)
        if div_result == integer_part:
            return integer_part
        else:
            return integer_part + 1

    def json2vods(self,arr):
        videos = []
        for i in arr['list']:
            videos.append({
                'vod_id': i['id'],
                'vod_name': i['name'],
                'vod_pic': i['horizontalPoster'],
                'vod_remarks': i['note'],
                'vod_content': i['introduce']
            })
        return videos

    def init(self, extend=""):
        pass

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