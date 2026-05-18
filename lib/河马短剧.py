"""
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '河马短剧',
  lang: 'hipy'
})
"""

import requests
import json
import base64
import uuid
from urllib.parse import quote
try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
except ImportError:
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
    except ImportError:
        from Cryptodome.Cipher import AES
        from Cryptodome.Util.Padding import pad, unpad
import sys
sys.path.append('../../')
try:
    from base.spider import Spider
except ImportError:
    class Spider:
        def init(self, extend=""):
            super().init()

            pass

class Spider(Spider):
    
    apiUrl = "https://freevideo.zqqds.cn"
    cateManual = {
        "精选": "53@精选",
        "古装": "54@古装",
        "重生": "55@重生",
        "家庭": "56@家庭",
        "恋爱": "57@恋爱"
    }
    key = base64.b64decode("ZHpramdmeXhnc2h5bGd6bQ==")
    iv = base64.b64decode("YXBpdXBkb3duZWRjcnlwdA==")
    
    def isVideoFormat(self, url):
        video_formats = ['.mp4', '.m3u8', '.avi', '.flv', '.mkv', '.mov', '.webm']
        return any(fmt in url.lower() for fmt in video_formats)

    def manualVideoCheck(self):
        return True
        
    def getName(self):
        return "河马短剧"
    
    def init(self, extend=""):
        super().init()

        return
    
    def aes_encrypt(self, text):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            padded_text = pad(text.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_text)
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception:
            return ""
    
    def aes_decrypt(self, encrypted_data):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted = cipher.decrypt(encrypted_bytes)
            unpadded = unpad(decrypted, AES.block_size)
            return unpadded.decode('utf-8')
        except Exception:
            return "{}"
    
    def encrypt_phone_info(self, text):
        try:
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            return encoded_bytes.decode('utf-8')
        except Exception:
            return text
    
    def decrypt_phone_info(self, encoded_text):
        try:
            decoded_bytes = base64.b64decode(encoded_text)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return encoded_text
    
    def encrypt_data(self):
        random_uuid = str(uuid.uuid4())
        brand_encrypted = self.encrypt_phone_info("vivo")
        model_encrypted = self.encrypt_phone_info("V1938T")
        manu_encrypted = self.encrypt_phone_info("vivo")
        os_encrypted = self.encrypt_phone_info("android")
        data = {
            "version": "2.1.0",
            "pname": "com.dz.hmjc",
            "channelCode": "HMJC1000002",
            "utdidTmp": "A20250528195953036srZcvA",
            "token": "",
            "utdid": "d5d959973340bb1325b551cce488a191",
            "os": "android",
            "osv": 28,
            "brand": "vivo",
            "model": "V1938T",
            "manu": "vivo",
            "userId": "2484393607",
            "launch": "shortcut",
            "mchid": "HMJC1000002",
            "nchid": "VHSE1000000",
            "session1": random_uuid,
            "session2": random_uuid,
            "startScene": "shortcut",
            "recSwitch": True,
            "installTime": 1748433575024,
            "p": 30
        }
        plaintext = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        encrypted_b64 = self.aes_encrypt(plaintext)
        return {
            "alg": "HG45LKBS",
            "datas": encrypted_b64,
            "content-type": "application/json; charset=utf-8",
            "user-agent": "okhttp/4.10.0"
        }
    
    def fetch_api_data(self, portal, body_text):
        try:
            encrypted_body = self.aes_encrypt(body_text)
            if not encrypted_body:
                return None
            headers = self.encrypt_data()
            response = requests.post(
                f"{self.apiUrl}/free-video-portal/portal/{portal}",
                headers=headers,
                data=encrypted_body,
                timeout=15
            )
            if response.status_code == 200:
                result = response.json()
                if result.get('data'):
                    decrypted_data = self.aes_decrypt(result['data'])
                    if decrypted_data:
                        return json.loads(decrypted_data)
            return None
        except Exception:
            return None
    
    def homeContent(self, filter):
        classes = [{"type_id": "53@精选", "type_name": "精选"},
                  {"type_id": "54@古装", "type_name": "古装"},
                  {"type_id": "55@重生", "type_name": "重生"},
                  {"type_id": "56@家庭", "type_name": "家庭"},
                  {"type_id": "57@恋爱", "type_name": "恋爱"}]
        return {'class': classes, 'list': []}
    
    def homeVideoContent(self):
        return {'list': []}
    
    def categoryContent(self, tid, pg, filter, ext):
        result = {'list': [], 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}
        try:
            fenge = tid.split("@")
            cid = fenge[0]
            cname = fenge[1] if len(fenge) > 1 else ""
            body = json.dumps({
                "recSwitch": True,
                "storePageId": 10002,
                "channelGroupId": "10",
                "channelId": int(cid),
                "channelName": cname,
                "lastColumnStyle": 3,
                "fromColumnId": "1",
                "pageFlag": str(pg),
                "theaterSubscriptSwitch": True
            })
            api_data = self.fetch_api_data("1125", body)
            if api_data and 'columnData' in api_data and api_data['columnData']:
                video_data = api_data['columnData'][0].get('videoData', [])
                videos = []
                for vod in video_data:
                    videos.append({
                        "vod_id": vod.get('bookId', ''),
                        "vod_name": vod.get('bookName', ''),
                        "vod_pic": vod.get('coverWap', ''),
                        "vod_remarks": vod.get('finishStatusCn', '')
                    })
                result['list'] = videos
        except Exception:
            pass
        return result
    
    def searchContent(self, key, quick, pg=1):
        return self.searchContentPage(key, quick, pg)
    
    def searchContentPage(self, key, quick, pg):
        result = {'list': [], 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}
        try:
            body = json.dumps({
                "keyword": key,
                "page": int(pg),
                "size": 15,
                "searchSource": "搜索按钮",
                "hotWordType": 2,
                "tagIds": "",
                "reservationSwitch": True
            })
            api_data = self.fetch_api_data("1803", body)
            if api_data and 'searchVos' in api_data:
                videos = []
                for vod in api_data['searchVos']:
                    videos.append({
                        "vod_id": vod.get('bookId', ''),
                        "vod_name": vod.get('bookName', ''),
                        "vod_pic": vod.get('coverWap', ''),
                        "vod_remarks": vod.get('finishStatusCn', '')
                    })
                result['list'] = videos
        except Exception:
            pass
        return result

    def detailContent(self, ids):
        result = {'list': []}
        if not ids:
            return result
        book_id = ids[0]
        try:
            body = json.dumps({
                "bookId": book_id,
                "needNextChapter": 0,
                "isNeedAlias": "",
                "bookAlias": "",
                "resolutionRate": "720P"
            })
            api_data = self.fetch_api_data("1131", body)
            if not api_data or 'videoInfo' not in api_data:
                return result
            video_info = api_data['videoInfo']
            chapter_list = api_data.get('chapterList', [])
            protagonist = video_info.get('protagonist', [])
            vod_actor = ', '.join(protagonist) if protagonist else ""
            vod_director = protagonist[0] if protagonist else ""
            book_tags = video_info.get('bookTags', [])
            book_tags_str = ', '.join(book_tags) if book_tags else ""
            vod_content = video_info.get('introduction', '')
            vod = {
                "vod_id": book_id,
                "vod_name": video_info.get('bookName', ''),
                "vod_pic": video_info.get('coverWap', ''),
                "vod_remarks": video_info.get('finishStatusCn', '') + " " + book_tags_str,
                "vod_content": vod_content,
                "vod_actor": vod_actor,
                "vod_director": vod_director,
                "vod_year": video_info.get('utime', ''),
                "vod_area": "中国",
                "vod_play_from": "河马短剧",
                "vod_play_url": self.buildPlayUrl(book_id, chapter_list)
            }
            result['list'] = [vod]
        except Exception:
            pass
        return result
    
    def buildPlayUrl(self, book_id, chapter_list):
        episodes = []
        if not chapter_list:
            return ""
        sorted_chapters = sorted(chapter_list, key=lambda x: x.get("chapterNum", 0))
        last_chapter_id = sorted_chapters[-1].get("chapterId", "") if sorted_chapters else ""
        for chapter in sorted_chapters:
            chapter_id = chapter.get("chapterId", "")
            chapter_name = chapter.get("chapterName", "")
            if chapter_id:
                episode_url = f"{book_id}@{chapter_id}@{last_chapter_id}"
                episodes.append(f"{chapter_name}${episode_url}")
        return "#".join(episodes)

    def playerContent(self, flag, id, vipFlags):
        result = {
            "parse": 0,
            "url": "",
            "header": "",
            "playUrl": ""
        }
        try:
            parts = id.split('@')
            if len(parts) >= 2:
                book_id = parts[0]
                chapter_id = parts[1]
                last_chapter_id = parts[2] if len(parts) > 2 else chapter_id
                video_url = self.getVideoUrlFromApi(book_id, chapter_id, last_chapter_id)
                if video_url:
                    result["url"] = video_url
                    result["header"] = {
                        "User-Agent": "MOBILE_UA",
                        "Referer": self.apiUrl
                    }
                    return result
        except Exception:
            pass
        return result
    
    def getVideoUrlFromApi(self, book_id, chapter_id, last_chapter_id):
        try:
            body = json.dumps({
                "bookId": book_id,
                "chapterIds": [chapter_id],
                "unClockType": "load",
                "chapterId": last_chapter_id,
                "resolutionRate": "720P"
            })
            api_data = self.fetch_api_data("1139", body)
            if (api_data and 'chapterInfo' in api_data and api_data['chapterInfo'] and
                'content' in api_data['chapterInfo'][0] and
                'mp4SwitchUrl' in api_data['chapterInfo'][0]['content']):
                mp4_urls = api_data['chapterInfo'][0]['content']['mp4SwitchUrl']
                if mp4_urls:
                    return mp4_urls[0]
            return None
        except Exception:
            return None

    def localProxy(self, param):
        return [200, "video/MP2T", {}, param]
