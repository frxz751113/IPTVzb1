# coding=utf-8
#!/usr/bin/python
import sys
import json
from urllib.parse import quote

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "B站搜索分类"

    def init(self, extend):
        self.ext = {}
        try:
            self.ext = json.loads(extend)
        except:
            pass

    def destroy(self):
        pass

    # ================= 主页分类 =================
    def homeContent(self, filter):
        return {
            "class": [
                {"type_name": "韩宝仪", "type_id": "1"},
                {"type_name": "杨钰莹", "type_id": "2"},
                {"type_name": "蔡幸娟", "type_id": "3"},
                {"type_name": "龙飘飘", "type_id": "4"},
                {"type_name": "林翠萍", "type_id": "5"},
                
            ]            
        }

    # ================= 分类映射 =================
    CATE_MAP = {
        "1": "韩宝仪",
        "2": "杨钰莹",
        "3": "蔡幸娟",
        "4": "龙飘飘",
        "5": "林翠萍",
    }

    # ================= 分类页（滑动加载核心） =================
    def categoryContent(self, tid, page, filter, ext):
        tid = str(tid)
        page = int(page)

        keyword = self.CATE_MAP.get(tid)
        if not keyword:
            return self.emptyResult(page)

        videos = self.search(keyword, page)

        # ✅ 关键：没有结果就告诉 OK 影视“到头了”
        if not videos:
            return self.emptyResult(page)

        return {
            "list": videos,
            "page": page,
            "pagecount": page + 1,   # ✅ 下一页还能点
            "limit": 20,
            "total": page * 20 + 1
        }

    # ================= 搜索接口（B站网页同款） =================
    def search(self, key, page):
        url = "https://api.bilibili.com/x/web-interface/wbi/search/all/v2"
        params = {
            "keyword": key,
            "page": page,
            "search_type": "media_bangumi"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/"
        }

        r = self.fetch(url, params=params, headers=headers, timeout=5)
        data = json.loads(r.text)

        videos = []
        if "data" not in data or "result" not in data["data"]:
            return videos

        for item in data["data"]["result"]:
            if item.get("result_type") != "media_bangumi":
                continue
            for v in item.get("data", []):
                videos.append({
                    "vod_id": str(v["season_id"]),
                    "vod_name": v.get("title", ""),
                    "vod_pic": v.get("cover", ""),
                    "vod_remarks": v.get("index_show", "")
                })

        return videos

    # ================= 空结果 =================
    def emptyResult(self, page):
        return {
            "list": [],
            "page": page,
            "pagecount": page,
            "limit": 20,
            "total": 0
        }

    # ================= 搜索入口 =================
    def searchContent(self, key, quick):
        return {
            "list": self.search(key, 1)
        }

    # ================= 详情（原样） =================
    def detailContent(self, ids):
        sid = ids[0]
        url = f"https://api.bilibili.com/pgc/view/web/season?season_id={sid}"
        r = self.fetch(url, headers=self.header())
        data = json.loads(r.text)

        vod = {
            "vod_id": sid,
            "vod_name": data["result"]["title"],
            "vod_pic": data["result"]["cover"],
            "vod_remarks": data["result"]["index_show"],
            "vod_content": data["result"]["evaluate"]
        }

        play = ""
        for ep in data["result"]["episodes"]:
            play += f"{ep['share_copy']}${ep['id']}_{ep['cid']}#"

        vod["vod_play_from"] = "B站"
        vod["vod_play_url"] = play.rstrip("#")

        return {"list": [vod]}

    # ================= Header =================
    def header(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/"
        }
