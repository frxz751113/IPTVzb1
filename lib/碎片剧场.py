# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。
# 'https://speed.rouzwv.com/papaya/papaya-file/files/download/'

from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import pad
import sys,json,time,random,urllib3,binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,host,res_api,cache_token_key = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'authorization': '',
        'uuid': ''
    }, '','https://speed.howdbm.com/papaya/papaya-file/files/download/','com.sha.fragment_5d091235ac87508f_token'

    def init(self, extend=''):
        self.host = 'https://free-api.bighotwind.cc'
        self.login()

    def homeContent(self, filter):
        if not self.host: return None
        response = {}
        for i in range(2):
            response = self.fetch(f'{self.host}/papaya/papaya-api/theater/tags', headers=self.headers, verify=False).json()
            if response['code'] == 401:
                self.re_login()
            else:
                break
        classes = []
        for i in response.get('data',[]):
            if isinstance(i,dict):
                classes.append({'type_id': i['id'], 'type_name': i['text_val']})
        return {'class': classes}

    def homeVideoContent(self):
        if not self.host: return None
        response = {}
        for i in range(2):
            response = self.fetch(f'{self.host}/papaya/papaya-api/videos/page?type=5&pageNum=1&pageSize=12',headers=self.headers, verify=False).json()
            if response['code'] == 401:
                self.re_login()
            else:
                break
        videos = []
        for i in response.get('list',[]):
            videos.append({
                'vod_id': f"{i['itemId']}@{i['videoCode']}@{i['tags']}",
                'vod_name': i['title'],
                'vod_pic': f"{self.res_api}{i['imageKey']}/{i['imageName']}",
                'vod_remarks': i['tags'],
                'vod_content': i['content']
            })
        return {'list': videos, 'total': response['total']}

    def categoryContent(self, tid, pg, filter, extend):
        if not self.host: return None
        response ={}
        for i in range(2):
            response = self.fetch(f'{self.host}/papaya/papaya-api/videos/page?type=5&tagId={tid}&pageNum={pg}&pageSize=12', headers=self.headers, verify=False).json()
            if response['code'] == 401:
                self.re_login()
            else:
                break
        videos = []
        for i in response.get('list',[]):
            videos.append({
                'vod_id': f"{i['itemId']}@{i['videoCode']}@{i['tags']}",
                'vod_name': i['title'],
                'vod_pic': f"{self.res_api}{i['imageKey']}/{i['imageName']}",
                'vod_remarks': i['tags'],
                'vod_content': i['content']
            })
        return {'list': videos, 'total': response['total']}

    def searchContent(self, key, quick, pg='1'):
        if not self.host: return None
        response = {}
        for i in range(2):
            response = self.fetch(f'{self.host}/papaya/papaya-api/videos/page?type=5&search={key}&pageNum={pg}&pageSize=12', headers=self.headers, verify=False).json()
            if response['code'] == 401:
                self.re_login()
            else:
                break
        videos = []
        for i in response.get('list',[]):
            videos.append({
                'vod_id': f"{i['itemId']}@{i['videoCode']}@{i['tags']}",
                'vod_name': i['title'],
                'vod_pic': f"{self.res_api}{i['imageKey']}/{i['imageName']}",
                'vod_remarks': i['tags'],
                'vod_content': i['content']
            })
        return {'list': videos, 'total': response['total']}

    def detailContent(self, ids):
        if not self.host: return None
        item_id, video_code, tags = ids[0].split('@',2)
        response = {}
        for i in range(2):
            response = self.fetch(f'{self.host}/papaya/papaya-api/videos/info?videoCode={video_code}&itemId={item_id}',headers=self.headers, verify=False).json()
            if response['code'] == 401:
                self.re_login()
            else:
                break
        data = response.get('data')
        if not data: return None
        play_urls = []
        episodes_list = data.get('episodesList',[])
        for i in episodes_list:
            if isinstance(i, dict):
                resolutionList = i['resolutionList'][0]
                play_urls.append(f"{i['episodes']}${resolutionList['fileKey']}/{resolutionList['fileName']}")
        video = {
            'vod_id': ids[0],
            'vod_name': data['title'],
            'vod_pic': f"{self.res_api}{data['imageKey']}/{data['imageName']}",
            'vod_remarks': f"集数:\u2005{len(episodes_list)}  时长:\u2005{self.convert_minutes(data['duration'])}",
            'vod_content': data['content'],
            'type_name': tags,
            'vod_play_from': '碎片剧场',
            'vod_play_url': '#'.join(play_urls),
        }
        return {'list': [video]}

    def playerContent(self, flag, id, vipflags):
        if not id.startswith('http'): id = f'{self.res_api}{id}'
        return { 'jx': 0, 'parse': 0, 'url': id, 'header': {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; Build/3480d86.0)','Connection': 'Keep-Alive','Accept-Encoding': 'identity'}}

    def login(self):
        try:
            cache_uuid_key = 'com.sha.fragment_5d091235ac87508f_uuid'
            uuid = self.getCache(cache_uuid_key)
            if not uuid:
                uuid = self.generate_android_id()
                self.setCache(cache_uuid_key,uuid)
            headers = self.headers.copy()
            headers['key'] = self.encrypt(str(int(time.time() * 1000)))
            headers['content-type'] = 'application/json; charset=utf-8'
            token = self.getCache(self.cache_token_key)
            if not token:
                response = self.post(f'{self.host}/papaya/papaya-api/oauth2/uuid', data=json.dumps({"openId":uuid}), headers=headers, verify=False).json()
                token = response['data']['token']
                if not token:
                    self.host = None
                    return
                self.setCache(self.cache_token_key,token)
            self.headers['authorization'] = token
            self.headers['uuid'] = uuid
            print(self.headers)
        except Exception:
            self.host = None

    def convert_minutes(self,total_minutes):
        try:
            total_minutes = int(total_minutes)
        except (ValueError, TypeError):
            return total_minutes
        if total_minutes == 0:
            return total_minutes
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if hours == 0:
            return f"{minutes}分钟"
        elif minutes == 0:
            return f"{hours}小时"
        else:
            return f"{hours}小时{minutes}分钟"

    def encrypt(self, plaintext):
        cipher = AES.new("p0sfjw@k&qmewu#w".encode('utf-8'), AES.MODE_ECB)
        data_bytes = plaintext.encode('utf-8')
        block_size = AES.block_size
        padded_data = pad(data_bytes, block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        return binascii.hexlify(encrypted_bytes).decode('utf-8')

    def generate_android_id(self):
        hex_chars = '0123456789abcdef'
        return ''.join(random.choice(hex_chars) for _ in range(16))

    def re_login(self):
        self.delCache(self.cache_token_key)
        self.login()

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