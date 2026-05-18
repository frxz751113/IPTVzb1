# coding=utf-8
#!/usr/bin/python
import sys
import json
import time
import hashlib
from urllib.parse import urlencode

sys.path.append('..')
from base.spider import Spider

# ========== WBI 签名（必须） ==========
mixinKeyEncTab = [
    46,47,18,2,53,8,23,32,15,50,10,31,58,3,45,35,27,43,22,24,6,11,36,41,16,0,14,25,53,57,50,38,49,61,13,23,28,33,8,60,39,34,17,5,55,40,9,31,20,29,61,19,57,7,21,51,60,12,47,44,37,38,59,43,52,42,2,1,40,41,27,55,10,16,9,58,52,48,54,30,56,25,36,20,32,47,56,43,18,53,45,29,34,47,56,38,44,46,19,43,55,16,50,15,48,27,36,20,32,47,56,43,18,53,51,39,51,45,15,47,53,40,37,11,56,48,34,39,18,53,47,55,14,50,23,18,43,24,43,44,51,38,55,40,50,28,18,46,71
]

def getMixinKey(orig):
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

# ========== 主 Spider ==========
class Spider(Spider):

    def getName(self):
        return "B站个性歌星"

    def init(self, extend):
        pass

    def destroy(self):
        pass

    # ================= 分类（你指定的） =================
    def homeContent(self, filter):
        return {
            "class": [
                {"type_name": "韩宝仪", "type_id": "韩宝仪"},
                {"type_name": "杨钰莹", "type_id": "杨钰莹"},
                {"type_name": "蔡幸娟", "type_id": "蔡幸娟"},
                {"type_name": "龙飘飘", "type_id": "龙飘飘"},
                {"type_name": "林翠萍", "type_id": "林翠萍"}
            ]
        }

    # ================= 分类页 =================
    def categoryContent(self, tid, page, filter, ext):
        return self.searchContent(tid, page)

    # ================= 搜索（JS 同款） =================
    def searchContent(self, key, page):
        wts = str(int(time.time()))

        params = {
            "keyword": key,
            "page": page,
            "search_type": "video",
            "wts": wts
        }

        # WBI 签名
        encoded = urlencode(sorted(params.items()))
        mixinKey = getMixinKey(encoded)
        w_rid = hashlib.md5((encoded + mixinKey).encode()).hexdigest()

        url = f"https://api.bilibili.com/x/web-interface/wbi/search/all/v2?{encoded}&w_rid={w_rid}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Cookie": self.getCookie()
        }

        r = self.fetch(url, headers=headers, timeout=5)
        data = json.loads(r.text)

        videos = []
        if data.get("code") != 0:
            return self.empty(page)

        for item in data.get("data", {}).get("result", []):
            if item.get("result_type") != "video":
                continue
            for v in item.get("data", []):
                title = v.get("title", "")
                title = title.replace("<em class=\"keyword\">", "").replace("</em>", "")

                videos.append({
                    "vod_id": v.get("bvid"),
                    "vod_name": title,
                    "vod_pic": v.get("pic"),
                    "vod_remarks": v.get("duration", "")
                })

        return {
            "list": videos,
            "page": int(page),
            "pagecount": int(page) + 1,
            "limit": 20,
            "total": len(videos)
        }

    # ================= Cookie（照 JS 给的） =================
    def getCookie(self):
        return (
            "_uuid=5E4B2B98-1014A-84D8-FA33-EC210C5BEC10DA82367infoc; "
            "buvid3=E9D0A426-85E9-E6C7-C75E-206A3E1BEB4D81910infoc; "
            "b_nut=1666168082; "
            "DedeUserID=3493076028885079; "
            "DedeUserID__ckMd5=60a8757a1f4d6ae9; "
            "SESSDATA=42b8ada6,1683277266,4bd05*b2; "
            "bili_jct=2dbe39aea02b41324395630a24d4775f; "
            "sid=89gnel66; "
            "CURRENT_QUALITY=80; "
            "bsource=search_google"
        )

    # ================= 空结果 =================
    def empty(self, page):
        return {
            "list": [],
            "page": int(page),
            "pagecount": int(page),
            "limit": 20,
            "total": 0
        }

    # ================= 兼容 =================
    def searchContentPage(self, key, quick, page):
        return self.searchContent(key, page)

    def detailContent(self, ids):
        return {}

    def playerContent(self, flag, id, vipFlags):
        return {}
