# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base.spider import Spider
from Crypto.Cipher import ARC4,AES
from urllib.parse import quote_plus
from Crypto.Util.Padding import unpad
import re,sys,time,uuid,json,base64,urllib3,hashlib,secrets,binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers = {
        'User-Agent': "Dalvik/2.1.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }
    headers2 = {**headers}
    client_mode,max_client,app_id,pg_url,yry_url,client,base_path,pg_key,yry_key,token,user,pwd,markcode,login_mode,app_name,model,cache_key = 0,2,'','','','','','','','','','','','','','',''

    def init(self, extend=''):
        try:
            ext = json.loads(extend)
        except Exception:
            ext = {}
        self.user = ext.get('username')
        self.pwd = ext.get('password')
        self.markcode = ext.get('markcode')
        self.app_name = ext.get('app_name', 'xiaomi')
        self.model = ext.get('model', 'xiaomi')
        cos_url = ext.get('CosUrl', 'http://2025-1329689796.cos.ap-guangzhou.myqcloud.com/kanke/app1.json')
        self.cache_key = hashlib.md5(cos_url.encode('utf-8')).hexdigest()
        try:
            number1 = 'No00000'
            number = self.md5(number1)
            number_key = self.md5(f'{number1}SmtEk1')
            payload = {'t': str(int(time.time())), 'key': self.rc4_encrypt(number, number_key)}
            self.app_id = '10000'
            res = self.fetch(cos_url, headers=self.headers, verify=False).json()
            notice = res['msg']['notice']
            main_host = self.decode(notice['content'])
            self.headers2['Authorization'] = self.decode(notice['type'])
            response = self.post(f'{main_host}?app={self.app_id}', data=payload, headers=self.headers2, verify=False).json()
            data = response['data']
            maink = self.rc4_decrypt(data['Maink'], number_key)
            self.pg_key = self.rc4_decrypt(data['pg'], maink)
            self.yry_key = self.rc4_decrypt(data['yry'], maink)
            key_time = self.rc4_decrypt(data['MT'], maink)
            pg_raw_url = data['pgUrl']
            yry_raw_url = data['yryUrl']
            aes_key = self.base64_encode(f"{key_time}{pg_raw_url[:14]}")
            aes_iv = self.base64_encode(f'{key_time}{yry_raw_url[:2]}').ljust(16)
            pg_url = self.aes_decrypt(self.base64_decode(pg_raw_url[32:]), aes_key, aes_iv)
            yry_url = self.aes_decrypt(self.base64_decode(yry_raw_url[16:]), aes_key, aes_iv)
            self.base_path = self.rc4_decrypt(data['HOST'])
            self.client = self.rc4_decrypt(data['newClient'])
            self.login_mode = data.get('Login',4)
            self.pg_url = pg_url
            self.yry_url = yry_url
        except Exception:
            self.pg_url = ''

    def homeContent(self, filter):
        if not self.pg_url: return None
        response = self.fetch(f'{self.pg_url}/api.php/{self.base_path}/Category?{self.sign()}', headers=self.headers2, verify=False).text
        try:
            data = self.rc4_decrypt(response)
            data2 = json.loads(data)
        except Exception:
            data2 = json.loads(response)
        classes = []
        for i in data2:
            if isinstance(i,dict) and i['type_status'] == 1:
                classes.append({'type_id': i['type_en'], 'type_name': i['type_name']})
        return {'class': classes}

    def homeVideoContent(self):
        if not self.pg_url: return None
        response = self.fetch(f'{self.pg_url}/api.php/{self.base_path}/top?{self.sign()}', headers=self.headers2, verify=False).json()
        videos = self.arr2vods(response['data'])
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if not self.pg_url: return None
        response = self.fetch(f'{self.pg_url}/api.php/{self.base_path}/vod/?ac=list&class={tid}&page={pg}&{self.sign()}', headers=self.headers2, verify=False).text
        try:
            data = self.rc4_decrypt(response)
            data2 = json.loads(data)
        except Exception:
            data2 = json.loads(response)
        videos = self.arr2vods(data2['data'])
        return {'list': videos,'pagecount':data2['totalpage'], 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        if not self.pg_url: return None
        response = self.fetch(f'{self.pg_url}/api.php/{self.base_path}/So/?ac=list&zm={key}&page={pg}&{self.sign()}', headers=self.headers2, verify=False).text
        try:
            data = self.rc4_decrypt(response)
            data2 = json.loads(data)
        except Exception:
            data2 = json.loads(response)
        videos = self.arr2vods(data2['data'])
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        if not self.pg_url: return None
        self.client_mode = 0
        if not self.token: self.auto_logon()
        req_data = f'token={self.token}&t={int(time.time())}'
        payload = {'data': self.rc4_encrypt(req_data),'sign': self.md5(f'{req_data}&{self.pg_key}')}
        res = self.post(f'{self.yry_url}/api.php?app={self.app_id}&act=motion',data=payload, headers=self.headers2, verify=False).json()
        self.client_mode = int(res['msg']['Clientmode'])
        if self.client_mode == 0 and res['msg']['Try'] != 1: return None
        response = self.fetch(f'{self.pg_url}/api.php/{self.base_path}/vod/{ids[0]}&{self.sign()}', headers=self.headers2, verify=False).text
        try:
            data2 = json.loads(response)
        except Exception:
            data = self.rc4_decrypt(response)
            data2 = json.loads(data)
        try:
            player_ = self.rc4_decrypt(data2['player'])
            player = json.loads(player_)
        except Exception:
            player = json.loads(response['player'])
        vod_name = data2['title']
        shows, play_urls = [], []
        for show, raw_urls in data2['videolist'].items():
            name = None
            for i in player:
                if i['from'] == show and i['from'] != i['show']:
                    name = i['show']
                    break
            urls = []
            for j in raw_urls:
                title = j['title']
                series = quote_plus(f"{vod_name}-{title}")
                urls.append(f"{title}${series}@{j['url']}")
            play_urls.append('#'.join(urls))
            if name:
                shows.append(f'{name}\u2005({show})')
            else:
                shows.append(show)
        video = {
            'vod_id': ids[0],
            'vod_name': vod_name,
            'vod_pic': data2['img_url'],
            'vod_remarks': data2['trunk'],
            'vod_year': data2['pubtime'],
            'vod_area': ','.join(data2['area']),
            'vod_actor': ','.join(data2['actor']),
            'vod_director': ','.join(data2['director']),
            'vod_content': data2['intro'],
            'vod_play_from': '$$$'.join(shows),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': ','.join(data2['type'])
        }
        return {'list': [video]}

    def playerContent(self, flag, vid, vip_flags):
        jx,url = 0,''
        series, raw_url = vid.split('@',1)
        self.client_mode = 1
        base_path = f'&account={self.user}&password={self.pwd}&series={series}&edition=1.0'
        cont = 0
        for i in range(1,4):
            if cont > self.max_client:
                break
            try:
                if self.client.startswith('http'):
                    if i == 1:
                        path = f'{self.client}/?url={raw_url}'
                    else:
                        path = f'{self.client}{i}/?url={raw_url}'
                    if self.client_mode == 1:
                        payload = {'app': self.app_id,'key': self.rc4_encrypt(base_path),'':''}
                        response = self.post(path, data=payload, headers=self.headers2, verify=False).text
                    else:
                        response = self.post(f'{path}&app={self.app_id}{base_path}', headers=self.headers2, verify=False).text
                    try:
                        data = self.rc4_decrypt(response)
                        data2 = json.loads(data)
                    except Exception:
                        data2 = json.loads(response)
                    self.max_client = int(data2.get('maxClient'))
                    play_url = data2['url']
                    if play_url.startswith('http'):
                        url = play_url
                        break
                cont += 1
            except Exception:
                url = ''
                cont += 1
                continue
        if not url:
            try:
                play_url = self.rc4_decrypt(raw_url)
                if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', play_url):
                    jx, url = 1, play_url
            except Exception:
                pass
        return { 'jx': jx, 'parse': 0, 'url': url, 'header': {'User-Agent':'Windows'}}

    def auto_logon(self):
        if not self.pg_url: return
        if self.user and self.pwd and self.markcode:
            user, pwd, markcode = self.user, self.pwd, self.markcode
        else:
            account_cache_key = f'smtv_account_{self.cache_key}_V73xfmWkXa'
            try:
                account = self.getCache(account_cache_key)
                user, pwd, markcode = account['username'], account['password'], account['markcode']
            except Exception:
                user, pwd, markcode = None, None, None
            if not (user and pwd and markcode):
                if self.login_mode == 2:
                    random_account = self.android_id()
                    user, pwd, markcode = random_account, random_account, random_account
                elif self.login_mode == 3:
                    random_account = self.mac()
                    user, pwd, markcode = random_account, random_account, random_account
                else:
                    random_account = self.uuid_number()
                    user, pwd, markcode = random_account, random_account, random_account
                self.register(user, pwd, markcode)
                self.setCache(account_cache_key, {'username': user, 'password': pwd, 'markcode': markcode})
        self.login(user, pwd, markcode)

    def login(self, user,pwd,markcode):
        if not self.pg_url: return
        req_data = f'account={user}&password={pwd}&markcode={markcode}&t={int(time.time())}'
        payload = {'data': self.rc4_encrypt(req_data),'sign': self.md5(f'{req_data}&{self.pg_key}')}
        response = self.post(f'{self.yry_url}/api.php?app={self.app_id}&act=user_logon', data=payload, headers=self.headers2, verify=False).json()
        msg = response['msg']
        try:
            data = self.rc4_decrypt(msg, self.yry_key)
            data2 = json.loads(data)
        except Exception:
            data2 = json.loads(msg)
        self.token = data2['token']
        self.user = user
        self.pwd = pwd

    def register(self, user,pwd,markcode):
        if not self.pg_url: return
        user_host = self.fetch(f'{self.yry_url}/ip.json', headers=self.headers).text
        req_data = f'user={user}&password={pwd}&markcode={markcode}&t={int(time.time())}&name={self.app_name}&phone={self.model}'
        payload = {'data': self.rc4_encrypt(req_data),'sign': self.md5(f'{req_data}&{self.pg_key}')}
        self.post(f'http://{user_host}/api.php?app={self.app_id}&act=user_reg', data=payload, headers=self.headers2, verify=False)

    def arr2vods(self, arr):
        videos = []
        if isinstance(arr,list):
            for i in arr:
                videos.append({
                    'vod_id': i.get('tjurl', i.get('nextlink')),
                    'vod_name': i.get('tjinfo', i.get('title')),
                    'vod_pic': i.get('tjpicurl', i.get('pic')),
                    'vod_remarks': i.get('state'),
                    'vod_year': None
                })
        return videos

    def rc4_encrypt(self, plaintext, key=None):
        if not key: key = self.yry_key
        key_bytes = key.encode('utf-8')
        plaintext_bytes = plaintext.encode('utf-8')
        cipher = ARC4.new(key_bytes)
        ciphertext = cipher.encrypt(plaintext_bytes)
        return binascii.hexlify(ciphertext).decode('utf-8')

    def rc4_decrypt(self,ciphertext_hex, key=None):
        if not key: key = self.pg_key
        key_bytes = key.encode('utf-8')
        ciphertext_bytes = binascii.unhexlify(ciphertext_hex)
        cipher = ARC4.new(key_bytes)
        plaintext_bytes = cipher.decrypt(ciphertext_bytes)
        return plaintext_bytes.decode('utf-8')

    def aes_decrypt(self, data, key, iv):
        try:
            encrypted_data = base64.b64decode(data)
            cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception:
            raise ValueError

    def uuid_number(self):
        uuid_bytes = uuid.uuid4().bytes
        result = []
        for i in range(9):
            value = uuid_bytes[i] % 10
            result.append(str(value))
        return ''.join(result)

    def mac(self):
        mac_bytes = [secrets.randbits(8) for _ in range(6)]
        return ''.join(f"{byte:02X}" for byte in mac_bytes)

    def android_id(self):
        return ''.join(secrets.choice('0123456789abcdef') for _ in range(16))

    def sign(self):
        timestamp = str(int(time.time()))
        return f'key={self.rc4_encrypt(timestamp, timestamp)}&tt={timestamp}'

    def base64_encode(self, data):
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def base64_decode(self, data):
        return base64.b64decode(data.encode('utf-8')).decode('utf-8')

    def decode(self, data):
        return self.base64_decode(self.base64_decode(data[16:]))

    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

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