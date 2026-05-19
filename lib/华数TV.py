# -*- coding: utf-8 -*-
#//新时代青年为您提示:作品内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请者 将及时删除侵权内容
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
import sys
import json
import base64
import urllib.parse

sys.path.append('..')

xurl = "https://www.wasu.cn"

headerx = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{'' + match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{'' + match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "961", "type_name": "电影"},
                            {"type_id": "962", "type_name": "电视剧"},
                            {"type_id": "963", "type_name": "少儿"},
                            {"type_id": "965", "type_name": "综艺"},
                            {"type_id": "966", "type_name": "新闻"}
                            ],

                  }

        return result

    def homeVideoContent(self):
        videos = []
        detail = requests.get(url='https://mcspapp.5g.wasu.tv/bvradio_app/hzhs/recommendServlet?functionName=getRecommond&modeId=1033&page=1&pageSize=10&siteId=1000101', headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        js1=json.loads(res)
        x=[1,3,5,7]
        for q in x:
            for i in js1['data'][q]['childModels'][0]['manualList']:
                name=i['title']
                pic=i['pPic']
                id=i['id']
                remark=i['episodeDesc']
                video = {
                    "vod_id": id,
                    "vod_name":  name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                         }
                videos.append(video)

        result = {'list': videos}
        return result



    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        detail = requests.get(url=f'https://ups.5g.wasu.tv/rmp-user-suggest/1000101/hzhs/searchServlet?functionName=getNewsSearchedByCondition&nodeId={cid}&nodeTag=%E5%85%A8%E9%83%A8&yearTag=%E5%85%A8%E9%83%A8&countryTag=%E5%85%A8%E9%83%A8&orderType=0&pageSize=40&page={pg}&keyword=&siteId=1000101', headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        js1=json.loads(res)
        for i in js1['data']:
            name=i['title']
            id=str(cid) +','+str(i['newsId'])
            pic = i['pPic']
            remark = i['episodeDesc']

            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks":remark
                    }
            videos.append(video)
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        cid,id=did.split(',')

        result = {}
        videos = []
        res1 = requests.get(url=f'https://mcspapp.5g.wasu.tv/bvradio_app/hzhs/newsServlet?siteId=1000101&functionName=getCurrentNews&nodeId={cid}&newsId={id}&platform=web', headers=headerx)
        res1.encoding = "utf-8"
        res = res1.text
        js1=json.loads(res)

        play_url=''

        actor = js1['data']['actor']

        director = js1['data']['director']

        vod_area = js1['data']['countryTag']

        remark1 = js1['data']['pubTime']
        remark2 = js1['data']['episodeDesc']        
        remark = "更新时间" + remark1 + ' ' + remark2

        content = js1['data']['newsAbstract']

        for i in js1['data']['vodList']:
            name = i['title']
            vid = str(i['vodId'])
            play_url += name + '$' + 'https://www.wasu.cn/teleplay-detail/' + cid + '/' + id + '/' + vid + '#'
        play_url = play_url[:-1]

        videos.append({
            "vod_id": did,
            "vod_actor": actor,
            "vod_director": director,
            "vod_content": content,
            "vod_remarks": remark,            
            "vod_area": vod_area,
            "vod_play_from": '华数TV',
            "vod_play_url": play_url
        })

        result = {'list': videos}
        return result
    def playerContent(self, flag, id, vipFlags):
             return  {'jx':1,'parse': 1, 'url': id, 'header': headerx}

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = '1'

        url = f'https://ups.5g.wasu.tv/rmp-user-suggest/1000101/hzhs/searchServlet?functionName=getServiceAndNewsSearch&keyword={key}&pageSize=10&page={page}&siteId=1000101'


        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        js1=json.loads(res)
        for i in js1['data']['videoDataList']:
            id=str(i['nodeId'])+','+str(i['newsId'])
            name=i['title']
            pic=i['pPic']
            remark=i['episodeDesc']


            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
                    }
            videos.append(video)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def searchContent(self, key, quick,pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None