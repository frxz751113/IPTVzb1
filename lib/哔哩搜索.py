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
        self.cookie = "_uuid=5E4B2B98-1014A-84D8-FA33-EC210C5BEC10DA82367infoc; buvid3=E9D0A426-85E9-E6C7-C75E-206A3E1BEB4D81910infoc; b_nut=1666168082; buvid4=4FC87B9C-3540-2275-688C-8612D3EA719B81910-022101916-ZLe640jXRAMHySuaCe9aUw==; rpdid=|(k|u)YYm)uY0J'uYYYuY)uuu; i-wanna-go-back=-1; fingerprint=9c214a6da0197a48e576ccf22e9f0ac7; buvid_fp_plain=undefined; nostalgia_conf=-1; DedeUserID=3493076028885079; DedeUserID__ckMd5=60a8757a1f4d6ae9; buvid_fp=9c214a6da0197a48e576ccf22e9f0ac7; CURRENT_QUALITY=80; b_ut=5; PVID=2; bp_video_offset_3493076028885079=undefined; bsource=search_google; SESSDATA=42b8ada6,1683277266,4bd05*b2; bili_jct=2dbe39aea02b41324395630a24d4775f; sid=89gnel66; innersign=0; b_lsid=9EF63922_1844D55A286; CURRENT_FNVAL=4048"

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
