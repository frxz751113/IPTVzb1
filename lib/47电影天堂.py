# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
from urllib.parse import quote_plus, unquote_plus
import os,sys,json,random,base64,urllib3,hashlib,binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host,cid,device_id,appid,channel,targ,proxy_url = {
        'User-Agent': "okhttp/3.12.13",
        'Accept-Encoding': "gzip",
        'accept-language': "zh-CN,zh;q=0.8"
    }, 'https://api.dyapis.cn',{'6'},'','__UNI__687ABC2','guanfang',{b'\xc2\xd7\xc0\xed'.decode('gbk'),b'\xb1\xa1\xa6\xe2'.decode('big5'),b'\xba\xd6\xa7Q'.decode('big5')},''

    def init(self, extend=''):
        if not self.host: return
        try:
            self.proxy_url = f'{self.getProxyUrl(True)}&type=47dyttpic'
        except Exception:
            self.proxy_url = 'http://127.0.0.1:9978/proxy?do=py&type=47dyttpic'
        device_id_cache_key = 'cc.vod.dytt_device_id_9e93d6a8c03487d2'
        self.device_id = self.getCache(device_id_cache_key)
        if not(self.device_id and isinstance(self.device_id,str) and len(self.device_id) == 32):
            self.device_id = self.random_32md5()
            self.setCache(device_id_cache_key, self.device_id)
        payload = {'data': self.encrypt(f'{{"user_uuid":"{self.device_id}","appid":"{self.appid}","channel":"{self.channel}","user_token":"","invite":"{self.channel}","uuid":"{self.device_id}","version":"2.0","platform":"1101","versionCode":"105","token":"{self.device_id}"}}')}
        response = self.post(f"{self.host}/api/app/home", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return
        data = json.loads(self.decrypt(response['data']))
        for i in data['type']:
            if any(j in i['name'] for j in self.targ):
                self.cid.add(str(i['id']))

    def homeContent(self, filter):
        payload = {'data': self.encrypt(f'{{"user_uuid":"{self.device_id}","appid":"{self.appid}","channel":"{self.channel}","user_token":"","invite":"{self.channel}","uuid":"{self.device_id}","version":"2.0","platform":"1101","versionCode":"105","token":"{self.device_id}"}}')}
        response = self.post(f"{self.host}/api/app/vodClass", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return
        data = json.loads(self.decrypt(response['data']))
        classes = []
        for i in data['type']:
            if any(j in i['name'] for j in self.targ):
                self.cid.add(str(i['id']))
            else:
                if isinstance(i, dict) and i['name'] not in {'推荐','全部', b'\xba\xd6\xa7Q'.decode('big5')}:
                    classes.append({'type_id': i['id'], 'type_name': i['name']})
        return {'class': classes}

    def homeVideoContent(self):
        payload = {'data': self.encrypt(f'{{"user_uuid":"{self.device_id}","appid":"{self.appid}","channel":"{self.channel}","user_token":"","invite":"{self.channel}","uuid":"{self.device_id}","version":"1.0.5","platform":"1101","versionCode":"105","token":"{self.device_id}"}}')}
        response = self.post(f"{self.host}/api/app/topicIndexList", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return response
        data = json.loads(self.decrypt(response['data']))
        videos = []
        for i in data['list']:
            videos.extend(self.arr2vods(i['vod_list']))
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        payload = {'data':self.encrypt(f'{{"area":"","year":"","channel":"{self.channel}","sort":"","type":"","uuid":"{self.device_id}","version":"1.0.5","platform":"1101","versionCode":"105","token":"{self.device_id}","user_uuid":"{self.device_id}","type_pid":"{tid}","appid":"{self.appid}","user_token":"","invite":"{self.channel}","page":"{pg}","lang":"","class":""}}')}
        response = self.post(f"{self.host}/api/app/vodList", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return response
        data = json.loads(self.decrypt(response['data']))
        return {'list': self.arr2vods(data['list']),'pagecount': data['page_total'], 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        payload = {'data': self.encrypt(f'{{"user_uuid":"{self.device_id}","appid":"{self.appid}","channel":"{self.channel}","user_token":"","invite":"{self.channel}","page":"{pg}","uuid":"{self.device_id}","version":"1.0.5","wd":"{key}","platform":"1101","versionCode":"105","token":"{self.device_id}"}}')}
        response = self.post(f"{self.host}/api/app/searchList", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return response
        data = json.loads(self.decrypt(response['data']))
        return {'list': self.arr2vods(data['list']),'pagecount': data['page_total'], 'page': pg}

    def detailContent(self, ids):
        payload = {'data': self.encrypt(f'{{"user_uuid":"{self.device_id}","appid":"{self.appid}","channel":"{self.channel}","user_token":"","invite":"{self.channel}","id":"{ids[0]}","uuid":"{self.device_id}","version":"1.0.5","platform":"1101","versionCode":"105","token":"{self.device_id}"}}')}
        response = self.post(f"{self.host}/api/app/vodDetails", data=payload, headers=self.headers, verify=False).json()
        if 'data' not in response: return response
        data = json.loads(self.decrypt(response['data']))
        if str(data['type_id']) in self.cid: return None
        show, play_urls = [], []
        for i in data['vod_play_url']:
            urls = []
            for j in i['list']:
                urls.append(f"{j['name']}${j['url']}")
            play_urls.append('#'.join(urls))
            if i['key'] == i['name']:
                name = i['key']
            else:
                name = f"{i['name']}\u2005({i['key']})"
            show.append(name)
        video = {
            'vod_id': data['vod_id'],
            'vod_name': data['vod_name'],
            'vod_pic': data['vod_pic'],
            'vod_remarks': data['vod_remarks'],
            'vod_year': data['vod_year'],
            'vod_area': data['vod_area'],
            'vod_actor': ','.join(data['vod_actor']),
            'vod_director': ','.join(data['vod_director']),
            'vod_content': data['vod_content'],
            'vod_play_from': '$$$'.join(show),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': ','.join(data['vod_class'])
        }
        return {'list': [video]}

    def playerContent(self, flag, url, vip_flags):
        return { 'jx': 0, 'parse': 0, 'url': url, 'header': {'User-Agent':'okhttp/3.12.13','Accept-Encoding':'gzip'}}

    def localProxy(self, params):
        if params['type'] == '47dyttpic':
            return self.dytt47pic(params['url'])
        return None

    def decrypt(self, ciphertext):
        try:
            len_cipher = len(ciphertext)
            if len_cipher < 48:
                iv_hex = ciphertext[len_cipher - 32:]
                encrypted_data_hex = ciphertext[:len_cipher - 32]
            else:
                iv_hex = ciphertext[16:48]
                encrypted_data_hex = ciphertext[:16] + ciphertext[48:]
            iv_bytes = binascii.unhexlify(iv_hex)
            encrypted_data_bytes = binascii.unhexlify(encrypted_data_hex.upper())
            cipher = AES.new("UeFk58Si151OmxqH".encode('utf-8'), AES.MODE_CFB, iv=iv_bytes, segment_size=128)
            decrypted_bytes = cipher.decrypt(encrypted_data_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception:
            return None

    def encrypt(self,plaintext):
        try:
            iv = os.urandom(16)
            cipher = AES.new("UeFk58Si151OmxqH".encode('utf-8'), AES.MODE_CFB, iv=iv, segment_size=128)
            encrypted_bytes = cipher.encrypt(plaintext.encode('utf-8'))
            encrypted_hex = binascii.hexlify(encrypted_bytes).decode('utf-8')
            iv_hex = binascii.hexlify(iv).decode('utf-8')
            return encrypted_hex[:16] + iv_hex + encrypted_hex[16:]
        except Exception:
            return None

    def dytt47pic(self,url):
        url = unquote_plus(url)
        headers = self.headers
        try:
            prefix = 'https://img.duanjuzy.com/12345.php?img='
            if url.startswith(prefix):
                raw_url = url[len(prefix):]
                if raw_url.startswith('aHR0c'):
                    raw_url2 = base64.b64decode(raw_url.encode('utf-8'),validate=True).decode('utf8')
                    if raw_url2.startswith(('http://','https://')):
                        url = raw_url2
        except Exception:
            pass
        try:
            if not 'dyapis.cn' in url: headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/537.36'
            response = self.fetch(url, headers=headers, verify=False).content
            try:
                data = base64.b64decode(response,validate=True)
            except Exception:
                data = response
        except Exception:
            data = ''
            return [400, 'application/octet-stream', data]
        return [200, 'application/octet-stream', data]

    def arr2vods(self,arr):
        videos = []
        for i in arr:
            if not str(i['type_id']) in self.cid:
                videos.append({
                    'vod_id': i['vod_id'],
                    'vod_name': i['vod_name'],
                    'vod_pic': f"{self.proxy_url}&url={quote_plus(i['vod_pic'])}",
                    'vod_remarks': i['vod_remarks']
                })
        return videos

    def random_32md5(self):
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        return hashlib.md5(random_string.encode('utf-8')).hexdigest()

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass
