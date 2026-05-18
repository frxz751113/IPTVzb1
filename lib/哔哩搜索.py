# coding=utf-8
#!/usr/bin/python
import sys
import json
import time
import hashlib
import base64
from urllib.parse import urlencode, quote

sys.path.append('..')
from base.spider import Spider

# ================= WBI 签名辅助 =================
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 22, 24, 6, 11, 36, 41, 16, 0, 14, 25, 53, 57, 50, 38, 49, 61, 13, 23, 28, 33, 8, 60, 39, 34, 17, 5, 55, 40, 9, 31, 20, 29, 61, 19, 57, 7, 21, 51, 60, 12, 47, 44, 37, 38, 59, 43, 52, 42, 2, 1, 40, 41, 27, 55, 10, 16, 9, 58, 52, 48, 54, 30, 56, 25, 36, 20, 32, 47, 56, 43, 18, 53, 45, 29, 34, 47, 56, 38, 44, 46, 19, 43, 55, 16, 50, 15, 48, 27, 36, 20, 32, 47, 56, 43, 18, 53, 51, 39, 51, 45, 15, 47, 53, 40, 37, 11, 56, 48, 34, 39, 18, 53, 47, 55, 14, 50, 23, 18
]

def getMixinKey(orig: str):
    """计算 WBI 签名"""
    mixin_key = ''.join([orig[i] for i in mixinKeyEncTab])
    return mixin_key[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    """生成 WBI 签名并加入参数"""
    wbi_keys = [img_key, sub_key]
    curr_time = int(time.time())
    params['wts'] = curr_time
    
    # 过滤掉 None 和空值，并按 key 排序
    filtered_params = {k: v for k, v in params.items() if v is not None and v != ''}
    sorted_params = sorted(filtered_params.items(), key=lambda x: x[0])
    
    # 拼接成字符串
    query = urlencode(sorted_params)
    wbi_sign = md5(query + getMixinKey(wbi_keys[0] + wbi_keys[1]))
    params['w_rid'] = wbi_sign
    return params

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# ================= 主类 =================
class Spider(Spider):

    def getName(self):
        return "B站歌星搜索"

    def init(self, extend):
        # 这里的 Cookie 必须保持有效，否则搜索和播放都会出问题
        # 建议定期检查 Cookie 是否过期
        self.cookie = "_uuid=5E4B2B98-1014A-84D8-FA33-EC210C5BEC10DA82367infoc; buvid3=E9D0A426-85E9-E6C7-C75E-206A3E1BEB4D81910infoc; b_nut=1666168082; buvid4=4FC87B9C-3540-2275-688C-8612D3EA719B81910-022101916-ZLe640jXRAMHySuaCe9aUw==; rpdid=|(k|u)YYm)uY0J'uYYYuY)uuu; i-wanna-go-back=-1; fingerprint=9c214a6da0197a48e576ccf22e9f0ac7; buvid_fp_plain=undefined; nostalgia_conf=-1; DedeUserID=3493076028885079; DedeUserID__ckMd5=60a8757a1f4d6ae9; buvid_fp=9c214a6da0197a48e576ccf22e9f0ac7; CURRENT_QUALITY=80; b_ut=5; PVID=2; bp_video_offset_3493076028885079=undefined; bsource=search_google; SESSDATA=42b8ada6,1683277266,4bd05*b2; bili_jct=2dbe39aea02b41324395630a24d4775f; sid=89gnel66; innersign=0; b_lsid=9EF63922_1844D55A286; CURRENT_FNVAL=4048"
        
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

    # ================= 搜索 =================
    def searchContent(self, key, quick):
        # B站搜索接口
        url = "https://api.bilibili.com/x/web-interface/search/all/v2"
        
        # 构造参数
        params = {
            "keyword": key,
            "page": 1,
            "pagesize": 20
        }
        
        # 这里需要 img_key 和 sub_key 来算 WBI，如果不知道可以留空或者找其他方式，但为了稳定建议加上
        # 注意：如果你的 Cookie 是登录态，有时不需要 WBI 也能搜，但加上更稳
        # 假设我们没有 img_key 和 sub_key，先用简化版，主要靠 Cookie 撑着
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
            "Referer": "https://search.bilibili.com/all?keyword=" + quote(key)
        }
        
        # 模拟请求
        # 注意：这里用 requests 的话需要导入，但根据你的环境可能不同
        # 为了通用性，这里用伪代码展示逻辑，实际运行请用你的 spider 基类方法
        # 比如：ret = self.fetch(url, headers=headers, params=params)
        # 但既然你的基类是 Spider，我们假设有这个方法
        
        # 由于我不知道你的基类具体 fetch 怎么写，我按标准写法给你
        import requests
        session = requests.Session()
        response = session.get(url, headers=headers, params=params)
        data = response.json()
        
        videos = []
        if data.get('code') == 0:
            for item in data.get('data', {}).get('result', []):
                if item.get('result_type') == 'video':
                    for video in item.get('data', []):
                        # 提取视频信息
                        title = video.get('title', '').replace('<em class="keyword">', '').replace('</em>', '')
                        bvid = video.get('bvid', '')
                        aid = video.get('aid', '')
                        cover = video.get('pic', '')
                        duration = video.get('duration', '')
                        pubdate = video.get('pubdate', '')
                        
                        videos.append({
                            "vod_id": bvid,
                            "vod_name": title,
                            "vod_pic": cover,
                            "vod_remarks": duration
                        })
        
        return videos

    # ================= 详情 =================
    def detailContent(self, array):
        # array 是 vod_id，即 bvid
        bvid = array[0]
        
        url = f"https://api.bilibili.com/x/player/wbi/v1/playurl?bvid={bvid}&cid=&qn=64&fnval=4048"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
            "Referer": f"https://www.bilibili.com/video/{bvid}"
        }
        
        import requests
        session = requests.Session()
        response = session.get(url, headers=headers)
        data = response.json()
        
        # 提取播放地址
        play_url = ""
        if data.get('code') == 0:
            # 获取第一个视频流
            durl = data.get('data', {}).get('durl', [])
            if durl:
                play_url = durl[0].get('url', '')
        
        # 获取视频详情
        info_url = f"https://api.bilibili.com/x/web-interface/view/detail?bvid={bvid}"
        info_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
            "Referer": f"https://www.bilibili.com/video/{bvid}"
        }
        info_response = session.get(info_url, headers=info_headers)
        info_data = info_response.json()
        
        title = "未知"
        pic = ""
        desc = ""
        if info_data.get('code') == 0:
            video_data = info_data.get('data', {}).get('view', {})
            title = video_data.get('title', '未知')
            pic = video_data.get('pic', '')
            desc = video_data.get('desc', '')
        
        # 构造返回格式
        vod_list = [
            {
                "vod_id": bvid,
                "vod_name": title,
                "vod_pic": pic,
                "vod_remarks": "",
                "vod_content": desc,
                "vod_play_from": "B站",
                "vod_play_url": play_url  # 这里直接放 URL，或者如果需要多线路可以放列表
            }
        ]
        
        return vod_list

    # ================= 播放 =================
    def playerContent(self, flag, id, vipFlags):
        # flag 是播放来源，id 是 vod_id，这里 id 就是 bvid
        bvid = id
        
        url = f"https://api.bilibili.com/x/player/wbi/v1/playurl?bvid={bvid}&cid=&qn=64&fnval=4048"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
            "Referer": f"https://www.bilibili.com/video/{bvid}"
        }
        
        import requests
        session = requests.Session()
        response = session.get(url, headers=headers)
        data = response.json()
        
        play_url = ""
        if data.get('code') == 0:
            durl = data.get('data', {}).get('durl', [])
            if durl:
                play_url = durl[0].get('url', '')
        
        # 如果 play_url 为空，尝试获取备用地址
        if not play_url:
            # 可能是需要特定格式，或者接口变了
            # 这里可以加个降级处理，比如返回错误信息
            return {
                "header": "",
                "parse": 0,
                "playUrl": "",
                "url": ""
            }
        
        # 返回播放地址
        return {
            "header": "",
            "parse": 0,
            "playUrl": play_url,
            "url": play_url
        }
