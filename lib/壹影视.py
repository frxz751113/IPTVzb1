# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base.spider import Spider
from Crypto.PublicKey import RSA
import re,sys,time,random,base64,hashlib,urllib3
from Crypto.Util.number import bytes_to_long,long_to_bytes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    def __init__(self):
        super().__init__()
        self.host = 'https://aleig4ah.yiys05.com'
        self.token = ''
        self.app_id = ''
        self.headers = {
            'User-Agent': 'Android/OkHttp',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

    def init(self, extend=''):
        if extend.startswith('http'):
            self.host = extend
        android_id_key = 'yiys_zNiOFyj0r4ux'
        self.app_id = self.getCache(android_id_key)
        if not self.app_id:
            self.app_id = ''.join(random.choice('0123456789abcdef') for _ in range(16))
            self.setCache(android_id_key, self.app_id)
        if not self.token:
            self.refresh_token()

    def refresh_token(self):
        ts = str(int(time.time()))
        payload = {'appID': self.app_id, 'timestamp': ts}
        headers = {**self.headers, 'APP-ID': self.app_id, 'X-Auth-Flow': '1'}
        try:
            res = self.post(f'{self.host}/vod-app/index/getGenerateKey', data=payload, headers=headers, verify=False).json()
            if 'data' in res:
                self.token = self.rsa_public_decrypt(res['data'])
                return True
        except:
            pass
        return False

    def get_signed_headers(self, params):
        h = {**self.headers, 'APP-ID': self.app_id, 'Authorization': ''}
        if params:
            sorted_keys = sorted(params.keys())
            query_str = "&".join([f"{k}={params[k]}" for k in sorted_keys])
            sign_str = f"{query_str}&token={self.token}"
            h['X-HASH-Data'] = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
        return h

    def smart_request(self, url, method='GET', data=None, params=None):
        sign_payload = data if method == 'POST' else params
        headers = self.get_signed_headers(sign_payload)
        if method == 'GET':
            res = self.fetch(url, params=params, headers=headers, verify=False)
        else:
            res = self.post(url, data=data, headers=headers, verify=False)
        if res.status_code == 400 or not res.text:
            if self.refresh_token():
                headers = self.get_signed_headers(sign_payload)
                if method == 'GET':
                    res = self.fetch(url, params=params, headers=headers, verify=False)
                else:
                    res = self.post(url, data=data, headers=headers, verify=False)
        return res.json()

    def homeContent(self, filter):
        ts = str(int(time.time()))
        params = {'timestamp': ts}
        res = self.smart_request(f'{self.host}/vod-app/type/list', params=params)
        classes, filters = [], {}
        def build_filter(key, name, values_str, is_sort=False):
            val_arr = []
            if not is_sort:
                val_arr.append({'n': '全部', 'v': ''})
            if values_str:
                splits = values_str.split(',')
                for s in splits:
                    item = s.strip()
                    if item:
                        val_arr.append({'n': item, 'v': item})
            elif is_sort:
                val_arr = [
                    {'n': '新上线', 'v': 'time'},
                    {'n': '热播榜', 'v': 'hits_day'},
                    {'n': '好评榜', 'v': 'score'}
                ]
            return {
                'key': key,
                'name': name,
                'value': val_arr,
                'init': 'time' if is_sort else ''
            }
        for i in res.get('data', []):
            tid = str(i['typeId'])
            classes.append({'type_id': tid, 'type_name': i['typeName']})
            if 'type_extend_obj' in i:
                ext = i['type_extend_obj']
                type_filters = []
                if ext.get('class'):
                    type_filters.append(build_filter('class', '类型', ext['class']))
                if ext.get('area'):
                    type_filters.append(build_filter('area', '地区', ext['area']))
                if ext.get('lang'):
                    type_filters.append(build_filter('lang', '语言', ext['lang']))
                if ext.get('year'):
                    type_filters.append(build_filter('year', '年份', ext['year']))
                type_filters.append(build_filter('sort', '排序', '', True))
                if type_filters:
                    filters[tid] = type_filters

        return {'class': classes, 'filters': filters}

    def homeVideoContent(self):
        ts = str(int(time.time()))
        params = {'timestamp': ts}
        res = self.smart_request(f'{self.host}/vod-app/rank/hotHits', params=params)
        videos = []
        for i in res.get('data', []):
            if 'vodBeans' in i:
                videos.extend(self.arr2vods(i['vodBeans']))
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        payload = {
            'tid': tid,
            'page': str(pg),
            'limit': '12',
            'timestamp': str(int(time.time())),
            'classType': extend.get('class', ''),
            'area': extend.get('area', ''),
            'lang': extend.get('lang', ''),
            'year': extend.get('year', ''),
            'by': extend.get('sort', 'time')
        }
        payload = {k: v for k, v in payload.items() if v}
        res = self.smart_request(f'{self.host}/vod-app/vod/list', method='POST', data=payload)
        data = res.get('data', {})
        return {
            'list': self.arr2vods(data.get('data', [])),
            'page': int(pg),
            'pagecount': data.get('totalPageCount', 1)
        }

    def detailContent(self, ids):
        payload = {
            'tid': '',
            'timestamp': str(int(time.time())),
            'vodId': str(ids[0])
        }
        res = self.smart_request(f'{self.host}/vod-app/vod/info', method='POST', data=payload)
        data = res.get('data', {})
        show, play_urls = [], []
        if 'vodSources' in data:
            data['vodSources'].sort(key=lambda x: x.get('sort', 0))
            for i in data['vodSources']:
                urls = []
                if 'vodPlayList' in i and 'urls' in i['vodPlayList']:
                    for j in i['vodPlayList']['urls']:
                        urls.append(f"{j['name']}${i['sourceCode']}@{j['url']}")
                play_urls.append('#'.join(urls))
                show.append(i['sourceName'])
        video = {
            'vod_id': data['vodId'],
            'vod_name': data['vodName'],
            'vod_pic': data['vodPic'],
            'vod_remarks': data.get('vodRemark', ''),
            'vod_year': data.get('vodYear', ''),
            'vod_area': data.get('vodArea', ''),
            'vod_actor': data.get('vodActor', ''),
            'vod_content': data.get('vodContent', ''),
            'vod_play_from': '$$$'.join(show),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': data.get('vodClass', '')
        }
        return {'list': [video]}

    def searchContent(self, key, quick, pg='1'):
        payload = {
            'key': key,
            'limit': '20',
            'page': str(pg),
            'timestamp': str(int(time.time()))
        }
        res = self.smart_request(f'{self.host}/vod-app/vod/segSearch', method='POST', data=payload)
        data = res.get('data', {})
        return {'list': self.arr2vods(data.get('data', [])), 'page': int(pg)}

    def playerContent(self, flag, vid, vip_flags):
        jx = 0
        source_code, raw_url = vid.split('@', 1)
        payload = {
            'sourceCode': source_code,
            'timestamp': str(int(time.time())),
            'urlEncode': raw_url
        }
        try:
            res = self.smart_request(f'{self.host}/vod-app/vod/playUrl', method='POST', data=payload)
            url = res.get('data', {}).get('url', raw_url)
        except Exception:
            url = None
        if not url:
            url = raw_url
            if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', url):
                jx = 1
        return {'jx': jx, 'parse': 0, 'url': url, 'header': {'User-Agent': self.headers['User-Agent']}}

    def rsa_public_decrypt(self, ciphertext_base64):
        pub_key_str = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw4qpeOgv+MeXi57MVPqZF7SRmHR3FUelCTfrvI6vZ8kgTPpe1gMyP/8ZTvedTYjTDMqZBmn8o8Ym98yTx3zHaskPpmDR80e+rcRciPoYZcWNpwpFkrHp1l6Pjs9xHLXzf3U+N3a8QneY+jSMvgMbr00DC4XfvamfrkPMXQ+x9t3gNcP5YtuRhGFREBKP2q20gP783MCOBFwyxhZTIAsFiXrLkgZ97uaUAtqW6wtKR4HWpeaN+RLLxhBdnVjuMc9jaBl6sHMdSvTJgAajBTAd6LLA9cDmbGTxH7RGp//iZU86kFhxGl5yssZvBcx/K95ADeTmLKCsabexZVZ0Fu3dDQIDAQAB\n-----END PUBLIC KEY-----"
        key = RSA.import_key(pub_key_str)
        ciphertext = base64.b64decode(ciphertext_base64)
        c = bytes_to_long(ciphertext)
        m = pow(c, key.e, key.n)
        m_bytes = long_to_bytes(m)
        m_bytes = m_bytes.rjust(256, b'\x00')
        try:
            sep_idx = m_bytes.index(b'\x00', 2)
            return m_bytes[sep_idx + 1:].decode('utf-8')
        except:
            return m_bytes.decode('utf-8', 'ignore').strip()

    def arr2vods(self, arr):
        return [{
            'vod_id': j['id'],
            'vod_name': j['name'],
            'vod_pic': j['vodPic'],
            'vod_remarks': j.get('vodRemarks', ''),
            'vod_year': j.get('vodYear', ''),
            'vod_content': j.get('vodBlurb', '')
        } for j in arr]