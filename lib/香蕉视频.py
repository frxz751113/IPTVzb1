# coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import time
import urllib.parse
import re
import requests
from lxml import etree
from urllib.parse import urljoin
import base64
import hashlib

class Spider(Spider):
    
    def getName(self):
        return "苹果视频"
    
    def init(self, extend=""):
        self.host = "https://618041.xyz"
        self.api_host = "https://h5.xxoo168.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': self.host
        }
        # 定义分类列表
        self.classes = [
            {'type_id': '618041.xyz_1', 'type_name': '全部视频'},
            {'type_id': '618041.xyz_13', 'type_name': '香蕉精品'},
            {'type_id': '618041.xyz_22', 'type_name': '制服诱惑'},
            {'type_id': '618041.xyz_6', 'type_name': '国产视频'},
            {'type_id': '618041.xyz_8', 'type_name': '清纯少女'},
            {'type_id': '618041.xyz_9', 'type_name': '辣妹大奶'},
            {'type_id': '618041.xyz_10', 'type_name': '女同专属'},
            {'type_id': '618041.xyz_11', 'type_name': '素人出演'},
            {'type_id': '618041.xyz_12', 'type_name': '角色扮演'},
            {'type_id': '618041.xyz_20', 'type_name': '人妻熟女'},
            {'type_id': '618041.xyz_23', 'type_name': '日韩剧情'},
            {'type_id': '618041.xyz_21', 'type_name': '经典伦理'},
            {'type_id': '618041.xyz_7', 'type_name': '成人动漫'},
            {'type_id': '618041.xyz_14', 'type_name': '精品二区'}
        ]

    def html(self, content):
        """将HTML内容转换为可查询的对象"""
        try:
            return etree.HTML(content)
        except:
            return None

    def regStr(self, pattern, string, index=1):
        """正则表达式提取字符串"""
        try:
            match = re.search(pattern, string, re.IGNORECASE)
            if match and len(match.groups()) >= index:
                return match.group(index)
        except:
            pass
        return ""

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        """获取首页内容和分类"""
        result = {}
        result['class'] = self.classes
        try:
            rsp = self.fetch(self.host, headers=self.headers)
            doc = self.html(rsp.text)
            videos = self._get_videos(doc, limit=20)
            result['list'] = videos
        except Exception as e:
            result['list'] = []
        return result

    def homeVideoContent(self):
        """分类定义 - 兼容性方法"""
        return {'class': self.classes}

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容"""
        try:
            domain, type_id = tid.split('_')
            url = f"https://{domain}/index.php/vod/type/id/{type_id}.html"
            if pg and pg != '1':
                url = url.replace('.html', f'/page/{pg}.html')
            
            rsp = self.fetch(url, headers=self.headers)
            doc = self.html(rsp.text)
            videos = self._get_videos(doc, category_id=type_id, limit=20)
            
            pagecount = 50  # 默认值
            try:
                page_elements = doc.xpath('//div[@class="mypage"]/a')
                if page_elements:
                    for elem in page_elements:
                        if '尾页' in elem.text or '最后一页' in elem.text:
                            href = elem.xpath('./@href')[0]
                            match = re.search(r'/page/(\d+)\.html', href)
                            if match:
                                pagecount = int(match.group(1))
                                break
            except:
                pass
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 20,
                'total': pagecount * 20
            }
        except Exception as e:
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        """搜索功能"""
        try:
            search_url = f"{self.host}/index.php/vod/type/id/1/wd/{urllib.parse.quote(key)}/page/{pg}.html"
            rsp = self.fetch(search_url, headers=self.headers)
            if not rsp or rsp.status_code != 200:
                return {'list': []}
            
            doc = self.html(rsp.text)
            if not doc:
                return {'list': []}
            
            videos = self._get_videos(doc, limit=20)
            
            pagecount = 5  # 默认值
            try:
                page_elements = doc.xpath('//div[@class="mypage"]/a')
                if page_elements:
                    for elem in page_elements:
                        if '尾页' in elem.text or '最后一页' in elem.text:
                            href = elem.xpath('./@href')[0]
                            match = re.search(r'/page/(\d+)\.html', href)
                            if match:
                                pagecount = int(match.group(1))
                                break
            except:
                pass
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 20,
                'total': pagecount * 20
            }
        except Exception as e:
            return {'list': []}

    def detailContent(self, ids):
        """详情页面"""
        try:
            vid = ids[0]
            
            if vid.startswith('special_'):
                parts = vid.split('_')
                if len(parts) >= 4:
                    category_id = parts[1]
                    video_id = parts[2]
                    encoded_url = '_'.join(parts[3:])
                    play_url = urllib.parse.unquote(encoded_url)
                    
                    parsed_url = urllib.parse.urlparse(play_url)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    video_url = query_params.get('v', [''])[0]
                    pic_url = query_params.get('b', [''])[0]
                    
                    path_parts = parsed_url.path.split('/')
                    if len(path_parts) > 0:
                        encrypted_title = path_parts[-1].replace('.html', '')
                        title = self._decrypt_title(encrypted_title)
                    else:
                        title = "未知标题"
                    
                    return {
                        'list': [{
                            'vod_id': vid,
                            'vod_name': title,
                            'vod_pic': pic_url,
                            'vod_remarks': '',
                            'vod_year': '',
                            'vod_area': '',
                            'vod_actor': '',
                            'vod_director': '',
                            'vod_content': '',
                            'vod_play_from': '直接播放',
                            'vod_play_url': f"第1集${play_url}"
                        }]
                    }
            
            if '_' in vid and len(vid.split('_')) > 2:
                domain, category_id, video_id = vid.split('_')
            else:
                domain, video_id = vid.split('_')
            
            detail_url = f"https://{domain}/index.php/vod/detail/id/{video_id}.html"
            
            rsp = self.fetch(detail_url, headers=self.headers)
            doc = self.html(rsp.text)
            video_info = self._get_detail(doc, rsp.text, vid)
            return {'list': [video_info]} if video_info else {'list': []}
        except Exception as e:
            return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        """播放链接"""
        try:
            if id.startswith('special_'):
                parts = id.split('_')
                if len(parts) >= 4:
                    encoded_url = '_'.join(parts[3:])
                    play_url = urllib.parse.unquote(encoded_url)
                    
                    parsed_url = urllib.parse.urlparse(play_url)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    video_url = query_params.get('v', [''])[0]
                    
                    if video_url:
                        if video_url.startswith('//'):
                            video_url = 'https:' + video_url
                        elif not video_url.startswith('http'):
                            video_url = urljoin(self.host, video_url)
                        
                        return {'parse': 0, 'playUrl': '', 'url': video_url}
                    else:
                        return {'parse': 1, 'playUrl': '', 'url': play_url}
            
            if id.startswith('http'):
                parsed_url = urllib.parse.urlparse(id)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                video_url = query_params.get('v', [''])[0]
                if video_url:
                    video_url = urllib.parse.unquote(video_url)
                    if video_url.startswith('//'):
                        video_url = 'https:' + video_url
                    elif not video_url.startswith('http'):
                        video_url = urljoin(self.host, video_url)
                    
                    return {'parse': 0, 'playUrl': '', 'url': video_url}
                else:
                    return {'parse': 1, 'playUrl': '', 'url': id}

            if id.count('_') >= 2:
                parts = id.split('_')
                video_id = parts[-1]
            else:
                video_id = id.split('_')[-1]
            
            api_url = f"{self.api_host}/api/v2/vod/reqplay/{video_id}"
            
            api_headers = self.headers.copy()
            api_headers.update({
                'Referer': f"{self.host}/",
                'Origin': self.host,
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            api_response = self.fetch(api_url, headers=api_headers)
            if api_response and api_response.status_code == 200:
                data = api_response.json()
                
                if data.get('retcode') == 3:
                    video_url = data.get('data', {}).get('httpurl_preview', '')
                else:
                    video_url = data.get('data', {}).get('httpurl', '')
                
                if video_url:
                    video_url = video_url.replace('?300', '')
                    return {'parse': 0, 'playUrl': '', 'url': video_url}
            
            if '_' in id:
                domain, play_id = id.split('_')
                play_url = f"https://{domain}/html/kkyd.html?m={play_id}"
            else:
                play_url = f"{self.host}/html/kkyd.html?m={id}"
            return {'parse': 1, 'playUrl': '', 'url': play_url}
                
        except Exception as e:
            if '_' in id:
                domain, play_id = id.split('_')
                play_url = f"https://{domain}/html/kkyd.html?m={play_id}"
            else:
                play_url = f"{self.host}/html/kkyd.html?m={id}"
            return {'parse': 1, 'playUrl': '', 'url': play_url}

    def _get_videos(self, doc, category_id=None, limit=None):
        """获取影片列表"""
        try:
            videos = []
            elements = doc.xpath('//a[@class="vodbox"]')
            for elem in elements:
                video = self._extract_video(elem, category_id)
                if video:
                    videos.append(video)
            return videos[:limit] if limit and videos else videos
        except Exception as e:
            return []

    def _extract_video(self, element, category_id=None):
        """提取影片信息"""
        try:
            link = element.xpath('./@href')[0]
            if link.startswith('/'):
                link = self.host + link
            
            is_special_link = '/html/dcdc/' in link
            
            if is_special_link:
                parsed_url = urllib.parse.urlparse(link)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                video_url = query_params.get('v', [''])[0]
                pic_url = query_params.get('b', [''])[0]
                
                if video_url:
                    video_id_match = re.search(r'/([a-f0-9-]+)/video\.m3u8', video_url)
                    if video_id_match:
                        video_id = video_id_match.group(1)
                    else:
                        video_id = hashlib.md5(video_url.encode()).hexdigest()[:8]
                else:
                    video_id = str(hash(link) % 1000000)
                
                encoded_link = urllib.parse.quote(link)
                final_vod_id = f"special_{category_id}_{video_id}_{encoded_link}"
                
                title_elem = element.xpath('.//p[@class="km-script"]/text()')
                if not title_elem:
                    title_elem = element.xpath('.//p[contains(@class, "script")]/text()')
                if not title_elem:
                    return None
                
                title_encrypted = title_elem[0].strip()
                title = self._decrypt_title(title_encrypted)
                
                pic_elem = element.xpath('.//img/@data-original')
                if not pic_elem:
                    pic_elem = element.xpath('.//img/@src')
                pic = pic_elem[0] if pic_elem else pic_url
                
                if pic:
                    if pic.startswith('//'):
                        pic = 'https:' + pic
                    elif pic.startswith('/'):
                        pic = self.host + pic
                
                return {
                    'vod_id': final_vod_id,
                    'vod_name': title,
                    'vod_pic': pic,
                    'vod_remarks': '',
                    'vod_year': ''
                }
            else:
                vod_id = self.regStr(r'm=(\d+)', link)
                if not vod_id:
                    vod_id = str(hash(link) % 1000000)
                
                final_vod_id = f"618041.xyz_{vod_id}"
                if category_id:
                    final_vod_id = f"618041.xyz_{category_id}_{vod_id}"
                
                title_elem = element.xpath('.//p[@class="km-script"]/text()')
                if not title_elem:
                    title_elem = element.xpath('.//p[contains(@class, "script")]/text()')
                if not title_elem:
                    return None
                
                title_encrypted = title_elem[0].strip()
                title = self._decrypt_title(title_encrypted)
                
                pic_elem = element.xpath('.//img/@data-original')
                if not pic_elem:
                    pic_elem = element.xpath('.//img/@src')
                pic = pic_elem[0] if pic_elem else ''
                
                if pic:
                    if pic.startswith('//'):
                        pic = 'https:' + pic
                    elif pic.startswith('/'):
                        pic = self.host + pic
                
                return {
                    'vod_id': final_vod_id,
                    'vod_name': title,
                    'vod_pic': pic,
                    'vod_remarks': '',
                    'vod_year': ''
                }
        except Exception as e:
            return None

    def _decrypt_title(self, encrypted_text):
        """解密标题 - 使用网站的解密算法 (XOR 128)"""
        try:
            decrypted_chars = []
            for char in encrypted_text:
                code_point = ord(char)
                decrypted_code = code_point ^ 128
                decrypted_char = chr(decrypted_code)
                decrypted_chars.append(decrypted_char)
            
            decrypted_text = ''.join(decrypted_chars)
            decrypted_text = decrypted_text.replace('&nbsp;', ' ')
            return decrypted_text
        except Exception as e:
            return encrypted_text

    def _get_detail(self, doc, html_content, vid):
        """获取详情信息"""
        try:
            title = self._get_text(doc, ['//h1/text()', '//title/text()'])
            pic = self._get_text(doc, ['//div[contains(@class,"dyimg")]//img/@src', '//img[contains(@class,"poster")]/@src'])
            if pic and pic.startswith('/'):
                pic = self.host + pic
            desc = self._get_text(doc, ['//div[contains(@class,"yp_context")]/text()', '//div[contains(@class,"introduction")]//text()'])
            actor = self._get_text(doc, ['//span[contains(text(),"主演")]/following-sibling::*/text()'])
            director = self._get_text(doc, ['//span[contains(text(),"导演")]/following-sibling::*/text()'])

            play_from = []
            play_urls = []
            
            player_link_patterns = [
                re.compile(r'href="(.*?ar\.html.*?)"'),
                re.compile(r'href="(.*?kkyd\.html.*?)"'),
                re.compile(r'href="(.*?ar-kk\.html.*?)"'),
                re.compile(r'href="(.*?dcdc/.*?)"')
            ]
            
            player_links = []
            for pattern in player_link_patterns:
                matches = pattern.findall(html_content)
                player_links.extend(matches)
            
            if player_links:
                episodes = []
                for link in player_links:
                    full_url = urljoin(self.host, link)
                    episodes.append(f"第1集${full_url}")

                if episodes:
                    play_from.append("默认播放源")
                    play_urls.append('#'.join(episodes))

            if not play_from:
                return {
                    'vod_id': vid,
                    'vod_name': title,
                    'vod_pic': pic,
                    'type_name': '',
                    'vod_year': '',
                    'vod_area': '',
                    'vod_remarks': '',
                    'vod_actor': actor,
                    'vod_director': director,
                    'vod_content': desc,
                    'vod_play_from': '默认播放源',
                    'vod_play_url': f"第1集${vid}"
                }

            return {
                'vod_id': vid,
                'vod_name': title,
                'vod_pic': pic,
                'type_name': '',
                'vod_year': '',
                'vod_area': '',
                'vod_remarks': '',
                'vod_actor': actor,
                'vod_director': director,
                'vod_content': desc,
                'vod_play_from': '$$$'.join(play_from),
                'vod_play_url': '$$$'.join(play_urls)
            }
        except Exception as e:
            return None

    def _get_text(self, doc, selectors):
        """通用文本提取"""
        for selector in selectors:
            try:
                texts = doc.xpath(selector)
                for text in texts:
                    if text and text.strip():
                        return text.strip()
            except:
                continue
        return ''

    def fetch(self, url, headers=None, method='GET', data=None, timeout=10):
        """网络请求"""
        try:
            if headers is None:
                headers = self.headers
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            else:
                response = requests.post(url, headers=headers, data=data, timeout=timeout, verify=False)
            return response
        except Exception as e:
            return None

# 注册爬虫
if __name__ == '__main__':
    from base.spider import Spider as BaseSpider
    BaseSpider.register(Spider())