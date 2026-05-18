# coding=utf-8
#!/usr/bin/python
import sys
import json
import time
import base64
from urllib.parse import quote, urlencode
from functools import reduce

sys.path.append('..')
from base.spider import Spider

# 引入用于计算 WBI 签名的字符表
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 22,
    24, 6, 11, 36, 41, 16, 0, 14, 25, 53, 57, 50, 38, 49, 61, 13, 23, 28, 33,
    8, 60, 39, 34, 17, 5, 55, 40, 9, 31, 20, 29, 61, 19, 57, 7, 21, 51, 60, 12,
    47, 44, 37, 38, 59, 43, 52, 42, 2, 1, 40, 41, 27, 55, 10, 16, 9, 58, 52, 48,
    54, 30, 56, 25, 1, 4, 11, 6, 45, 52, 33, 3, 63, 41, 59, 17, 13, 48, 34, 62,
    2, 15, 46, 57, 38, 44, 21, 24, 13, 53, 40, 37, 39, 42, 44, 50, 45, 52, 49, 47,
    41, 17, 56, 25, 36, 22, 8, 58, 14, 5, 20, 61, 37, 51, 30, 2, 54, 22, 8, 1,
    39, 33, 17, 27, 54, 43, 14, 36, 47, 42, 28, 7, 8, 53, 13, 17, 7, 40, 49, 46,
    6, 53, 20, 47, 41, 25, 50, 17, 37, 4, 47, 55, 19, 14, 56, 44, 16, 42, 51, 1,
    34, 53, 46, 42, 52, 61, 48, 15, 45, 53, 42, 29, 18, 44, 47, 52, 1, 8, 24, 30,
    45, 38, 18, 46, 47, 31, 54, 38, 29, 47, 56, 15, 51, 37, 34, 18, 53, 45, 29, 34,
    47, 56, 38, 44, 46, 19, 43, 55, 16, 50, 15, 48, 27, 36, 20, 32, 47, 56, 43, 18,
    53, 51, 39, 51, 45, 15, 47, 53, 40, 37, 11, 56, 48, 34, 39, 18, 53, 47, 55, 14,
    50, 23, 18, 43, 24, 43, 44, 51, 38, 55, 40, 50, 28, 18, 46, 71
]

def getMixinKey(orig: str):
    """计算 B站 WBI 签名"""
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

class Spider(Spider):
    def getName(self):
        return "哔哩歌曲[PY]"

    def init(self, extend):
        pass

    def destroy(self):
        pass

    # ================= 主页分类 =================
    def homeContent(self, filter):
        # 直接把歌星列表写死在这里，以后不用改
        singers = [
            {"type_name": "韩宝仪", "type_id": "hanbaoyi"},
            {"type_name": "杨钰莹", "type_id": "yangyuying"},
            {"type_name": "蔡幸娟", "type_id": "caixingjuan"},
            {"type_name": "龙飘飘", "type_id": "longpiaopiao"},
            {"type_name": "林翠萍", "type_id": "lincuiping"}
        ]
        return {
            "class": singers
        }

    # ================= 分类详情（关键） =================
    def categoryContent(self, tid, page, filter, ext):
        # tid 就是上面的 type_id
        return self.searchContent(tid, page)

    def searchContent(self, key, page):
        videos = []
        
        # 1. 准备 WBI 签名所需的 wts (当前时间戳)
        wts = str(int(time.time()))
        
        # 2. 构造查询参数
        params = {
            'keyword': key,
            'page': page,
            'search_type': 'video',  # 搜索视频
            'wts': wts
        }
        
        # 3. 计算 w_rid (签名)
        # 先排序参数并编码
        encoded_params = urlencode(sorted(params.items()))
        w_rid = getMixinKey(encoded_params)
        
        # 4. 组装最终 URL
        url = f'https://api.bilibili.com/x/web-interface/wbi/search/all/v2?{encoded_params}&w_rid={w_rid}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }

        # 5. 请求数据
        rsp = self.fetch(url, headers=headers)
        data = json.loads(rsp.text)
        
        # 6. 解析数据 (适配 B站新结构)
        if data.get('code') == 0:
            # 注意：B站现在把所有结果都包在 result -> video 里
            video_list = data.get('data', {}).get('result', [])
            
            # 有时候 result 是混合的，确保我们取的是 video 类型
            if video_list and isinstance(video_list, list):
                for item in video_list:
                    # 检查 item 是否有 title 和 bvid
                    if 'title' in item and 'bvid' in item:
                        title = item['title']
                        # B站标题有 HTML 标签，需要替换掉
                        title = title.replace('<em class="keyword">', '').replace('</em>', '')
                        
                        videos.append({
                            'vod_id': item['bvid'],
                            'vod_name': title,
                            'vod_pic': item.get('pic', ''),
                            'vod_remarks': f"{item.get('duration', '00:00')}  播放:{item.get('play', 0)}"
                        })
        
        # 7. 返回结果 (OK影视要求的格式)
        return {
            "page": page,
            "pagecount": 9999, # 设为大数，让壳子一直滑
            "limit": 30,
            "total": len(videos),
            "list": videos
        }

    # ================= 播放地址 (占位) =================
    def detailContent(self, array):
        pass

    def searchContentPage(self, key, quick, page):
        pass

    def playerContent(self, flag, id, vipFlags):
        pass
