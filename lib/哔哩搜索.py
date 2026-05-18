# coding=utf-8
#!/usr/bin/python
import sys
import json

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "怀旧歌星(番剧合集)"

    def init(self, extend):
        # 如你那边需要cookie，把有效cookie写这里（有些环境可不写）
        self.cookie = ""

    def destroy(self):
        pass

    # ========== 主页分类：名字你定的，id是B站番剧合集season_id ==========
    def homeContent(self, filter):
        return {
            "class": [
                {"type_name": "韩宝仪", "type_id": "486917"},   # 韩宝仪 经典合集(番剧)
                {"type_name": "杨钰莹", "type_id": "487201"},   # 杨钰莹 经典合集(番剧)
                {"type_name": "蔡幸娟", "type_id": "487315"},   # 蔡幸娟 经典合集(番剧)
                {"type_name": "龙飘飘", "type_id": "487402"},   # 龙飘飘 经典合集(番剧)
                {"type_name": "林翠萍", "type_id": "487509"},   # 林翠萍 经典合集(番剧)
            ]
        }

    # ========== 分类列表（pgc番剧接口，和你最早能用的那个一样） ==========
    def categoryContent(self, tid, page, filter, ext):
        url = "https://api.bilibili.com/pgc/season/index/result?season_type={}&page={}&pagesize=20".format(tid, page)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie

        r = self.fetch(url, headers=headers)
        data = json.loads(r.text)

        videos = []
        for item in data.get("data", {}).get("list", []):
            videos.append({
                "vod_id": str(item.get("season_id")),
                "vod_name": item.get("title", ""),
                "vod_pic": item.get("cover", ""),
                "vod_remarks": item.get("index_show", "")
            })

        return {
            "list": videos,
            "page": int(page),
            "pagecount": 999,
            "limit": 20,
            "total": len(videos)
        }

    # ========== 详情（pgc番剧详情，和你最早能用的那个一样） ==========
    def detailContent(self, ids):
        sid = ids[0]
        url = "https://api.bilibili.com/pgc/view/web/season?season_id={}".format(sid)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie

        r = self.fetch(url, headers=headers)
        data = json.loads(r.text).get("result", {})

        play_url = ""
        for ep in data.get("episodes", []):
            name = ep.get("share_copy", ep.get("long_title", ""))
            epid = ep.get("id")
            cid = ep.get("cid")
            play_url += "{}&{}${}_{}#".format(ep.get("badge", ""), name, epid, cid)

        vod = {
            "vod_id": sid,
            "vod_name": data.get("title", ""),
            "vod_pic": data.get("cover", ""),
            "vod_play_from": "B站",
            "vod_play_url": play_url.rstrip("#")
        }
        return {"list": [vod]}

    # ========== 播放（pgc番剧播放，和你最早能用的那个一样） ==========
    def playerContent(self, flag, id, vipFlags):
        epid, cid = id.split("_")
        url = "https://api.bilibili.com/pgc/player/web/playurl?ep_id={}&cid={}&qn=120&fnval=0".format(epid, cid)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie

        return {
            "parse": 0,
            "playUrl": "",
            "url": url,
            "header": headers
        }

    # ========== 搜索（保留兼容，不用来走分类） ==========
    def searchContent(self, key, quick):
        return {"list": []}
