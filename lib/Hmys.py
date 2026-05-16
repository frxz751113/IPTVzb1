# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base.spider import Spider
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
import re,sys,time,json,base64,secrets,hashlib,urllib3
from urllib.parse import quote,unquote,urljoin,urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,play_header,host,play_domain,proxyurl,encrypt_domain = {
        'User-Agent': 'Android',
        'Connection': 'Keep-Alive',
        'Accept': 'application/vnd.yourapi.v1.full+json',
        'Accept-Encoding': 'gzip',
        'Device-Id': '',
        'Screen-Width': '2670',
        'Channel': 'guan',
        'Cur-Time': '',
        'Mob-Mfr': 'xiaomi',
        'prefersex': '1',
        'Mob-Model': 'xiaomi',
        'token': '',
        'Sys-Release': '15',
        'appid': '',
        'Version-Code': '',
        'Sys-Platform': 'Android',
        'Screen-Height': '1200',
        'timestamp': ''
    },{'User-Agent': 'Mozi'},'','','',''

    def init(self, extend=''):
        try:
            ext = json.loads(extend.strip())
            host = ext.get('host').rstrip('/')
            if not re.match(r'^https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(:\d+)?/?$', host): return
            appid = ext['app_id']
            deviceid = ext.get('deviceid')
            version_code = ext['versionCode']
            channel = ext['UMENG_CHANNEL']
            self.encrypt_domain = ext.get('EncryptDomain','vT1RQRz8YzlzTgN26pIXNJ7Mi65juwSP')
            if not(appid and version_code and channel): return
            if deviceid:
                if not self.is_valid_android_id(deviceid): return
            else:
                deviceid_cache_key = f'Hmys_deviceid_{appid}_{channel}'
                deviceid = self.getCache(deviceid_cache_key)
                if not deviceid:
                    deviceid = self.device_id()
                    self.setCache(deviceid_cache_key,deviceid)
            self.host = host
            self.headers['appid'] = appid
            self.headers['Channel'] = channel
            self.headers['Device-Id'] = deviceid
            self.headers['Version-Code'] = version_code
            try:
                self.proxyurl = f'{self.getProxyUrl(True)}&type=hmys'
            except Exception:
                self.proxyurl = 'http://127.0.0.1:9978/proxy?do=py&type=hmys'
            self.login(host)
        except Exception:
            return

    def homeContent(self, filter):
        if not self.host: return None
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        response = self.post(f'{self.host}/api/block/category_type', headers=headers, verify=False).json()
        data = json.loads(self.des3(response['data']))
        class_list = []
        for item in data['result']:
            class_list.append({ 'type_id': item['type_pid'], 'type_name': item['type_name']})
        filters_dict = {}
        for item in data['result']:
            type_id = item['type_pid']
            cate_list = [cate.strip() for cate in item['cate'].split(',')]
            cate_values = [{'n': cate, 'v': cate} for cate in cate_list]
            area_list = [area.strip() for area in item['area'].split(',')]
            area_values = [{'n': area, 'v': area} for area in area_list]
            year_list = [year.strip() for year in item['year'].split(',')]
            year_values = [{'n': year, 'v': year} for year in year_list]
            order_list = [order.strip() for order in item['order'].split(',')]
            order_values = [{'n': order, 'v': order} for order in order_list]
            filters_dict[str(type_id)] = [
                {'key': 'class', 'name': '类型', 'value': cate_values},
                {'key': 'area', 'name': '地区', 'value': area_values},
                {'key': 'year', 'name': '年份', 'value': year_values},
                {'key': 'sort', 'name': '排序', 'value': order_values}
            ]
        return {'class': class_list, 'filters': filters_dict}

    def homeVideoContent(self):
        if not self.host: return None
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        response = self.post(f'{self.host}/api/nav/list', headers=headers,verify=False).json()
        data = self.des3(response['data'])
        result = json.loads(data)['result']
        if not result: return None
        classes, videos, recommend_id = [], [], ''
        for i in result:
            if isinstance(i, dict):
                if i.get('nav_name') == '推荐':
                    recommend_id = i.get('nav_id')
                    break
        headers['timestamp'] = self.timestamp()
        response2 = self.post(f'{self.host}/api/nav/index',data={'nav_id': recommend_id or '253'}, headers=headers, verify=False).json()
        data2 = self.des3(response2['data'])
        result2 = json.loads(data2)['result']
        for item in result2:
            if not isinstance(item, dict):
                continue
            for block in item.get('block_list', []):
                if not isinstance(block, dict):
                    continue
                for vod in block.get('vod_list', []):
                    if vod.get('type_pid') != 1:
                        remark = f"{vod['serial']}集全" if vod.get('is_end') == 1 else f"更新至{vod['serial']}集"
                    else:
                        remark = f"评分：{vod['score']}"
                    videos.append({
                        'vod_id': vod['vod_id'],
                        'vod_name': vod['title'],
                        'vod_pic': vod['pic'],
                        'vod_remarks': remark
                    })
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, ext):
        if not self.host: return None
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        payload = {
            'area': ext.get('area','全部'),
            'cate': ext.get('class','全部'),
            'type_pid': tid,
            'year': ext.get('year','全部'),
            'length': '12',
            'page': pg,
            'order': ext.get('sort','最热')
        }
        response = self.post(f'{self.host}/api/block/category', data=payload, headers=headers, verify=False).json()
        data = json.loads(self.des3(response['data']))
        videos = []
        for i in data.get('result',[]):
            if i.get('type_pid') != 1:
                remark = f"{i['serial']}集全" if i.get('is_end') == 1 else f"更新至{i['serial']}集"
            else:
                remark = f"评分：{i['score']}"
            videos.append({
                'vod_id': i['vod_id'],
                'vod_name': i['title'],
                'vod_pic': i['pic'],
                'vod_remarks': remark
            })
        return {'list': videos, 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        if not self.host: return None
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        payload = {'type_pid': "0", 'kw': key, 'pn': pg}
        response = self.post(f'{self.host}/api/search/result', data=payload, headers=headers, verify=False).json()
        data = json.loads(self.des3(response['data']))
        videos = []
        for i in data.get('result',[]):
            vod_remarks = f"{i['serial']}集" if i['type_pid'] != '1' else i['tags']
            if i['short_video'] == 1:
                vod_remarks += ',短剧'
            videos.append({
                'vod_id': i['vod_id'],
                'vod_name': i['title'],
                'vod_pic': i['pic'],
                'vod_remarks': vod_remarks,
                'vod_year': i['year']
            })
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        if not self.host: return None
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        payload = {'vod_id': ids[0]}
        response = self.post(f'{self.host}/api/vod/info', data=payload, headers=headers, verify=False).json()
        data = self.des3(response['data'])
        result = json.loads(data)['result']
        play_urls = []
        for i in result['map_list']:
            if isinstance(i, dict):
                play_urls.append(f"{i['title']}${ids[0]}@{i['id']}@{i['collection']}")
        video = {
            'vod_id': result['vod_id'],
            'vod_name': result['title'],
            'vod_pic': result['pic'],
            'vod_remarks': result['remarks'],
            'vod_year': result['year'],
            'vod_area': result['area'],
            'vod_actor': result['actor'],
            'vod_director': result['director'],
            'vod_content': result['intro'],
            'vod_play_from': '河马',
            'vod_play_url': '#'.join(play_urls),
            'type_name': result['tags']
        }
        return {'list': [video]}

    def playerContent(self, flag, id, vipflags):
        video_id, vod_map_id, collection = id.split('@', 2)
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        payload = {
            'xz': "0",
            'vod_map_id': vod_map_id,
            'vod_id': video_id,
            'collection': collection
        }
        response = self.post(f'{self.host}/api/vod/play_url', data=payload, headers=headers, verify=False).json()
        data = self.des3(response['data'])
        result = json.loads(data)['result']
        try:
            ck = base64.b64decode(result['ck']).decode('utf-8')
        except Exception:
            ck = result['ck']
        vod_url = result['vod_url']
        check_url = result.get('check_url')
        url = check_url or self.proxyurl + '&url=' + quote(f"{vod_url}?{ck}", safe='')
        return {'jx': '0', 'parse': '0', 'url': url, 'header': self.play_header}

    def localProxy(self, params):
        if params['type'] == "hmys":
            return self.hema_m3u8_proxy(params)
        return None

    def login(self, host):
        if self.headers['token'] and self.play_domain: return
        self.headers['Cur-Time'] = self.timestamp()
        headers = self.headers.copy()
        headers['timestamp'] = self.timestamp()
        response = self.post(f'{host}/api/user/init', data={'password': '','account': ''}, headers=headers, verify=False).json()
        data = self.des3(response['data'])
        result = json.loads(data)['result']
        self.headers['token'] = result['user_info']['token']
        self.play_domain = result['sys_conf']['play_domain']
        self.host = result['sys_conf']['host_main']
        if not(self.headers['token'] or self.play_domain or self.play_domain):
            self.host = ''
            return
        headers['timestamp'] = self.timestamp()
        self.post(f'{self.host}/api/stats/login', data={'action': '6'}, headers=headers, verify=False)

    def hema_m3u8_proxy(self, params):
        url = unquote(params['url'])
        if params.get('format') == "ts":
            data = {"Location": url + self.hls_sign(url), "Content-Length": "0"}
            return [302, "text/html; charset=utf-8", None, data]
        else:
            data = self.hema_modify_m3u8(url)
            return [200, "application/vnd.apple.mpegurl", data]

    def hema_modify_m3u8(self, raw_url):
        ck = raw_url.split('?')[1]
        m3u8_url = raw_url + self.hls_sign(raw_url)
        m3u8_content = self.fetch(m3u8_url, headers=self.play_header, verify=False).text
        content = m3u8_content if m3u8_content is not None else self.m3u8_content
        if content is None: raise ValueError("M3U8为空")
        parsed = urlparse(raw_url)
        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rsplit('/', 1)[0]}/"
        output_lines = []
        for line in content.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                if not stripped_line.startswith(('http://', 'https://')):
                    full_url = urljoin(base, stripped_line)
                else:
                    full_url = stripped_line
                signed_url = self.proxyurl + f'&format=ts&url=' + quote(full_url + '&' + ck,safe='')
                output_lines.append(signed_url)
            else:
                output_lines.append(line)
        return '\n'.join(output_lines)

    def des3(self, base64_ciphertext):
        try:
            ciphertext = base64.b64decode(base64_ciphertext)
            key_bytes = 'ZT8g6QH2kS3Xj7G5wG4JtU1F'.encode('utf-8')
            iv_bytes = '51518888'.encode('utf-8')
            cipher = DES3.new(key_bytes, DES3.MODE_CBC, iv_bytes)
            plaintext_bytes = unpad(cipher.decrypt(ciphertext), DES3.block_size)
            return plaintext_bytes.decode('utf-8')
        except Exception as e:
            return None

    def hls_sign(self, url):
        replaceDomain = self.play_domain
        hex_time = self.hex_time()
        if '?' in url: url = url.split('?')[0]
        data = url.replace(replaceDomain, self.encrypt_domain) + hex_time
        data_hash = hashlib.md5()
        data_hash.update(data.encode('utf-8'))
        return f"&wsSecret={data_hash.hexdigest()}&wsTime={hex_time}"

    def is_valid_android_id(self, android_id):
        if not isinstance(android_id, str): return False
        return bool(re.fullmatch(r'^[0-9a-f]{16}$', android_id))

    def device_id(self):
        return ''.join(secrets.choice('0123456789abcdef') for _ in range(16))

    def timestamp(self):
        return str(int(time.time() * 1000))

    def hex_time(self):
        return hex(int(time.time()))[2:]

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass