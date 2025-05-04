#本程序只适用于酒店源的检测,请勿移植他用
import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import os
import threading
from queue import Queue
import queue
from datetime import datetime
import replace
import fileinput
from tqdm import tqdm
from pypinyin import lazy_pinyin
from opencc import OpenCC
import base64
import cv2
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from translate import Translator  # 导入Translator类,用于文本翻译
# 扫源测绘空间地址
# 搜素关键词："iptv/live/zh_cn.js" && country="CN" && region="Hunan" && city="changsha"
# 搜素关键词："ZHGXTV" && country="CN" && region="Hunan" && city="changsha"
#"isShowLoginJs"智能KUTV管理
######################################################################################################################
######################################################################################################################
###########################################################ZHGX采集####################################################
######################################################################################################################
######################################################################################################################
import requests

urls = [
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODA4Ig%3D%3D", #808
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODg4OCI%3D" ,   #8888
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iOTk5OSI%3D",#9999
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODgi" ,   #88
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODAwMyI%3D" ,   #8003
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODg4Ig%3D%3D" ,   #888
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODA4OSI%3D" ,   #8089
    #"https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgcG9ydD0iODAwOSI%3D", #8009
]

def modify_urls(url):
    # 创建一个空列表用于存储修改后的 URL
    modified_urls = []
    # 找到 URL 中 IP 地址开始的索引位置,"//" 后两个字符开始为 IP 地址起始位置
    ip_start_index = url.find("//") + 2
    # 找到 URL 中 IP 地址结束的索引位置,从 ip_start_index 开始查找第一个 ":" 的位置
    ip_end_index = url.find(":", ip_start_index)
    # 找到 URL 中 IP 地址结束的索引位置,从 ip_start_index 开始查找第一个 ":" 的位置
    base_url = url[:ip_start_index]
    # 获取 URL 中的 IP 地址部分
    ip_address = url[ip_start_index:ip_end_index]
    # 获取 URL 中的端口部分
    port = url[ip_end_index:]
    # 定义一个字符串,表示 IP 地址的结尾部分
    ip_end = "/ZHGXTV/Public/json/live_interface.txt"
    # 遍历 1 到 255 的数字
    for i in range(1, 256):
        # 修改 IP 地址的最后一位数字
        modified_ip = f"{ip_address[:-1]}{i}"
        # 组合成新的 URL
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        # 将新的 URL 添加到列表中
        modified_urls.append(modified_url)
    # 返回修改后的 URL 列表
    return modified_urls

def is_url_accessible(url):
    try:
        # 发送 GET 请求,设置超时时间为 3 秒
        response = requests.get(url, timeout=3)
        # 如果响应状态码在 200 到 401 之间（包括 200 和 401）,则认为 URL 可访问
        if 200 <= response.status_code <= 401:
            return url
    except requests.exceptions.RequestException:
        # 如果请求过程中出现异常,不做任何处理,直接跳过
        pass
    return None

