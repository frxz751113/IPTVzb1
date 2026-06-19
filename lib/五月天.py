# -*- coding: utf-8 -*-
import re
from pyquery import PyQuery as pq
from base.spider import Spider
#发布页：https://qswyt4444.com/page
class Spider(Spider):
    def init(self, extend=""):
        self.host = "https://qswyt03.cc"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Referer':f'{self.host}/','Accept-Language':'zh-CN,zh;q=0.9'}
    def getName(self):return "QS五月天"
    def isVideoFormat(self,url):return url.lower().endswith('.m3u8')
    def manualVideoCheck(self):return True
    def destroy(self):pass
    def homeContent(self,filter):
        result={'class':[],'filters':{}}
        try:
            res=self.fetch(self.host,headers=self.headers)
            d=pq(res.text)
            items=d('a[href^="/movie/block/"]')
            seen=set()
            for item in items.items():
                href=item.attr('href')
                match=re.search(r'/movie/block/(\d+)',href) if href else None
                if match:
                    tid=match.group(1)
                    if tid not in seen:
                        name=item.text().strip() or item.find('span').text().strip()
                        if name:
                            result['class'].append({'type_name':name,'type_id':tid})
                            seen.add(tid)
        except:pass
        if not result['class']:
            result['class']=[{'type_name':k,'type_id':v} for k,v in {'最新':'newest','国产':'50','淫荡少妇':'21','人妻诱惑':'22','大奶萝莉':'23','丝袜制服':'24','强奸':'45','群P':'46'}.items()]
        return result
    def homeVideoContent(self):
        try:
            res=self.fetch(self.host,headers=self.headers)
            return {'list':self._parseVideoList(res.text)}
        except:return {'list':[]}
    def categoryContent(self,tid,pg,filter,extend):
        try:
            url=f'{self.host}/movie/block/{tid}?page={pg}' if tid.isdigit() else f'{self.host}/movie/{tid}?page={pg}'
            res=self.fetch(url,headers=self.headers)
            return {'list':self._parseVideoList(res.text),'page':int(pg),'pagecount':999,'limit':20,'total':9999}
        except:return {'list':[]}
    def detailContent(self,ids):
        if not ids:return {'list':[]}
        tid=ids[0]
        try:
            url=tid if tid.startswith('http') else f'{self.host}{tid}' if tid.startswith('/') else f'{self.host}/movie/detail/{tid}'
            res=self.fetch(url,headers=self.headers)
            content=res.text
            title=''
            pic=''
            t_match=re.search(r'<meta property="og:title" content="(.*?)">',content)
            if t_match:title=t_match.group(1).split(' - ')[0]
            p_match=re.search(r'<meta property="og:image" content="(.*?)">',content)
            if p_match:pic=p_match.group(1)
            matches=re.findall(r'(/api/m3u8/p/[a-zA-Z0-9]+\.m3u8)',content)
            seen=set()
            sources,urls=[],[]
            for m in matches:
                full=m if m.startswith('http') else f"{self.host}{m}"
                if full not in seen:
                    seen.add(full)
                    sources.append(f"线路{len(sources)+1}")
                    urls.append(full)
            vod={'vod_id':tid,'vod_name':title,'vod_pic':pic,'type_name':'','vod_year':'','vod_area':'','vod_remarks':'','vod_actor':'','vod_director':'','vod_content':'','vod_play_from':'$$$'.join(sources),'vod_play_url':'$$$'.join(urls)}
            return {'list':[vod]}
        except:return {'list':[]}
    def searchContent(self,key,quick,pg="1"):
        try:
            url=f'{self.host}/search/{key}?page={pg}'
            res=self.fetch(url,headers=self.headers)
            return {'list':self._parseVideoList(res.text)}
        except:return {'list':[]}
    def playerContent(self,flag,id,vipFlags):
        return {'parse':0,'url':id,'header':{'User-Agent':self.headers['User-Agent']}}
    def localProxy(self,param):pass
    def _parseVideoList(self, html):
        videos = []
        try:
            d = pq(html)
            items = d('.listing_flex')
            for item in items.items():
                a_tag = item.find('a.listing_a')
                href = a_tag.attr('href')
                if not href or '/movie/detail/' not in href: continue
                
                vid = href.split('/')[-1]
                title = item.find('.video_title').text()
                pic = ''
                pic_match = re.search(f'"{vid}".*?"(https?://[^"]+)"', html)
                if pic_match:
                    pic = pic_match.group(1)
                remarks = item.find('.absolute_bottom_right span').text()
                
                videos.append({
                    'vod_id': href,
                    'vod_name': title,
                    'vod_pic': pic,
                    'vod_remarks': remarks
                })
        except: pass
        return videos
