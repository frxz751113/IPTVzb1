# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
import re,sys,json,base64,urllib3
from Crypto.Util.Padding import unpad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,iv, key,host = {
        'User-Agent': "okhttp/3.12.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }, '1234567890123456', '', ''

    def init(self, extend=""):
        try:
            host = extend.strip()
            if host.startswith('http'): self.host = host
            response = self.fetch(f'{self.host}/public/?service=App.Mov.GetTypeList', headers=self.headers, verify=False).text
            data = self.decode(response)
            sign_start = ''
            for i in data['Data']:
                if str(i['type_id']) == '1':
                    sign_start = i['type_union']
                    break
            response2 = self.fetch(f'{self.host}/public/?service=App.Mov.GetAdType', headers=self.headers, verify=False).text
            data2 = self.decode(response2)
            sign_end = data2['Data']['tmp']
            key = f'{sign_start}{sign_end}'[:16]
            if len(key) == 16: self.key = key
        except Exception:
            self.host = ''

    def homeContent(self, filter):
        if not self.host: return None
        return {'class': [{'type_id': 1, 'type_name': '电影'}, {'type_id': 2, 'type_name': '连续剧'}, {'type_id': 3, 'type_name': '综艺'}, {'type_id': 4, 'type_name': '动漫'}]}

    def homeVideoContent(self):
        if not self.host: return None
        response = self.fetch(f'{self.host}/public/?service=App.Mov.GetHomeLevel', headers=self.headers, verify=False).text
        data = self.decode(response)
        videos = []
        for i in data.values():
            if isinstance(i, dict):
                for j in i.values():
                    for k in j:
                        videos.append({
                            'vod_id': k['vod_id'],
                            'vod_name': k['vod_name'],
                            'vod_pic': k['vod_pic'],
                            'vod_remarks': k['vod_remarks'],
                            'vod_year': k['vod_year'],
                            'vod_content': k['vod_content'],
                        })
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if not self.host: return None
        response = self.fetch(f'{self.host}/public/?service=App.Mov.GetOnlineList&type_id={tid}&page={pg}&limit=18', headers=self.headers, verify=False).text
        data = self.decode(response)
        videos = []
        for i in data.get('Data',[]):
            videos.append({
                'vod_id': i['vod_id'],
                'vod_name': i['vod_name'],
                'vod_pic': i['vod_pic'],
                'vod_remarks': i['vod_remarks'],
                'vod_year': i['vod_year'],
                'vod_content': i['vod_content'],
            })
        return {'list': videos, 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        if not self.host: return None
        response = self.fetch(f'{self.host}/public/?service=App.Mov.SearchVod&key={key}', headers=self.headers, verify=False).text
        data = self.decode(response)
        videos = []
        for i in data.get('Data',[]):
            if isinstance(i,dict):
                videos.append({
                    'vod_id': i['vod_id'],
                    'vod_name': i['vod_name'],
                    'vod_pic': i['vod_pic'],
                    'vod_remarks': i['vod_remarks'],
                    'vod_year': i['vod_year'],
                    'vod_content': i['vod_content']
                })
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        response = self.fetch(f'{self.host}/public/?service=App.Mov.GetOnlineMvById&vodid={ids[0]}', headers=self.headers, verify=False).text
        data = self.decode(response)
        for i in data.get('Data', []):
            print(type(i))
            if isinstance(i, dict):
                videos = {
                    'vod_id': i['vod_id'],
                    'vod_name': i['vod_name'],
                    'vod_pic': i['vod_pic'],
                    'vod_remarks': i['vod_remarks'],
                    'vod_year': i['vod_year'],
                    'vod_area': i['vod_area'],
                    'vod_actor': i['vod_actor'],
                    'vod_content': i['vod_content'],
                    'vod_play_from': i['vod_play_from'],
                    'vod_play_url': i['vod_play_url'],
                    'type_name': i['vod_class'],
                }
                return {'list': [videos]}
            return None
        return None

    def playerContent(self, flag, id, vipflags):
        jx,parse,url,ua = 0,0,'','com.gjkj.zxysdq/1.1.0 (Linux;Android 12) ExoPlayerLib/2.12.3'
        if re.match(r'https?:\/\/.*\.(m3u8|mp4|flv|mkv)', id):
            url = id
        else:
            try:
                response = self.fetch(f'{self.host}/public/?service=App.Mov.GetMvJXUrlByUrl&url={id}', headers=self.headers, verify=False).text
                data = self.decode(response)
                raw_url = data['Data']['url']
                paly_url = self.decrypt(raw_url)
                if paly_url.startswith('http'):
                    url = paly_url
            except Exception:
                if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', id):
                    url,parse = id,1
                    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        return { 'jx': jx, 'parse': parse, 'url': url, 'header': {'User-Agent': ua}}

    def decrypt(self, base64_ciphertext):
        try:
            ciphertext = base64.b64decode(base64_ciphertext)
            cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, self.iv.encode('utf-8'))
            plaintext_bytes = cipher.decrypt(ciphertext)
            decrypted = unpad(plaintext_bytes, AES.block_size)
            return decrypted.decode('utf-8')
        except Exception:
            raise Exception('解密失败')

    def decode(self, data):
        return json.loads(data[1:] if data.startswith('\ufeff') else data)

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