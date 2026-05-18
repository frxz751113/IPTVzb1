# -*- coding: utf-8 -*-
# 本资源收集自互联网，仅供个人学习与测试用途。
# 严禁用于商业目的，请于下载后 24 小时内删除。

from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import unpad, pad
import re,sys,time,json,base64,urllib3,hashlib,binascii
from concurrent.futures import ThreadPoolExecutor, as_completed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': "Dart/2.10 (dart:io)",
            'Accept-Encoding': "gzip",
        }
        self.host = ''
        self.key = ''
        self.iv = ''
        self.ckkey = ''
        self.ckiv = ''
        self.config = {}

    def init(self, extend=""):
        try:
            ext = json.loads(extend.strip())
            host = ext['host']
            self.key = ext['key']
            self.iv = ext['iv']
            self.ckkey = ext.get('ckkey','ygcnbcrvaervztmw')
            self.ckiv = ext.get('ckiv','1212164105143708')
            if not host.startswith('http'):
                return None
            if not re.match(r'^https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(:\d+)?/?$', host):
                host = self.fetch(host,headers=self.headers,verify=False).text.strip()
            self.host = host.rstrip('/')
            if len(self.key) != 16 or len(self.iv) != 16:
                self.host = ''
                return None
            payload = {
                "sign": hashlib.md5(f'{self.key}{self.iv}'.encode('utf-8')).hexdigest(),
                "ck": self.ck_encrypt(f'{self.host}##5483##{int(time.time() * 1000)}##ckzmbc')
            }
            headers = self.headers.copy()
            headers.update({'Content-Type': "application/json",'content-type': "application/json; charset=utf-8"})
            response = self.post(f'{self.host}/get_config', data=json.dumps(payload), headers=headers, verify=False).text
            if response:
                token = self.sk_decrypt(response)
                if token:
                    self.headers['authorization'] = 'Bearer ' + token
            config_ = self.fetch(f'{self.host}/app/config', headers=self.headers, verify=False).text
            config = self.sk_decrypt(config_)
            data = json.loads(config)
            direct_link = data.get('direct_link')
            direct_json_link = data.get('direct_json_link')
            app_trans_name = data.get('app_trans_name')
            if direct_link and isinstance(direct_link, str):
                if '|' in direct_link:
                    direct_link_list = direct_link.split('|')
                else:
                    direct_link_list = [direct_link]
                self.config['direct_link'] = direct_link_list
            if direct_json_link and isinstance(direct_json_link,str):
                if '|' in direct_json_link:
                    direct_json_link_list = direct_json_link.split('|')
                else:
                    direct_json_link_list = [direct_json_link]
                self.config['direct_json_link'] = direct_json_link_list
            if app_trans_name and isinstance(app_trans_name,list):
                self.config['app_trans_name'] = app_trans_name
            return None
        except Exception:
            return None

    def homeContent(self, filter):
        if not self.host: return None
        try:
            response = self.fetch(f'{self.host}/sk-api/type/list', headers=self.headers, verify=False).text
            data_ = self.sk_decrypt(response)
            data = json.loads(data_)['data']
            classes = []
            for i in data:
                if isinstance(i, dict):
                    classes.append({'type_id': i['type_id'], 'type_name': i['type_name']})
        except Exception:
            return {'class': []}
        filters = {}
        def fetch_filter(tid):
            try:
                url = f'{self.host}/sk-api/type/alltypeextend?typeId={tid}'
                resp = self.fetch(url, headers=self.headers, verify=False).text
                decrypted = self.sk_decrypt(resp)
                f_data = json.loads(decrypted)
                if f_data.get('code') == 200 and f_data.get('data'):
                    data_obj = f_data['data']
                    type_filters = []
                    mappings = {
                        'class': ('extendtype', '类型'),
                        'area': ('area', '地区'),
                        'lang': ('lang', '语言'),
                        'year': ('year', '年份')
                    }
                    for api_key, val in mappings.items():
                        filter_key, filter_name = val
                        if data_obj.get(api_key):
                            options = [x.strip() for x in data_obj[api_key].split(',') if x.strip()]
                            if options:
                                value_list = [{'n': '全部', 'v': ''}]
                                for opt in options:
                                    value_list.append({'n': opt, 'v': opt})
                                type_filters.append({'key': filter_key, 'name': filter_name, 'init': '', 'value': value_list})
                    type_filters.append({
                        'key': 'sort',
                        'name': '排序',
                        'init': 'updateTime',
                        'value': [
                            {'n': '最新', 'v': 'updateTime'},
                            {'n': '人气', 'v': 'hot'},
                            {'n': '评分', 'v': 'score'}
                        ]
                    })
                    return str(tid), type_filters
            except Exception:
                pass
            return None
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_filter, c['type_id']) for c in classes]
            for future in as_completed(futures):
                res = future.result()
                if res:
                    filters[res[0]] = res[1]
        return {'class': classes, 'filters': filters}

    def homeVideoContent(self):
        response = self.fetch(f'{self.host}/sk-api/vod/list?page=1&limit=12&type=randomlikeindex&area=&lang=&year=&mtype=',headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        return {'list': data}

    def categoryContent(self, tid, pg, filter, extend):
        sort = extend.get('sort', 'updateTime')
        area = extend.get('area', '')
        lang = extend.get('lang', '')
        year = extend.get('year', '')
        extendtype = extend.get('extendtype', '')
        response = self.fetch(f"{self.host}/sk-api/vod/list?typeId={tid}&page={pg}&limit=18&type={sort}&area={area}&lang={lang}&year={year}&mtype=&extendtype={extendtype}", headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        return {'list': data, 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        response = self.fetch(f"{self.host}/sk-api/search/pages?keyword={key}&page={pg}&limit=10&typeId=-1", headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        return {'list': data, 'page': pg}

    def detailContent(self, ids):
        response = self.fetch(f"{self.host}/sk-api/vod/one?vodId={ids[0]}",headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        return {'list': [data]}

    def playerContent(self, flag, id, vipflags):
        jx,url,direct_link = 0,'',0
        config = self.config
        direct_json_links = config.get('direct_json_link',[])
        direct_links = config.get('direct_link',[])
        direct_json = 0
        for i in direct_json_links:
            if i in id:
                direct_json = 1
        for i in direct_links:
            if i in id and i.startswith('http'):
                direct_link = 1
        if direct_json or not direct_link or not(id.startswith('http')):
            try:
                response = self.fetch(f'{self.host}/sk-api/vod/skjson?url={id}&skjsonindex=0', headers=self.headers, verify=False).text
                data_ = self.sk_decrypt(response)
                data = json.loads(data_)['data']
                play_url = data.get('url')
                if play_url.startswith('http'):
                    url = play_url
            except Exception:
                pass
        if not url:
            url = id
            if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', id):
                jx = 1
        return { 'jx': jx, 'parse': 0, 'url': url, 'header': {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}}

    def ck_encrypt(self, str):
        key = self.ckkey.encode('utf-8')
        iv = self.ckiv.encode('utf-8')
        b64_1 = base64.b64encode(str.encode("utf-8"))
        b64_2 = base64.b64encode(b64_1)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(b64_2, AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        hex_encoded = encrypted_bytes.hex()
        hex_bytes = hex_encoded.encode('utf-8')
        final_ciphertext = base64.b64encode(hex_bytes).decode('utf-8')
        return final_ciphertext

    def sk_decrypt(self,data):
        prefix = "FROMSKZZJM"
        if data.startswith('FROMSKZZJM'):
            try:
                encrypted_hex = data[len(prefix):]
                key = self.key.encode('utf-8')
                iv = self.iv.encode('utf-8')
                encrypted_data = binascii.unhexlify(encrypted_hex)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                return decrypted_data.decode('utf-8')
            except Exception:
                return None
        else:
            return data

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
