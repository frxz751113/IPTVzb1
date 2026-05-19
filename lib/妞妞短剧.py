from base.spider import Spider
import requests
import sys
import json
import time
import hashlib
import hmac
import re
import base64
from datetime import datetime

sys.path.append('..')

xurl = "https://new.tianjinzhitongdaohe.com"

headers = {
    "Cache-Control": "no-cache",
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "okhttp/4.12.0"
}

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}

class Spider(Spider):
    global xurl
    global headers
    global headerx
    
    _nntoken = None
    _nnatoken = None
    _token_time = None

    def getName(self):
        return "妞妞短剧[短]"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def _get_date_key(self):
        return datetime.now().strftime('%Y%m%d')

    def _ensure_token(self):
        try:
            current_date = self._get_date_key()
            
            if (Spider._token_time != current_date or 
                not Spider._nntoken or 
                not Spider._nnatoken):
                
                tkurl = f"{xurl}/api/v1/app/user/visitorInfo"
                tkheaders = {
                    "deviceid": "aa11fc54-ba9c-3980-add5-447d3fa5b939",
                    "token": "",
                    "User-Agent": "okhttp/4.12.0",
                    "client": "app",
                    "devicetype": "Android"
                }
                
                response = requests.get(tkurl, headers=tkheaders, timeout=10)
                tkdata = response.json()
                Spider._nntoken = tkdata.get('data', {}).get('token', '')
                
                t = str(int(time.time()))
                body = f"ac=wifi&os=Android&vod_version=1.10.21.6-tob&os_version=9&type=1&clientVersion=v5.2.5&uuid=Y4WNZ3SAWK7MAJMH7CXCDHJ4VMPVFRZQTBSIA4XTYO4AWEUHIK6Q01&resolution=1280*2618&openudid=889edced38f1069b&dt=Pixel%204&sha1=46121F77CE2FCAD3DBC3B9EC8A24908C1A8AD6D9&os_api=28&install_id=1549688030634536&device_brand=google&sdk_version=1.1.3.0&package_name=com.niuniu.ztdh.app&siteid=5627189&dev_log_aid=667431&oaid=&timestamp={t}"
                nonce = "VX1KKGtoBDCi1fB1"
                secret = 'aceaa47f96b4875d446b2e1d97e03bbb'
                
                message = t + nonce + body
                signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
                
                try:
                    from Crypto.Cipher import AES
                    from Crypto.Util.Padding import pad
                    
                    key = 'dafdb3d2a5c343d6'.encode('utf-8')
                    cipher = AES.new(key, AES.MODE_ECB)
                    padded_data = pad(body.encode('utf-8'), AES.block_size)
                    encrypted = cipher.encrypt(padded_data)
                    enc_body = base64.b64encode(encrypted).decode('utf-8')
                except:
                    enc_body = body
                
                login_url = "https://csj-sp.csjdeveloper.com/csj_sp/api/v1/user/login?siteid=5627189"
                login_headers = {
                    'X-Salt': '786774955F',
                    'X-Nonce': nonce,
                    'X-Timestamp': t,
                    'X-Signature': signature,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                login_response = requests.post(login_url, headers=login_headers, data=enc_body, timeout=10)
                
                try:
                    from Crypto.Cipher import AES
                    from Crypto.Util.Padding import unpad
                    
                    key = 'dafdb3d2a5c343d6'.encode('utf-8')
                    cipher = AES.new(key, AES.MODE_ECB)
                    encrypted_data = base64.b64decode(login_response.text)
                    decrypted = cipher.decrypt(encrypted_data)
                    login_data = json.loads(unpad(decrypted, AES.block_size).decode('utf-8'))
                    Spider._nnatoken = login_data.get('data', {}).get('access_token', '')
                except:
                    Spider._nnatoken = ''
                
                Spider._token_time = current_date
            
            return {'nntoken': Spider._nntoken, 'nnatoken': Spider._nnatoken}
        except Exception as e:
            print(f"Token获取失败: {e}")
            return {'nntoken': '', 'nnatoken': ''}

    def _aes_encrypt_ecb(self, data, key):
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad
            
            key_bytes = key.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_ECB)
            padded_data = pad(data.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted).decode('utf-8')
        except:
            return data

    def _aes_decrypt_ecb(self, encrypted_data, key):
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            
            key_bytes = key.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_ECB)
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted = cipher.decrypt(encrypted_bytes)
            return unpad(decrypted, AES.block_size).decode('utf-8')
        except:
            return encrypted_data

    def _post_encrypted(self, url, data, index):
        try:
            t10 = str(int(time.time()))
            x_nonce = "X9UknYKtLa3DmtjC"
            
            body1 = data
            body1 = re.sub(r'&timestamp=\d+', f'&timestamp={t10}', body1)
            body1 = re.sub(r'&index=\d+', f'&index={index}', body1)
            body1 = re.sub(r'&count=\d+', '&count=1', body1)
            body1 = re.sub(r'&lock_free=\d+', '&lock_free=1', body1)
            body1 = re.sub(r'&lock_ad=\d+', '&lock_ad=1', body1)
            body1 = re.sub(r'&lock_index=\d+', f'&lock_index={index}', body1)
            
            body2 = self._aes_encrypt_ecb(body1, 'ce49b18dd4e0a4d8')
            body3 = t10 + x_nonce + body1
            signature = hmac.new('aceaa47f96b4875d446b2e1d97e03bbb'.encode(), 
                               body3.encode(), hashlib.sha256).hexdigest()
            
            tokens = self._ensure_token()
            headers_enc = {
                'X-Salt': 'FD8188A8D5',
                'X-Nonce': x_nonce,
                'X-Timestamp': t10,
                'X-Access-Token': tokens['nnatoken'],
                'X-Signature': signature,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(url, headers=headers_enc, data=body2, timeout=10)
            decrypted = self._aes_decrypt_ecb(response.text, 'ce49b18dd4e0a4d8')
            return json.loads(decrypted)
        except Exception as e:
            print(f"加密请求失败: {e}")
            return {}

    def homeContent(self, filter):
        result = {"class": []}
        
        try:
            tokens = self._ensure_token()
            
            payload = {}
            url = f"{xurl}/api/v1/app/screen/screenType"
            req_headers = headers.copy()
            req_headers['token'] = tokens['nntoken']
            
            response = requests.post(url=url, headers=req_headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()

                if data.get('data') and len(data['data']) > 0:
                    if data['data'][0].get('children') and len(data['data'][0]['children']) > 0:
                        if data['data'][0]['children'][0].get('children'):
                            setup = data['data'][0]['children'][0]['children']

                            for vod in setup:
                                name = vod['name']
                                result["class"].append({"type_id": name, "type_name": name})
            
            return result
        except Exception as e:
            print(f"homeContent错误: {e}")
            fixed_categories = ["都市", "穿越", "逆袭", "总裁", "虐恋", "甜宠", "重生", "玄幻"]
            for cat in fixed_categories:
                result["class"].append({"type_id": cat, "type_name": cat})
            return result

    def homeVideoContent(self):
        result = {}
        videos = []
        
        try:
            tokens = self._ensure_token()
            
            payload = {
                "condition": {
                    "classify": "都市",
                    "typeId": "S1"
                },
                "pageNum": "1",
                "pageSize": 20
            }
            
            url = f"{xurl}/api/v1/app/screen/screenMovie"
            req_headers = headers.copy()
            req_headers['token'] = tokens['nntoken']
            
            response = requests.post(url=url, headers=req_headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('data') and data['data'].get('records'):
                    setup = data['data']['records']
                    
                    for vod in setup:
                        name = vod['name']
                        id = vod['id']
                        pic = vod['cover']
                        remark = f"{vod.get('totalEpisode', '0')}集" if vod.get('totalEpisode') else vod.get('classify', '短剧')
                        
                        video = {
                            "vod_id": str(id),
                            "vod_name": name,
                            "vod_pic": pic,
                            "vod_remarks": remark
                        }
                        videos.append(video)
            
            result = {'list': videos}
            return result
        except Exception as e:
            print(f"homeVideoContent错误: {e}")
            return {'list': []}

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        try:
            if pg:
                page = int(pg)
            else:
                page = 1

            tokens = self._ensure_token()

            payload = {
                "condition": {
                    "classify": cid,
                    "typeId": "S1"
                },
                "pageNum": str(page),
                "pageSize": 40
            }

            url = f"{xurl}/api/v1/app/screen/screenMovie"
            req_headers = headers.copy()
            req_headers['token'] = tokens['nntoken']
            
            response = requests.post(url=url, headers=req_headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('data') and data['data'].get('records'):
                    setup = data['data']['records']

                    for vod in setup:
                        name = vod['name']
                        id = vod['id']
                        pic = vod['cover']
                        remark = f"{vod.get('totalEpisode', '0')}集" if vod.get('totalEpisode') else vod.get('classify', '短剧')

                        video = {
                            "vod_id": str(id),
                            "vod_name": name,
                            "vod_pic": pic,
                            "vod_remarks": remark
                        }
                        videos.append(video)
            
            result = {'list': videos}
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 40
            result['total'] = 999999
            return result
        except Exception as e:
            print(f"categoryContent错误: {e}")
            result = {'list': []}
            result['page'] = pg
            result['pagecount'] = 1
            result['limit'] = 40
            result['total'] = 0
            return result

    def _clean_episode_name(self, episode_num):
        if not episode_num:
            return ""
        episode_str = str(episode_num)
        episode_str = episode_str.replace('第', '').replace('集', '')
        return episode_str

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''
        
        vod_name = '未知'
        vod_pic = ''
        vod_content = '暂无剧情介绍'
        vod_director = ''
        vod_actor = ''
        vod_area = ''
        vod_year = ''
        vod_remarks = ''
        vod_total_episode = 0  # 新增：总集数

        try:
            tokens = self._ensure_token()
            req_headers = headers.copy()
            req_headers['token'] = tokens['nntoken']

            try:
                detail_payload = {"id": did, "typeId": "S1"}
                detail_url = f"{xurl}/api/v1/app/play/movieDesc"
                detail_response = requests.post(url=detail_url, headers=req_headers, json=detail_payload, timeout=10)
                
                if detail_response.status_code == 200:
                    detail_json = detail_response.json()
                    if detail_json.get('code') == 200 and detail_json.get('data'):
                        detail_data = detail_json['data']
                        
                        vod_name = detail_data.get('name', '未知')
                        vod_pic = detail_data.get('cover', '')
                        vod_content = detail_data.get('introduce', '暂无剧情介绍')
                        vod_director = detail_data.get('director', '')
                        vod_actor = detail_data.get('star', '')
                        vod_area = detail_data.get('area', '')
                        vod_year = detail_data.get('year', '')
                        classify = detail_data.get('classify', '')
                        score = detail_data.get('score', '')
                        watch_count = detail_data.get('watch', 0)
                        
                        remark_parts = []
                        if score:
                            remark_parts.append(f"评分:{score}")
                        if classify:
                            remark_parts.append(f"类型:{classify}")
                        if watch_count:
                            remark_parts.append(f"播放:{watch_count}")
                        vod_remarks = ' | '.join(remark_parts) if remark_parts else ''
                        
            except Exception as e:
                print(f"获取movieDesc详情失败: {e}")

            list_payload = {
                "id": did,
                "source": 0,
                "typeId": "S1",
                "userId": "546932"
            }

            url = f"{xurl}/api/v1/app/play/movieDetails"
            response = requests.post(url=url, headers=req_headers, json=list_payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                vod_data = data.get('data', {})
                
                vod_total_episode = vod_data.get('totalEpisode', 0)
                
                if vod_name == '未知' and vod_data.get('name'):
                    vod_name = vod_data.get('name')
                if not vod_pic and vod_data.get('cover'):
                    vod_pic = vod_data.get('cover')
                if vod_content == '暂无剧情介绍' and vod_data.get('introduce'):
                    vod_content = vod_data.get('introduce')
                
                if vod_data.get('episodeList') and len(vod_data['episodeList']) > 0:
                    for episode in vod_data['episodeList']:
                        episode_num = self._clean_episode_name(episode.get('episode', ''))
                        episode_id = episode.get('id', '')
                        bofang += f"第{episode_num}集${did}@{episode_id}#"
                    
                    if bofang:
                        bofang = bofang[:-1]
                        xianlu = '妞妞短剧'
                
                elif vod_data.get('thirdPlayId'):
                    third_play_id = vod_data['thirdPlayId']
                    base_data = f"not_include=0&lock_free=1&type=1&clientVersion=v5.2.5&uuid=6IDYUSASPQY5BBVACWQW3LLTPV4V7DE26UOCX5TZTVUGX4VUJNXQ01&resolution=1080*2320&openudid=82f4175d577a2939&dt=22021211RC&os_api=31&install_id=1496879012031075&sdk_version=1.1.3.0&siteid=5627189&dev_log_aid=667431&oaid=abec0dfff623201b&timestamp=1752498494&direction=0&ac=mobile&os=Android&vod_version=1.10.21.6-tob&os_version=12&count=1&index=1&shortplay_id={third_play_id}&sha1=46121F77CE2FCAD3DBC3B9EC8A24908C1A8AD6D9&device_brand=Redmi&package_name=com.niuniu.ztdh.app"
                    
                    html1 = self._post_encrypted("https://csj-sp.csjdeveloper.com/csj_sp/api/v1/shortplay/detail?siteid=5627189", base_data, "1")
                    
                    if html1.get('data') and html1['data'].get('episode_right_list'):
                        ep_list = html1['data']['episode_right_list']
                        for it in ep_list:
                            ep_index = self._clean_episode_name(it.get('index', ''))
                            lock_type = it.get('lock_type', '')
                            bofang += f"第{ep_index}集+{lock_type}+{third_play_id}#"
                        
                        if bofang:
                            bofang = bofang[:-1]
                            xianlu = '妞妞短剧2'
            
            if vod_total_episode > 0:
                total_ep_str = f"总集数:{vod_total_episode}"
                if vod_remarks:
                    vod_remarks = f"{total_ep_str} | {vod_remarks}"
                else:
                    vod_remarks = total_ep_str
            
            video_info = {
                "vod_id": did,
                "vod_name": vod_name,
                "vod_pic": vod_pic,
                "vod_content": vod_content,
                "vod_director": vod_director,
                "vod_actor": vod_actor,
                "vod_area": vod_area,
                "vod_year": vod_year,
                "vod_remarks": vod_remarks,
                "vod_play_from": xianlu if xianlu else '暂无资源',
                "vod_play_url": bofang if bofang else '暂无播放地址$0'
            }
            
            videos.append(video_info)
            result['list'] = videos
            return result
            
        except Exception as e:
            print(f"detailContent错误: {e}")
            videos.append({
                "vod_id": did,
                "vod_name": "加载失败",
                "vod_pic": "",
                "vod_content": f"详情加载失败: {str(e)}",
                "vod_director": "",
                "vod_actor": "",
                "vod_area": "",
                "vod_year": "",
                "vod_remarks": "",
                "vod_play_from": "暂无资源",
                "vod_play_url": "暂无播放地址$0"
            })
            result['list'] = videos
            return result

    def playerContent(self, flag, id, vipFlags):
        try:
            tokens = self._ensure_token()
            
            if '@' in id:
                fenge = id.split('@')
                
                if len(fenge) < 2:
                    return {
                        "parse": 0,
                        "playUrl": '',
                        "url": '',
                        "header": headerx
                    }

                vid = fenge[0].split('$')[-1] if '$' in fenge[0] else fenge[0]
                ep_id = fenge[1]

                payload = {
                    "episodeId": ep_id,
                    "id": vid,
                    "source": 0,
                    "typeId": "S1",
                    "userId": "546932"
                }

                url = f"{xurl}/api/v1/app/play/movieDetails"
                req_headers = headers.copy()
                req_headers['token'] = tokens['nntoken']
                
                response = requests.post(url=url, headers=req_headers, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data') and data.get('data').get('url'):
                        play_url = data['data']['url']
                    else:
                        play_url = ''
                else:
                    play_url = ''

                result = {
                    "parse": 0,
                    "playUrl": '',
                    "url": play_url,
                    "header": headerx
                }
                return result
            
            elif '+' in id:
                parts = id.split('+')
                if len(parts) >= 3:
                    index = self._clean_episode_name(parts[0])
                    lock_type = parts[1]
                    third_play_id = parts[2]
                    
                    base_data = f"not_include=0&lock_free=1&type=1&clientVersion=v5.2.5&uuid=6IDYUSASPQY5BBVACWQW3LLTPV4V7DE26UOCX5TZTVUGX4VUJNXQ01&resolution=1080*2320&openudid=82f4175d577a2939&dt=22021211RC&os_api=31&install_id=1496879012031075&sdk_version=1.1.3.0&siteid=5627189&dev_log_aid=667431&oaid=abec0dfff623201b&timestamp=1752498494&direction=0&ac=mobile&os=Android&vod_version=1.10.21.6-tob&os_version=12&count=1&index=1&shortplay_id={third_play_id}&sha1=46121F77CE2FCAD3DBC3B9EC8A24908C1A8AD6D9&device_brand=Redmi&package_name=com.niuniu.ztdh.app"
                    
                    if lock_type == 'free':
                        html1 = self._post_encrypted("https://csj-sp.csjdeveloper.com/csj_sp/api/v1/shortplay/detail?siteid=5627189", base_data, index)
                        
                        if (html1.get('data') and html1['data'].get('list') and 
                            len(html1['data']['list']) > 0):
                            video_model = html1['data']['list'][0].get('video_model', {})
                            video_list = video_model.get('video_list', {})
                            video_1 = video_list.get('video_1', {})
                            main_url = video_1.get('main_url', '')
                            
                            if main_url:
                                try:
                                    real_url = base64.b64decode(main_url).decode('utf-8')
                                    return {
                                        "parse": 0,
                                        "playUrl": '',
                                        "url": real_url,
                                        "header": headerx
                                    }
                                except:
                                    pass
                    else:
                        unlock_data = f"ac=mobile&os=Android&vod_version=1.10.21.6-tob&os_version=12&lock_ad=3&lock_free=3&type=1&clientVersion=v5.2.5&uuid=6IDYUSASPQY5BBVACWQW3LLTPV4V7DE26UOCX5TZTVUGX4VUJNXQ01&resolution=1080*2320&openudid=82f4175d577a2939&shortplay_id={third_play_id}&dt=22021211RC&sha1=46121F77CE2FCAD3DBC3B9EC8A24908C1A8AD6D9&lock_index=21&os_api=31&install_id=1496879012031075&device_brand=Redmi&sdk_version=1.1.3.0&package_name=com.niuniu.ztdh.app&siteid=5627189&dev_log_aid=667431&oaid=abec0dfff623201b&timestamp=1752498493"
                        
                        self._post_encrypted("https://csj-sp.csjdeveloper.com/csj_sp/api/v1/pay/ad_unlock?siteid=5627189", unlock_data, index)
                        
                        html1 = self._post_encrypted("https://csj-sp.csjdeveloper.com/csj_sp/api/v1/shortplay/detail?siteid=5627189", base_data, index)
                        
                        if (html1.get('data') and html1['data'].get('list') and 
                            len(html1['data']['list']) > 0):
                            video_model = html1['data']['list'][0].get('video_model', {})
                            video_list = video_model.get('video_list', {})
                            video_1 = video_list.get('video_1', {})
                            main_url = video_1.get('main_url', '')
                            
                            if main_url:
                                try:
                                    real_url = base64.b64decode(main_url).decode('utf-8')
                                    return {
                                        "parse": 0,
                                        "playUrl": '',
                                        "url": real_url,
                                        "header": headerx
                                    }
                                except:
                                    pass
            
            return {
                "parse": 0,
                "playUrl": '',
                "url": '',
                "header": headerx
            }
            
        except Exception as e:
            print(f"playerContent错误: {e}")
            return {
                "parse": 0,
                "playUrl": '',
                "url": '',
                "header": headerx
            }

    def searchContentPage(self, key, quick, pg):
        result = {}
        videos = []

        try:
            if pg:
                page = int(pg)
            else:
                page = 1

            tokens = self._ensure_token()

            payload = {
                "condition": {
                    "typeId": "S1",
                    "value": key
                },
                "pageNum": str(page),
                "pageSize": 40
            }

            url = f"{xurl}/api/v1/app/search/searchMovie"
            req_headers = headers.copy()
            req_headers['token'] = tokens['nntoken']
            
            response = requests.post(url=url, headers=req_headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('data') and data['data'].get('records'):
                    setup = data['data']['records']

                    for vod in setup:
                        name = vod['name']
                        if key not in name:
                            continue
                            
                        id = vod['id']
                        pic = vod['cover']
                        remark = vod.get('year', '未知')

                        video = {
                            "vod_id": str(id),
                            "vod_name": name,
                            "vod_pic": pic,
                            "vod_remarks": remark
                        }
                        videos.append(video)

            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 40
            result['total'] = 999999
            return result
        except Exception as e:
            print(f"searchContentPage错误: {e}")
            result['list'] = []
            result['page'] = pg
            result['pagecount'] = 1
            result['limit'] = 40
            result['total'] = 0
            return result

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, pg)

    def localProxy(self, params):
        return None
