# coding=utf-8
#!/usr/bin/python
import sys
import json
import time
from datetime import datetime
from difflib import SequenceMatcher
from urllib.parse import quote, unquote

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "B站搜索分类"

    def init(self, extend):
        try:
            self.extendDict = json.loads(extend)
        except:
            self.extendDict = {}

    def destroy(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    # ===================== 主页分类（关键词） =====================
    def homeContent(self, filter):
        result = {}
        cateManual = {
            "韩宝仪": "韩宝仪",
            "杨钰莹": "杨钰莹",
            "蔡幸娟": "蔡幸娟",
            "龙飘飘": "龙飘飘",
            "林翠萍": "林翠萍",
        }
        classes = []
        for k, v in cateManual.items():
            classes.append({
                'type_name': k,
                'type_id': v
            })
        result['class'] = classes
        return result

    def homeVideoContent(self):
        return self.categoryContent('海贼王', '1', False, {})

    # ===================== 分类 = 搜索 =====================
    def categoryContent(self, tid, page, filter, ext):
        page = int(page)
        videos = self.realSearch(tid, page)
        return {
            'list': videos,
            'page': page,
            'pagecount': 999,
            'limit': 20,
            'total': len(videos)
        }

    # ===================== 真·B站搜索框接口 =====================
    def realSearch(self, key, page):
        videos = []
        cookie, imgKey, subKey = self.getCookie('{}')

        url = 'https://api.bilibili.com/x/web-interface/wbi/search/all/v2'
        params = {
            'keyword': key,
            'page': page,
            'search_type': 'media_bangumi',
            'order': 'totalrank'
        }

        headers = self.header.copy()
        r = self.fetch(
            url,
            params=params,
            headers=headers,
            cookies=cookie,
            timeout=5
        )

        data = json.loads(self.cleanText(r.text))
        if 'data' not in data or 'result' not in data['data']:
            return videos

        for item in data['data']['result']:
            if item.get('result_type') != 'media_bangumi':
                continue
            for vod in item.get('data', []):
                sid = str(vod.get('season_id'))
                title = self.removeHtmlTags(vod.get('title', ''))
                pic = vod.get('cover') or vod.get('pic', '')
                remark = vod.get('index_show', '')

                if not sid or not title:
                    continue

                videos.append({
                    "vod_id": sid,
                    "vod_name": title,
                    "vod_pic": pic,
                    "vod_remarks": remark
                })

        return videos

    # ===================== 搜索入口（兼容） =====================
    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):
        videos = self.realSearch(key, int(page))
        return {'list': videos}

    # ===================== 详情（原样） =====================
    def detailContent(self, did):
        did = did[0]
        url = f"http://api.bilibili.com/pgc/view/web/season?season_id={did}"
        r = self.fetch(url, headers=self.header, timeout=10)
        data = json.loads(self.cleanText(r.text))

        vod = {
            "vod_id": did,
            "vod_name": self.removeHtmlTags(data['result']['title']),
            "vod_pic": data['result']['cover'],
            "type_name": data['result']['share_sub_title'],
            "vod_actor": data['result']['actors'].replace('\n', '，'),
            "vod_content": self.removeHtmlTags(data['result']['evaluate'])
        }

        playUrl = ''
        for ep in data['result']['episodes']:
            name = self.removeHtmlTags(ep['share_copy']).replace("#", "-").replace('$', '*')
            playUrl += f"[01:00]/{name}${ep['id']}_{ep['cid']}#"

        vod['vod_play_from'] = 'B站番剧'
        vod['vod_play_url'] = playUrl.rstrip('#')
        return {'list': [vod]}

    # ===================== 播放（原样） =====================
    def playerContent(self, flag, pid, vipFlags):
        aid, cid = pid.split('_')
        url = f'https://api.bilibili.com/pgc/player/web/playurl?ep_id={aid}&cid={cid}&qn=120&fnval=4048'
        return {
            "parse": "0",
            "playUrl": "",
            "url": url,
            "header": self.header
        }

    # ===================== 工具 =====================
    def removeHtmlTags(self, src):
        from re import sub, compile
        return sub(compile('<.*?>'), '', src)

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