# 创建一个空列表用于存储结果
results = []
for url in urls:
    # 发送 GET 请求获取 URL 的内容
    response = requests.get(url)
    # 获取响应的文本内容
    page_content = response.text

    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"   # 设置匹配的格式,如 http://8.8.8.8:8888
    # 使用正则表达式在页面内容中查找所有符合格式的 URL
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理,ip第四位修改为1,并去重
        url = url.strip()
        # 找到 URL 中 IP 地址开始的索引位置,"//" 后两个字符开始为 IP 地址起始位置
        ip_start_index = url.find("//") + 2
        # 找到 URL 中 IP 地址结束的索引位置,从 ip_start_index 开始查找第一个 ":" 的位置
        ip_end_index = url.find(":", ip_start_index)
        # 找到 IP 地址中第一个 "." 的位置
        ip_dot_start = url.find(".") + 1
        # 找到 IP 地址中第二个 "." 的位置
        ip_dot_second = url.find(".", ip_dot_start) + 1
        # 找到 IP 地址中第三个 "." 的位置
        ip_dot_three = url.find(".", ip_dot_second) + 1
        # 获取 URL 的基础部分,即从开头到 IP 地址开始的部分
        base_url = url[:ip_start_index]  # http:// or https://
        # 获取 URL 中的 IP 地址部分,截取到第三个 "." 的位置
        ip_address = url[ip_start_index:ip_dot_three]
        # 获取 URL 中的端口部分
        port = url[ip_end_index:]
        # 定义一个字符串,表示 IP 地址的结尾部分为 "1"
        ip_end = "1"
        # 修改 IP 地址的最后一位为 "1"
        modified_ip = f"{ip_address}{ip_end}"
        # 组合成新的 URL
        x_url = f"{base_url}{modified_ip}{port}"
        # 将新的 URL 添加到列表中
        x_urls.append(x_url)
    urls = set(x_urls)  # 去重得到唯一的URL列表
    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            # 获取修改后的 URL 列表
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                # 提交任务,检查每个修改后的 URL 是否可访问
                futures.append(executor.submit(is_url_accessible, modified_url))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                # 如果 URL 可访问,将其添加到有效 URL 列表中
                valid_urls.append(result)
    for url in valid_urls:
        print(url)
    # 遍历网址列表,获取JSON文件并解析
    for url in valid_urls:
        try:
            # 发送GET请求获取JSON文件,设置超时时间为0.5秒
            json_url = f"{url}"
            response = requests.get(json_url, timeout=3)################################
            json_data = response.content.decode('utf-8')
            try:
                    # 按行分割数据
             lines = json_data.split('\n')
             excluded_keywords = ['udp', 'rtp']   
             for line in lines:
                 if 'hls' in line and all(keyword not in line for keyword in excluded_keywords):
                        line = line.strip()
                        if line:
                            name, channel_url = line.split(',')
                            urls = channel_url.split('/', 3)
                            url_data = json_url.split('/', 3)
                            if len(urls) >= 3:
                                urld = (f"{urls[0]}//{url_data[2]}/{urls[3]}")
                            else:
                                urld = (f"{urls}")
                            #print(f"{name},{urld}")  #关闭频道名称和频道地址打印,缩短运行时间
                        if name and urld:
                            name = name.replace("高清电影", "影迷电影")                            
                            name = name.replace("中央", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("超高", "")
                            name = name.replace("频道", "")
                            name = name.replace("靓妆", "女性时尚")
                            name = name.replace("本港台", "TVB星河")
                            name = name.replace("汉3", "汉")
                            name = name.replace("汉4", "汉")
                            name = name.replace("汉5", "汉")
                            name = name.replace("汉6", "汉")
                            name = name.replace("CHC动", "动")
                            name = name.replace("CHC家", "家")
                            name = name.replace("CHC影", "影")
                            name = name.replace("-", "")
                            name = name.replace("都市6", "都市")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace(")", "")
                            name = name.replace("L", "")
                            name = name.replace("新农村", "河南新农村")
                            name = name.replace("百姓调解", "河南百姓调解")
                            name = name.replace("法治", "河南法治")
                            name = name.replace("睛彩中原", "河南睛彩")
                            name = name.replace("军事", "河南军事")
                            name = name.replace("梨园", "河南梨园")
                            name = name.replace("相声小品", "河南相声小品")
                            name = name.replace("移动戏曲", "河南移动戏曲")
                            name = name.replace("都市生活", "河南都市生活")
                            name = name.replace("民生", "河南民生")
                            name = name.replace("CCTVNEWS", "CCTV13")
                            name = name.replace("cctv", "CCTV")
                            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV2经济", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV4欧洲", "CCTV4")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7农业", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV8纪录", "CCTV9")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("央视14少儿", "CCTV14")
                            name = name.replace("CCTV少儿超", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("SCTV5四川影视）", "SCTV5")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV17军农", "CCTV17")
                            name = name.replace("CCTV17农业", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            name = name.replace("CCTV5+赛事", "CCTV5+")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV5赛事", "CCTV5+")
                            name = name.replace("凤凰中文台", "凤凰中文")
                            name = name.replace("凤凰资讯台", "凤凰资讯")
                            name = name.replace("CCTV4K测试）", "CCTV4")
                            name = name.replace("CCTV164K", "CCTV16")
                            name = name.replace("上海东方卫视", "上海卫视")
                            name = name.replace("东方卫视", "上海卫视")
                            name = name.replace("内蒙卫视", "内蒙古卫视")
                            name = name.replace("福建东南卫视", "东南卫视")
                            name = name.replace("广东南方卫视", "南方卫视")
                            name = name.replace("湖南金鹰卡通", "金鹰卡通")
                            name = name.replace("炫动卡通", "哈哈炫动")
                            name = name.replace("卡酷卡通", "卡酷少儿")
                            name = name.replace("卡酷动画", "卡酷少儿")
                            name = name.replace("BRTVKAKU少儿", "卡酷少儿")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("嘉佳卡通", "佳嘉卡通")
                            name = name.replace("世界地理", "地理世界")
                            name = name.replace("CCTV世界地理", "地理世界")
                            name = name.replace("BTV北京卫视", "北京卫视")
                            name = name.replace("BTV冬奥纪实", "冬奥纪实")
                            name = name.replace("东奥纪实", "冬奥纪实")
                            name = name.replace("卫视台", "卫视")
                            name = name.replace("湖南电视台", "湖南卫视")
                            name = name.replace("少儿科教", "少儿")
                            name = name.replace("TV星河2）", "星河")
                            name = name.replace("影视剧", "影视")
                            name = name.replace("电视剧", "影视")
                            name = name.replace("奥运匹克", "")
                            urld = urld.replace("index.m3u8", "index.m3u8?$智慧光迅听说名字越长越好看")
                            results.append(f"{name},{urld}")
            except:
                continue
        except:
            continue
channels = []
for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))
with open("iptv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        print(result)  #关闭频道名称和频道地址打印,缩短运行时间
print("频道列表文件iptv.txt获取完成！")




for line in fileinput.input("iptv.txt", inplace=True):  #打开文件,并对其进行关键词原地替换
    line = line.replace("河南河南", "河南")
    line = line.replace("河南河南", "河南")  
    line = line.replace("河南法制", "河南法治")          
    line = line.replace("国防河南军事", "")             
    line = line.replace("CCTV12法制", "CCTV12")             
    line = line.replace("CCTV15+音乐", "CCTV15")             
    line = line.replace("CCTV17农村农业", "CCTV17")             
    line = line.replace("（福建卫视）", "")               
    line = line.replace("公共,http://171.8", "河南公共,http://171.8")   
    line = line.replace("新闻,http://171.8", "河南新闻,http://171.8")  
    line = line.replace("影视,http://171.8", "河南电视剧,http://171.8")             
    line = line.replace("河南影视,http://171.13", "河南电视剧,http://171.13")                       
    line = line.replace("广东大湾区卫视", "大湾区卫视")             
    line = line.replace("吉林延边卫视", "延边卫视")             
    line = line.replace("国防河南军事", "国防军事")             
    line = line.replace("都市生活", "都市")               
    line = line.replace("都市生活6", "都市")                   
    print(line, end="")  #设置end="",避免输出多余的换行符
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
#定义智慧桌面采集地址
urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9Ijk5OTki",  #9999
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9IjgwODIi",  # 8082
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9IjgwOTYi",  # 8096
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9Ijk5MDEi",  # 9901
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9IjgwODgi",  # 8088
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Inl1bGluIg==",  #玉林
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHBvcnQ9IjgxODEii",#8181
]
def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)
    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=3)
        if 200 <= response.status_code <= 401:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

