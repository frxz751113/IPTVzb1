# coding=utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import datetime
import binascii
import requests
import base64
import hmac
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "http://if2.hifiok.com"

xurl1 = "http://if2.zhenxian.fm"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

class Spider(Spider):
    global xurl
    global xurl1
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def decrypt(self, timestamp):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        protocolver = "zx11"
        sliderid = "4"
        terminaltype = "5"
        data = f"apikey{apikey}protocolver{protocolver}sliderid{sliderid}terminaltye{terminaltype}timestamp{timestamp}"
        signature = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), 'sha1').digest()
        base64_result = base64.b64encode(signature).decode('utf-8')
        return base64_result

    def decrypt_sha1(self, timestamp, value):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        id_value = value
        maxitems = "96"
        protocolver = "zx11"
        startitem = "0"
        type_value = "1"
        data = f"apikey{apikey}id{id_value}maxitems{maxitems}protocolver{protocolver}startitem{startitem}timestamp{timestamp}type{type_value}"
        signature = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), 'sha1').digest()
        base64_result = base64.b64encode(signature).decode('utf-8')
        return base64_result

    def decrypt_sha2(self, timestamp):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        protocolver = "zx11"
        data = f"apikey{apikey}protocolver{protocolver}timestamp{timestamp}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            'sha1'
                             ).digest()
        base64_signature = base64.b64encode(signature).decode('utf-8')
        return base64_signature

    def decrypt_sha4(self, timestamp):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        protocolver = "zx11"
        terminaltype = "0"
        data = f"apikey{apikey}protocolver{protocolver}terminaltype{terminaltype}timestamp{timestamp}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            'sha1'
                            ).digest()
        base64_signature = base64.b64encode(signature).decode('utf-8')
        return base64_signature

    def decrypt_sha3(self, timestamp, value):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        id_value = value
        protocolver = "zx11"
        data = f"apikey{apikey}id{id_value}protocolver{protocolver}timestamp{timestamp}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            'sha1'
                             ).digest()
        base64_signature = base64.b64encode(signature).decode('utf-8')
        return base64_signature

    def decrypt_sha5(self, timestamp):
        secret_key = "6f7ab440b39eba4ac87bfa5576eac999"
        apikey = "0f607264-fc63-38a9-ab9e-13c65db7cd3c"
        protocolver = "zx11"
        maxitems = "96"
        startitem = "0"
        data = f"apikey{apikey}maxitems{maxitems}protocolver{protocolver}startitem{startitem}timestamp{timestamp}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            'sha1'
                            ).digest()
        base64_signature = base64.b64encode(signature).decode('utf-8')
        return base64_signature

    def homeContent(self, filter):
        result = {"class": []}

        current_timestamp = int(datetime.datetime.now().timestamp())
        signature = self.decrypt_sha2(current_timestamp)

        url = f'{xurl}/interface2/ws/tv/index?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&protocolver=zx/1.1&timestamp={str(current_timestamp)}&signature={signature}'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        if detail.status_code == 200:
            data = detail.json()

            data = data['menus']

            skip_patterns = [r'\b5\.1环绕声\b',r'\b厂牌音乐\b']

            for vod in data:

                name = vod['menuname']

                should_skip = any(re.fullmatch(pattern, name) for pattern in skip_patterns)
                if should_skip:
                    continue

                id = vod['menuid']

                result["class"].append({"type_id": id, "type_name": name})

        return result

    def homeVideoContent(self):
        videos = []

        current_timestamp = int(datetime.datetime.now().timestamp())
        signature = self.decrypt(current_timestamp)

        url = f'{xurl}/interface2/ws/content/slider?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&protocolver=zx/1.1&sliderid=4&terminaltye=5&timestamp={str(current_timestamp)}&signature={signature}'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        if detail.status_code == 200:
            data = detail.json()

            data = data['content']

            for vod in data:

                name = vod['albumName']

                id = str(int(vod['contentId'])) + "@" + "456"

                pic = vod['imgUrl']

                remark = vod.get('artistName', '未知')

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        current_timestamp = int(datetime.datetime.now().timestamp())
        if '93' not in cid:
            signature = self.decrypt_sha1(current_timestamp, cid)
            url = f'{xurl}/interface2/ws/content/album/list?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&id={cid}&maxitems=96&protocolver=zx/1.1&startitem=0&timestamp={str(current_timestamp)}&type=1&signature={signature}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            if detail.status_code == 200:
                data = detail.json()

                data = data['album']

                for vod in data:

                    name = vod['cn_name']

                    id = str(int(vod['id'])) + "@" + "456"

                    pic = vod['smallimg']

                    remark = vod.get('artist', '未知')

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                            }
                    videos.append(video)
        else:
            signature = self.decrypt_sha5(current_timestamp)
            url = f'{xurl}/interface2/ws/content/pack/list?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&maxitems=96&protocolver=zx/1.1&startitem=0&timestamp={str(current_timestamp)}&signature={signature}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            if detail.status_code == 200:
                data = detail.json()

                data = data['packs']

                for vod in data:

                    name = vod['name']

                    id = str(int(vod['id'])) + "@" + "789"

                    pic = vod['smallimg']

                    remark = "请您欣赏"

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                            }
                    videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''
        fenge = did.split("@")

        current_timestamp = int(datetime.datetime.now().timestamp())
        signature = self.decrypt_sha3(current_timestamp, fenge[0])

        if '789' not in fenge[1]:
            url = f'{xurl}/interface2/ws/content/album/detail?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&id={fenge[0]}&protocolver=zx/1.1&timestamp={str(current_timestamp)}&signature={signature}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            if detail.status_code == 200:
                data = detail.json()

            content = '为您介绍剧情📢' + data.get('introduction', '未知')

            director = data.get('companyname', '未知')

            actor = data.get('artists', '未知')

            bitDepth = data.get('bitDepth', '未知')

            remarks = '共计' + str(data.get('musiccount', '未知')) + '首 ' + str(bitDepth) + '比特'

            year = data.get('publishtime', '未知')

            area = data.get('language', '未知')

            data = data['disks'][0]['musics']

            for sou in data:

                id = sou['id']

                name = sou['name']
                name = name.replace('#', '')

                bofang = bofang + str(name) + '$' + str(id) + '#'

            bofang = bofang[:-1]

            xianlu = '音乐专线'
        else:
            url = f'{xurl}/interface2/ws/content/pack/detail?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&id={fenge[0]}&protocolver=zx/1.1&timestamp={str(current_timestamp)}&signature={signature}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            if detail.status_code == 200:
                data = detail.json()

            content = '为您介绍剧情📢' + data.get('introduction', '未知')

            director = data.get('companyname', '未知')

            actor = data.get('artists', '未知')

            bitDepth = data.get('bitDepth', '未知')

            remarks = '共计' + str(data.get('musiccount', '未知')) + '首 ' + str(bitDepth) + '比特'

            year = data.get('publishtime', '未知')

            area = data.get('language', '未知')

            data = data['musicListItems']

            for sou in data:

                id = sou['testurl']

                name = sou['name']
                name = name.replace('#', '')

                bofang = bofang + str(name) + '$' + str(id) + '#'

            bofang = bofang[:-1]

            xianlu = '音乐音乐'

        videos.append({
            "vod_id": did,
            "vod_director": director,
            "vod_actor": actor,
            "vod_remarks": remarks,
            "vod_year": year,
            "vod_area": area,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
                     })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        if 'http' not in id:
            current_timestamp = int(datetime.datetime.now().timestamp())
            signature = self.decrypt_sha3(current_timestamp, id)

            url1 = f'{xurl1}/interface2/ws/content/music/detail?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&id={id}&protocolver=zx/1.1&timestamp={str(current_timestamp)}&signature={signature}'
            response = requests.get(url1, headers=headerx, allow_redirects=False)
            url1 = response.headers.get('Location')

            detail = requests.get(url=url1, headers=headerx)
            detail.encoding = "utf-8"
            data = detail.json()
            data = data['listenurl']

            signature = self.decrypt_sha4(current_timestamp)

            url2 = f'{data}?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&protocolver=zx/1.1&terminaltype=0&timestamp={str(current_timestamp)}&signature={signature}'
            response = requests.get(url2, headers=headerx, allow_redirects=False)
            url = response.headers.get('Location')
        else:
            current_timestamp = int(time.time() * 1000)
            signature = self.decrypt_sha4(current_timestamp)

            url1 = f'{id}?apikey=0f607264-fc63-38a9-ab9e-13c65db7cd3c&protocolver=zx/1.1&terminaltype=0&timestamp={str(current_timestamp)}&signature={signature}'
            response = requests.get(url1, headers=headerx, allow_redirects=False)
            url = response.headers.get('Location')

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, pg):
        pass

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None








