# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base.spider import Spider
import re,sys,time,urllib3,hashlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host,tab = {
        'User-Agent': 'okhttp-okgo/jeasonlzy',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    },'',{'泰剧','日剧','美剧','台剧'}

    def init(self, host=''):
        if host.startswith('http'): self.host = host

    def homeContent(self, filter):
        if not self.host: return None
        response = self.post(f'{self.host}/v3/type/top_type', data=self.payload(), headers=self.headers, verify=False).json()
        classes = []
        for i in response['data']['list']:
            if isinstance(i, dict):
                if i['type_name'] not in self.tab:
                    classes.append({'type_id': i['type_id'],'type_name': i['type_name']})
        return {'class': classes}

    def homeVideoContent(self):
        if not self.host: return None
        response = self.post(f'{self.host}/v3/type/tj_vod', data=self.payload({'':''}), headers=self.headers, verify=False).json()
        data = response['data']
        videos = []
        videos.extend(self.arr2vods(data.get('cai',[])))
        videos.extend(self.arr2vods(data.get('loop', [])))
        for i in data.get('type_vod',[]):
            if isinstance(i,dict):
                if i['type_name'] not in self.tab:
                    videos.extend(self.arr2vods(i.get('vod', [])))
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if not self.host: return None
        response = self.post(f'{self.host}/v3/home/type_search', data=self.payload({'type_id':str(tid),'page':str(pg)}), headers=self.headers, verify=False).json()
        return {'list': self.arr2vods(response['data']['list']), 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        if not self.host: return None
        response = self.post(f'{self.host}/v3/home/search', data=self.payload({'keyword':key}), headers=self.headers, verify=False).json()
        videos = []
        for i in response['data']['list']:
            i.pop('vod_play_list', None)
            videos.append(i)
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        if not self.host: return None
        response = self.post(f'{self.host}/v3/home/vod_details', data=self.payload({'vod_id':str(ids[0])}), headers=self.headers, verify=False).json()
        data = response['data']
        shows,play_urls = [],[]
        for i in data['vod_play_list']:
            parses = ','.join(i['parse_urls'])
            urls = []
            for j in i['urls']:
                urls.append(f"{j['name']}${j['url']}@{parses}@{i['ua']}@{i['referer']}")
            play_urls.append('#'.join(urls))
            name = re.sub(r'[\(（](?:点击|换)[^)]*[\)）]|[Z▶❤【].*', '', i.get('title', i.get('name', '')))
            if name == i['flag']:
                shows.append(name)
            else:
                shows.append(f"{name}({i['flag']})")
        video = {
            'vod_id': data['vod_id'],
            'vod_name': data['vod_name'],
            'vod_pic': data.get('vod_pic',data.get('vod_pic_thumb')),
            'vod_remarks': data['vod_remarks'],
            'vod_year': data['vod_year'],
            'vod_area': data['vod_area'],
            'vod_actor': data['vod_actor'],
            'vod_director': data['vod_director'],
            'vod_content': data['vod_content'],
            'vod_play_from': '$$$'.join(shows),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': data['vod_class']
        }
        return {'list': [video]}

    def playerContent(self, flag, vid, vip_flags):
        raw_url,parses,ua,referer = vid.split('@',3)
        jx,url,play_headers = 0,'',{}
        if ua:
            play_headers['User-Agent'] = ua
        if referer:
            play_headers['Referer'] = referer
        for parse in parses.split(','):
            try:
                if parse.startswith('http'):
                    res = self.fetch(f'{parse}{raw_url}',headers=self.headers, verify=False).json()
                    play_url = res['url']
                    if play_url.startswith('http'):
                        url = play_url
            except Exception:
                pass
        if not url and raw_url.startswith('http'):
            url = raw_url
            if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', raw_url):
                jx = 1
        return {'jx': jx, 'parse': 0, 'url': url, 'header': play_headers}

    def arr2vods(self, arr):
        videos = []
        for i in arr:
            try:
                videos.append({
                    'vod_id': i['vod_id'],
                    'vod_name': i['vod_name'],
                    'vod_pic': i.get('vod_pic',i.get('vod_pic_thumb')),
                    'vod_remarks': i.get('vod_remarks'),
                    'vod_year': None
                })
            except Exception:
                continue
        return videos

    def payload(self, payload={}):
        timestamp = str(int(time.time()))
        return {
            'sign': hashlib.md5(f'7gp0bnd2sr85ydii2j32pcypscoc4w6c7g5spl{timestamp}'.encode()).hexdigest(),
            **payload,
            'timestamp': timestamp
        }

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