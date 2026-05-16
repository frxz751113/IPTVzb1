# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import unpad, pad
import re,sys,time,json,base64,urllib3,hashlib,binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host,key,iv,ckkey,ckiv,config = {
        'User-Agent': "Dart/2.10 (dart:io)",
        'Accept-Encoding': "gzip",
    }, '','','','','',{}

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
        response = self.fetch(f'{self.host}/sk-api/type/list', headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        classes = []
        for i in data:
            if isinstance(i,dict):
                classes.append({'type_id': i['type_id'], 'type_name': i['type_name']})
        return {'class': classes}

    def homeVideoContent(self):
        response = self.fetch(f'{self.host}/sk-api/vod/list?page=1&limit=12&type=randomlikeindex&area=&lang=&year=&mtype=',headers=self.headers, verify=False).text
        data_ = self.sk_decrypt(response)
        data = json.loads(data_)['data']
        return {'list': data}

    def categoryContent(self, tid, pg, filter, extend):
        response = self.fetch(f"{self.host}/sk-api/vod/list?typeId={tid}&page={pg}&limit=18&type={extend.get('sort','updateTime')}&area={extend.get('area','')}&lang={extend.get('lang','')}&year={extend.get('year','')}&mtype=&extendtype=", headers=self.headers, verify=False).text
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
        jx,url = 0,''
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
        if direct_json or not(id.startswith('http')) or not(re.match(r'https?:\/\/.*\.(m3u8|mp4|flv)', id)):
            try:
                response = self.fetch(f'{self.host}/sk-api/vod/skjson?url={id}&skjsonindex=0', headers=self.headers, verify=False).text
                data_ = self.sk_decrypt(response)
                data = json.loads(data_)['data']
                url = data.get('url')
                if not url.startswith('http'):
                    if url == '' and (re.match(r'https?:\/\/.*\.(m3u8|mp4|flv)', id) or direct_link):
                        jx, url = 0, id
                    else:
                        jx,url = 1, id
            except Exception:
                jx, url = 1, id
        if url == '' and (re.match(r'https?:\/\/.*\.(m3u8|mp4|flv)', id) or direct_link):
            jx, url = 0, id
        return { 'jx': jx, 'parse': '0', 'url': url, 'header': {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}}

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
