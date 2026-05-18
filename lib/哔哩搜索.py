# coding=utf-8
#!/usr/bin/python
import sys
import json
import time
from urllib.parse import quote

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "B站歌星搜索"

    def init(self, extend):
        pass

    def destroy(self):
        pass

    # ================= 分类 =================
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

    # ================= 搜索 =================
    def searchContent(self, key, page):
        url = "https://api.bilibili.com/x/web-interface/wbi/search/all/v2"
        params = {
            "keyword": key,
            "page": page,
            "search_type": "video"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Cookie": self.getCookie()
        }

        r = self.fetch(url, params=params, headers=headers, timeout=5)
        data = json.loads(r.text)

        videos = []
        if "data" not in data or "result" not in data["data"]:
            return self.empty(page)

        for item in data["data"]["result"]:
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

    # ================= Cookie（重点） =================
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
            "bp_video_offset_3493076028885079=undefined; "
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

    # ================= 其他 =================
    def searchContentPage(self, key, quick, page):
        return self.searchContent(key, page)

    def detailContent(self, ids):
        return {}

    def playerContent(self, flag, id, vipFlags):
        return {}