results = []
for url in urls:
    response = requests.get(url)
    page_content = response.text
    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式,如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理,ip第四位修改为1,并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    urls = set(x_urls)  # 去重得到唯一的URL列表
    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)
    for url in valid_urls:
        print(url)

    # 遍历网址列表,获取JSON文件并解析
    for url in valid_urls:
        try:
            ip_start_index = url.find("//") + 2
            # 找到URL中"//"的位置,并从该位置的下一个字符开始截取,直到找到第一个"/"字符
            ip_dot_start = url.find(".") + 1
            # 从URL中找到第一个"."的位置,并从该位置的下一个字符开始截取,直到找到第二个"/"字符
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]  # 截取URL中的协议部分,例如"http://"或"https://"
            # 截取从"//"之后到第一个"/"之前的部分,这通常是IP地址或域名
            ip_address = url[ip_start_index:ip_index_second]
            # 构造一个新的URL,由基本URL和IP地址组成
            url_x = f"{base_url}{ip_address}"
            # 将原始URL赋值给json_url变量
            json_url = f"{url}"
            # 使用requests库发起一个GET请求到json_url,超时时间设置为3秒
            response = requests.get(json_url, timeout=3)
            # 将响应的内容解析为JSON格式
            json_data = response.json()
            try:
            # 尝试执行以下代码块,如果发生错误则跳转至except部分
                # 解析JSON文件,获取'data'键对应的列表中的每个元素
                for item in json_data['data']:
                    # 检查每个元素是否为字典类型
                    if isinstance(item, dict):
                        # 从字典中获取'name'键的值,如果键不存在则返回None
                        name = item.get('name')
                        # 从字典中获取'url'键的值,如果键不存在则返回None
                        urlx = item.get('url')
                        # 如果urlx包含'udp'或'rtp'字符串,则跳过当前循环的剩余部分
                        if 'udp' in urlx or 'rtp' in urlx:   # or 'CCTV' in name or '卫视' in name
                            continue  # 跳过包含'udp'或'rtp'的url
                        # 如果urlx以'http'开头,则直接使用这个url
                        if 'http' in urlx:
                            urld = f"{urlx}"
                        # 如果urlx不以'http'开头,则在前面添加一个前缀（注意：这里的url_x变量未在代码中定义）
                        else:
                            urld = f"{url_x}{urlx}"
                        #print(f"{name},{urld}")  #关闭频道名称和频道地址打印,缩短运行时间
                        if name and urld:
                            name = name.replace("高清电影", "影迷电影")                            
                            name = name.replace("中央", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("超高", "")
                            name = name.replace("频道", "")
                            name = name.replace("汉1", "汉")
                            name = name.replace("汉2", "汉")
                            name = name.replace("汉3", "汉")
                            name = name.replace("汉4", "汉")
                            name = name.replace("汉5", "汉")
                            name = name.replace("汉6", "汉")
                            name = name.replace("CHC动", "动")
                            name = name.replace("CHC家", "家")
                            name = name.replace("CHC影", "影")
                            name = name.replace("-", "")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace("综合体育", "")
                            name = name.replace(")", "")
                            name = name.replace("CHC", "")
                            name = name.replace("L", "")
                            name = name.replace("002", "AA酒店MV")
                            name = name.replace("测试002", "凤凰卫视")
                            name = name.replace("测试003", "凤凰卫视")
                            name = name.replace("测试004", "私人影院")
                            name = name.replace("测试005", "私人影院")
                            name = name.replace("测试006", "东森洋片")
                            name = name.replace("测试007", "东森电影")
                            name = name.replace("测试008", "AXN电影")
                            name = name.replace("测试009", "好莱坞电影")
                            name = name.replace("测试010", "龙祥电影")
                            name = name.replace("莲花台", "凤凰香港")
                            name = name.replace("测试014", "凤凰资讯")
                            name = name.replace("测试015", "未知影视")
                            name = name.replace("TV星河", "空")
                            name = name.replace("305", "酒店影视1")
                            name = name.replace("306", "酒店影视2")
                            name = name.replace("307", "酒店影视3")
                            name = name.replace("CMIPTV", "")
                            name = name.replace("cctv", "CCTV")
                            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV4欧洲", "CCTV4")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7农业", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV8纪录", "CCTV9")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("央视14少儿", "CCTV14")
                            name = name.replace("CCTV少儿超", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV17军农", "CCTV17")
                            name = name.replace("CCTV17农业", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            name = name.replace("CCTV5+赛事", "CCTV5+")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("CCTV5赛事", "CCTV5+")
                            name = name.replace("凤凰中文台", "凤凰中文")
                            name = name.replace("凤凰资讯台", "凤凰资讯")
                            name = name.replace("CCTV4K测试）", "CCTV4")
                            name = name.replace("CCTV164K", "CCTV16")
                            name = name.replace("上海东方卫视", "上海卫视")
                            name = name.replace("东方卫视", "上海卫视")
                            name = name.replace("内蒙卫视", "内蒙古卫视")
                            name = name.replace("福建东南卫视", "东南卫视")
                            name = name.replace("广东南方卫视", "南方卫视")
                            name = name.replace("湖南金鹰卡通", "金鹰卡通")
                            name = name.replace("炫动卡通", "哈哈炫动")
                            name = name.replace("卡酷卡通", "卡酷少儿")
                            name = name.replace("卡酷动画", "卡酷少儿")
                            name = name.replace("BRTVKAKU少儿", "卡酷少儿")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("优曼卡通", "优漫卡通")
                            name = name.replace("嘉佳卡通", "佳嘉卡通")
                            name = name.replace("世界地理", "地理世界")
                            name = name.replace("CCTV世界地理", "地理世界")
                            name = name.replace("BTV北京卫视", "北京卫视")
                            name = name.replace("BTV冬奥纪实", "冬奥纪实")
                            name = name.replace("东奥纪实", "冬奥纪实")
                            name = name.replace("卫视台", "卫视")
                            name = name.replace("湖南电视台", "湖南卫视")
                            name = name.replace("少儿科教", "少儿")
                            name = name.replace("TV星河2）", "星河")
                            name = name.replace("影视剧", "影视")
                            name = name.replace("电视剧", "影视")
                            name = name.replace("奥运匹克", "")
                            name = name.replace("TVBTVB", "TVB")
                            name = name.replace("星空卫视", "动物杂技")
                            urld = urld.replace("key", "$不见黄河心不死") #key=txiptv&playlive=1&down=1  key=txiptv&playlive=0&authid=0  key=txiptv&playlive=1&authid=0
                            results.append(f"{name},{urld}")
            except:
                continue
        except:
            continue
channels = []
for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))
with open("iptv.txt", 'a', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        print(result)  #关闭频道名称和频道地址打印,缩短运行时间
print("频道列表文件iptv.txt追加写入成功！")


######################################################################
#定义一个关键词组,用于排除掉含有关键词的行
keywords = ['南宁#', '公共#', '教育', '新闻', 'SCTV#', '动漫', '卡通', '少儿', '中国', '玉林', '陆川', '新疆', '摄影']
with open('iptv.txt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()
filtered_lines = [line for line in lines if not any(keyword in line for keyword in keywords)]
with open('iptv.txt', 'w', encoding='utf-8') as outfile:
    outfile.writelines(filtered_lines)
#####################################################################

#####################################定义替换规则的字典,对整行内的多余标识内容进行替换
replacements = {
    	"2珠江": "TVB星河",
        "T[": "T",
    	"BM20": "",
    	"1ZX": "凤凰资讯HD",
    	"2ZW）": "凤凰中文HD",
    	"3XG": "凤凰香港",
    	"4ZW": "凤凰中文",
    	"5ZX": "凤凰资讯", 
        "星河台": "星河",   
        "dx[": "[",
        "g[": "[",
        "P[": "+[",
        "lt[": "[",
        "电信": "",
        "卫视高清": "卫视",
        "SCTV5": "",
        "T,": ",",
        "dx,": ",",
        "g,": ",",
        "TVBTVB星河": "TVB星河",
        "5音乐台": "CCTV15",
        "天映": "天映经典[🏠]",
        "星河": "星河[🏠]",
        "翡翠台": "翡翠台[🏠]",
        "环球旅游": "环球旅游[🏠]",
        "凤凰香港": "凤凰香港[🏠]",
        "凤凰中文": "凤凰中文[🏠]",
        "凤凰资讯": "凤凰资讯[🏠]",
    	"BM9家庭影院": "东森电影[🏠]",
    	"BM15广东影视": "广东影视[🏠]",
    	"3X电影": "龙祥时代[🏠]",
    	"4DS": "东森电影[🏠]",
        "电影[🏠]电影": "电影[🏠]",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": ""
}
# 打开原始文件读取内容,并写入新文件
with open('iptv.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 创建新文件并写入替换后的内容
with open('iptv.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():
            line = line.replace(old, new)
        new_file.write(line)
print("替换完成,新文件已保存。")

#####################################################################
# 定义要搜索的关键词,从文件中提取包含这个关键词的行,然后添加到另一个文件尾
#keywords = [',', 'tsfile#']
# 打开1.txt文件并读取内容
#with open('网络收集.txt', 'r', encoding='utf-8') as file:
    #lines = file.readlines()
# 创建一个新的列表,只包含包含关键词的行
#filtered_lines = [line for line in lines if any(keyword in line for keyword in keywords)]
# 将这些行追加写入到2.txt文件
#with open('iptv.txt', 'a', encoding='utf-8') as file:
    #file.writelines(filtered_lines)
#print("频道列表文件iptv.txt再次追加写入成功！")
#####################################################################

################################################按网址去除重复行#####
def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[https]?[http]?[P2p]?[mitv]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行,无论是否已被记录,都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))
# 使用方法
remove_duplicates('iptv.txt', 'iptv.txt')



######################################################################################################################
###################################################去除列表中的组播地址,酒店源验证整理
def filter_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    filtered_lines = []
    for line in lines:
        if ('hls' in line and 'm3u' in line) or ('tsfile' in line and 'm3u' in line):  #行中包含m3u的同时还要包含hls或者tsfile
          if 'udp' not in line and 'rtp' not in line and 'BM' not in line and 'B1' not in line and 'B2' not in line and 'B3' not in line and '1TY' not in line:   #  排除组播地址
            filtered_lines.append(line)
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.writelines(filtered_lines)
filter_lines("iptv.txt", "iptv.txt")




#################################################### 对整理好的频道列表测试HTTP连接
def test_connectivity(url, max_attempts=2): #定义测试HTTP连接的次数
    # 尝试连接指定次数    
   for _ in range(max_attempts):  
    try:
        response = requests.head(url, timeout=3)  # 发送HEAD请求,仅支持V4,修改此行数字可定义链接超时##////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #response = requests.get(url, timeout=1)  # 发送get请求,支持V6,修改此行数字可定义链接超时##############################//////////////////////////////////////////////////////////////////////////////////////
        return response.status_code == 200  # 返回True如果状态码为200
    except requests.RequestException:  # 捕获requests引发的异常
        pass  # 发生异常时忽略
   #return False  # 如果所有尝试都失败,返回False
   pass   
# 使用队列来收集结果的函数
def process_line(line, result_queue):
    parts = line.strip().split(",")  # 去除行首尾空白并按逗号分割
    if len(parts) == 2 and parts[1]:  # 确保有URL,并且URL不为空
        channel_name, channel_url = parts  # 分别赋值频道名称和URL
        if test_connectivity(channel_url):  # 测试URL是否有效
            result_queue.put((channel_name, channel_url, "有效"))  # 将结果放入队列
        else:
            result_queue.put((channel_name, channel_url, "无效"))  # 将结果放入队列
    else:
        # 格式不正确的行不放入队列
        pass
# 主函数
def main(source_file_path, output_file_path):
    with open(source_file_path, "r", encoding="utf-8") as source_file:  # 打开源文件
        lines = source_file.readlines()  # 读取所有行s     
    result_queue = queue.Queue()  # 创建队列
    threads = []  # 初始化线程列表
    for line in tqdm(lines, desc="检测进行中"):  # 显示进度条
        thread = threading.Thread(target=process_line, args=(line, result_queue))  # 创建线程
        thread.start()  # 启动线程
        threads.append(thread)  # 将线程加入线程列表
    for thread in threads:  # 等待所有线程完成
        thread.join()
    # 初始化计数器
    valid_count = 0
    invalid_count = 0
    with open(output_file_path, "w", encoding="utf-8") as output_file:  # 打开输出文件
        for _ in range(result_queue.qsize()):  # 使用队列的大小来循环
            item = result_queue.get()  # 获取队列中的项目
            # 只有在队列中存在有效的项目时才写入文件
            if item[0] and item[1]:  # 确保channel_name和channel_url都不为None
                output_file.write(f"{item[0]},{item[1]},{item[2]}\n")  # 写入文件
                if item[2] == "有效":  # 统计有效源数量
                    valid_count += 1
                else:  # 统计无效源数量
                    invalid_count += 1
    print(f"任务完成, 有效源数量: {valid_count}, 无效源数量: {invalid_count}")  # 打印结果
if __name__ == "__main__":
    try:
        source_file_path = "iptv.txt"  # 输入源文件路径
        output_file_path = "酒店源.txt"  # 设置输出文件路径
        main(source_file_path, output_file_path)  # 调用main函数
    except Exception as e:
        print(f"程序发生错误: {e}")  # 打印错误信息
        
#########################################################################提取酒店源中的有效行
def filter_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # 打开文件
        lines = file.readlines()  # 读取所有行
    filtered_lines = []  # 初始化过滤后的行列表
    for line in lines:  # 遍历所有行
        if 'genre' in line or '有效' in line:  # 如果行中包含'genre'或'有效'
            filtered_lines.append(line)  # 将行添加到过滤后的行列表
    return filtered_lines  # 返回过滤后的行列表
def write_filtered_lines(output_file_path, filtered_lines):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:  # 打开输出文件
        output_file.writelines(filtered_lines)  # 写入过滤后的行
if __name__ == "__main__":
    input_file_path = "酒店源.txt"  # 设置输入文件路径
    output_file_path = "酒店源.txt"  # 设置输出文件路径
    filtered_lines = filter_lines(input_file_path)  # 调用filter_lines函数
    write_filtered_lines(output_file_path, filtered_lines)  # 调用write_filtered_lines函数
###################################################################################定义替换规则的字典,对整行内的内容进行替换
replacements = {
    ",有效": "",  # 将",有效"替换为空字符串
    "#genre#,无效": "#genre#",  # 将"#genre#,无效"替换为"#genre#"
}
# 打开原始文件读取内容,并写入新文件
with open('酒店源.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 创建新文件并写入替换后的内容
with open('酒店源.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():  # 遍历替换规则字典
            line = line.replace(old, new)  # 替换行中的内容
        new_file.write(line)  # 写入新文件
print("新文件已保存。")  # 打印完成信息

#对生成的文件进行合并
file_contents = []
file_paths = ['酒店源.txt']  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
    else:                # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file_path} 不存在,跳过")
# 写入合并后的文件
with open('酒店源.txt', "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
#

##########################################################################################简体转繁体
# 创建一个OpenCC对象,指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('酒店源.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()
# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)
# 将转换后的简体字写入txt文件
with open('酒店源.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)
#


import cv2
import time
from tqdm import tqdm
# 初始化酒店源字典
detected_ips = {}
# 存储文件路径
file_path = "酒店源.txt"
output_file_path = "酒店优选.txt"
def get_ip_key(url):
    """从URL中提取IP地址,并构造一个唯一的键"""
    # 找到'//'到第三个'.'之间的字符串
    start = url.find('://') + 3  # '://'.length 是 3
    end = start
    dot_count = 0
    while dot_count < 3:
        end = url.find('.', end)
        if end == -1:  # 如果没有找到第三个'.',就结束
            break
        dot_count += 1
    return url[start:end] if dot_count == 3 else None
# 打开输入文件和输出文件
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 获取总行数用于进度条
total_lines = len(lines)
# 写入通过检测的行到新文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # 使用tqdm显示进度条
    for i, line in tqdm(enumerate(lines), total=total_lines, desc="Processing", unit='line'):
        # 检查是否包含 'genre'
        if 'genre' in line:
            output_file.write(line)
            continue
        # 分割频道名称和URL,并去除空白字符
        parts = line.split(',', 1)
        if len(parts) == 2:
            channel_name, url = parts
            channel_name = channel_name.strip()
            url = url.strip()
            # 构造IP键
            ip_key = get_ip_key(url)
            if ip_key and ip_key in detected_ips:
                # 如果IP键已存在,根据之前的结果决定是否写入新文件
                if detected_ips[ip_key]['status'] == 'ok':
                    output_file.write(line)
            elif ip_key:  # 新IP键,进行检测
                # 进行检测
                cap = cv2.VideoCapture(url)
                start_time = time.time()
                frame_count = 0
                # 尝试捕获5秒内的帧
                while frame_count < 50 and (time.time() - start_time) < 3:#//////////////////////////////////////////////////////////////////////////////////////###########
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame_count += 1
                # 释放资源
                cap.release()
                # 根据捕获的帧数判断状态并记录结果#////////////////////////////////////////////////////////////////////////////////////////////////////////////////###########
                if frame_count >= 50:  #5秒内超过100帧则写入#/////////////////////////////////////////////////////////////////////////////////////////////////////###########
                    detected_ips[ip_key] = {'status': 'ok'}
                    output_file.write(line)  # 写入检测通过的行
                else:
                    detected_ips[ip_key] = {'status': 'fail'}
# 打印酒店源
for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")





####################### 提示用户输入文件名（拖入文件操作）打开用户指定的文件对不规范频道名再次替换
file_path = '酒店优选.txt'
# 检查文件是否存在
if not os.path.isfile(file_path):
    print("文件不存在,请重新输入.")
    exit(1)
with open(file_path, 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
#定义替换规则的字典对频道名替换
replacements = {
    	"-": "",
    	"星河": "TVB星河",
    	"福建东南卫视": "东南卫视",
    	"CCTV风云音乐": "风云音乐",
    	"本港台（珠江）": "TVB星河",
    	"\n都市": "\n河南都市",
    	"": "",
    	"": "",
    	"SD": "",
    	"「": "",
    	"AA": "",
    	"XF": "",
    	"": "",
    	"": "",
    	"湖南金鹰纪实": "金鹰纪实",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	" ": "",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV兵器科技": "兵器科技",
    	"CCTV地理世界": "地理世界",
    	"CCTV风云足球": "风云足球",
    	"CCTV央视台球": "央视台球",
    	"CCTV台球": "台球",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV中视购物": "中视购物",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"IPTV": "",
    	"PLUS": "+",
    	"＋": "+",
    	"(": "",
    	")": "",
    	"CAV": "",
    	"美洲": "",
    	"北美": "",
    	"12M": "",
    	"高清测试CCTV-1": "",
    	"高清测试CCTV-2": "",
    	"高清测试CCTV-7": "",
    	"高清测试CCTV-10": "",
    	"LD": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	"NewTv": "",
    	"NEWTV": "",
    	"NewTV": "",
    	"iHOT": "",
    	"CHC": "",
    	"测试cctv": "CCTV",
    	"凤凰中文台": "凤凰中文",
    	"凤凰资讯台": "凤凰资讯",
    	"(CCTV4K测试）": "CCTV4K",
    	"上海东方卫视": "上海卫视",
    	"东方卫视": "上海卫视",
    	"内蒙卫视": "内蒙古卫视",
    	"福建东南卫视": "东南卫视",
    	"广东南方卫视": "南方卫视",
    	"湖南金鹰卡通": "金鹰卡通",
    	"炫动卡通": "哈哈炫动",
    	"卡酷卡通": "卡酷少儿",
    	"卡酷动画": "卡酷少儿",
    	"BRTVKAKU少儿": "卡酷少儿",
    	"优曼卡通": "优漫卡通",
    	"优曼卡通": "优漫卡通",
    	"嘉佳卡通": "佳嘉卡通",
    	"世界地理": "地理世界",
    	"CCTV世界地理": "地理世界",
    	"BTV北京卫视": "北京卫视",
    	"BTV冬奥纪实": "冬奥纪实",
    	"东奥纪实": "冬奥纪实",
    	"卫视台": "卫视",
    	"湖南电视台": "湖南卫视",
    	"少儿科教": "少儿",
    	"影视剧": "影视",
    	"电视剧": "影视",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}


with open('酒店优选.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除行尾的换行符
        line = line.rstrip('\n')
        # 分割行,获取逗号前的字符串
        parts = line.split(',', 1)
        if len(parts) > 0:
            # 替换逗号前的字符串
            before_comma = parts[0]
            for old, new in replacements.items():
                before_comma = before_comma.replace(old, new)
            # 将替换后的逗号前部分和逗号后部分重新组合成一行,并写入新文件
            new_line = f'{before_comma},{parts[1]}\n' if len(parts) > 1 else f'{before_comma}\n'
            new_file.write(new_line)

#####################################定义替换规则的字典,对整行内的多余标识内容进行替换
replacements = {
    	"（）": "",
        "峨眉电影": "峨眉电影[50FPS]",
        "T[": "T",
        "dx[": "[",
        "g[": "[",
        "P[": "+[",
        "lt[": "[",
        "电信": "",
        "卫视高清": "卫视",
        "SCTV5": "",
        "T,": ",",
        "dx,": ",",
        "g,": ",",
        "TVBTVB": "TVB",
        "": "",
        "": "",
        "": "",
        "": "",
        "": ""
}
# 打开原始文件读取内容,并写入新文件
with open('酒店优选.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 创建新文件并写入替换后的内容
with open('酒店优选.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():
            line = line.replace(old, new)
        new_file.write(line)
print("替换完成,新文件已保存。")


###############################################################################文本排序
# 打开原始文件读取内容,并写入新文件
with open('酒店优选.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 定义一个函数,用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')
# 对列表中的行进行排序
# 按照第一个数字的大小排列,如果不存在数字则按中文拼音排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))
# 将排序后的行写入新的utf-8编码的文本文件,文件名基于原文件名
output_file_path = "sorted_" + os.path.basename(file_path)
# 写入新文件
with open('酒店源.txt', "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)
print(f"文件已排序并保存为新文件")
print("\n\n\n\n\n\n")


########################################################################定义关键词分割规则,分类提取
def check_and_write_file(input_file, output_file, keywords):
    # 使用 split(', ') 而不是 split(',') 来分割关键词
    keywords_list = keywords.split(', ')
    first_keyword = keywords_list[0]  # 获取第一个关键词作为头部信息
    pattern = '|'.join(re.escape(keyword) for keyword in keywords_list)
    extracted_lines = False
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(f'{first_keyword},#genre#\n')  # 使用第一个关键词作为头部信息
        for line in lines:
            if 'genre' not in line and 'epg' not in line:
                if re.search(pattern, line):
                    out_file.write(line)
                    extracted_lines = True
    # 如果没有提取到任何关键词,则不保留输出文件
    if not extracted_lines:
        os.remove(output_file)  # 删除空的输出文件
        print(f"未提取到关键词,{output_file} 已被删除。")
    else:
        print(f"文件已提取关键词并保存为: {output_file}")
# 按类别提取关键词并写入文件
check_and_write_file('酒店源.txt',  'a0.txt',  keywords="央视频道, 8K, 4K, 4k")
check_and_write_file('酒店源.txt',  'a.txt',  keywords="央视频道, CCTV, 风云, 女性时尚, 地理世界, 音乐")
check_and_write_file('酒店源.txt',  'a1.txt',  keywords="央视频道")
check_and_write_file('酒店源.txt',  'b.txt',  keywords="卫视频道, 卫视, 凤凰, 星空")
check_and_write_file('酒店源.txt',  'c.txt',  keywords="影视频道, 剧, 选, 影")
check_and_write_file('酒店源.txt',  'e.txt',  keywords="港澳频道, shuma, TVB, 珠江台, 澳门, 龙华, 广场舞, 动物杂技, 民视, 中视, 华视, AXN, MOMO, 采昌, 耀才, 靖天, 镜新闻, 靖洋, 莲花, 年代, 爱尔达, 好莱坞, 华丽, 非凡, 公视, \
寰宇, 无线, EVEN, MoMo, 爆谷, 面包, momo, 唐人, 中华小, 三立, 37.27, 猪哥亮, 综艺, Movie, 八大, 中天, 中视, 东森, 凤凰, 天映, 美亚, 环球, 翡翠, ZIPP, 大爱, 大愛, 明珠, jdshipin, AMC, 龙祥, 台视, 1905, 纬来, 神话, 经典都市, 视界, \
番薯, 私人, 酒店, TVB, 凤凰, 半岛, 星光视界, 大愛, 新加坡, 星河, 明珠, 环球, 翡翠台")
#check_and_write_file('酒店源.txt',  'f.txt',  keywords="省市频道, 湖北, 武汉, 河北, 广东, 河南, 陕西, 四川, 湖南, 广西, 山西, 石家庄, 南宁, 汕头, 揭阳, 普宁, 福建, 辽宁")
#check_and_write_file('酒店源.txt',  'o1.txt',  keywords="其他频道, 新闻, 综合, 文艺, 电视, 公共, 科教, 教育, 民生, 轮播, 套, 法制, 文化, 经济, 生活")
check_and_write_file('酒店源.txt',  'o.txt',  keywords="其他频道, , ")
#
#对生成的文件进行合并
file_contents = []
file_paths = ["e.txt", "a0.txt", "a.txt", "a1.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "f.txt", "o1.txt", "o.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
    else:                # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file_path} 不存在,跳过")
# 写入合并后的文件
with open("去重.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
#
##################################################################### 打开文档并读取所有行 ,对提取后重复的频道去重
with open('去重.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
# 使用列表来存储唯一的行的顺序 
 unique_lines = [] 
 seen_lines = set() 
# 遍历每一行,如果是新的就加入unique_lines 
for line in lines:
 if line not in seen_lines:
  unique_lines.append(line)
  seen_lines.add(line)
# 将唯一的行写入新的文档 
with open('酒店优选.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)

import datetime
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
current_time = now.strftime("%Y-%m-%d %H:%M")
# 打开文本文件并将时间添加到开头
file_path = "酒店优选.txt"
with open(file_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(f'#鉴于酒店源的不实用性,本次最后一次更新。如果需要的话,请fork以后自行启用工作流程\n')
    f.write(f'最后更新时间{current_time},#genre#\n')
    f.write(f'虚情的爱,https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n{content}')


#任务结束,删除不必要的过程文件
files_to_remove = ['去重.txt', "2.txt", "iptv.txt", "e.txt", "a0.txt", "a.txt", "a1.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "f.txt", "o1.txt", "o.txt", "酒店源.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file} 不存在,跳过删除。")
print("任务运行完毕,酒店源频道列表可查看文件夹内txt文件！")
