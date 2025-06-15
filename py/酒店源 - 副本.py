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
# 搜素关键词："iptv/live/zh_cn.js" && country="CN" && region="Hunan" && city="changsha"   ZHGXTV/Public/json/live_interface.txt
# 搜素关键词："ZHGXTV" && country="CN" && region="Hunan" && city="changsha"              iptv/live/1000.json?key=txiptv
#"isShowLoginJs"智能KUTV管理
import platform
import subprocess
import subprocess

# 读取文件内容
with open('ip.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 匹配IP:Port或域名:Port，保留可能的地域标识符
pattern = r'([\w\.-]+:\d+(?:\$[^$\n]+)?)'
matches = set()
for line in lines:
    if match := re.search(pattern, line):
        matches.add(match.group(1))

# 提取 IP 或端口部分并去重
extracted_entries = set()
print(f"需要提取的地址总数: {len(matches)}")
for i, full_entry in enumerate(matches, 1):
    # 分离地址部分和地域标识符
    if '$' in full_entry:
        address_part, region = full_entry.split('$', 1)
    else:
        address_part, region = full_entry, ""
  
    # 提取 IP 或端口部分
    host_and_port = address_part.split(':', 1)
    host = host_and_port[0]
    port = host_and_port[1] if len(host_and_port) > 1 else ""
  
    region_info = f" [{region}]" if region else ""
  
    # 只保留 IP 或端口部分，并可选地包含地域标识符
    extracted_entry = f"{host}:{port}{region_info}"
  
    # 加入去重功能，只保留唯一的条目
    if extracted_entry not in extracted_entries:
        print(f"({i}/{len(matches)}) {extracted_entry} ", end='')
        extracted_entries.add(extracted_entry)

# 写回文件（包含完整的地域标识符）
with open('ip.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(sorted(extracted_entries)))  # 排序以便于阅读

print(f"提取完成，去重后的唯一地址数: {len(extracted_entries)}")


	
import requests
import re
import concurrent.futures


# 从 IPV.txt 文件中读取 IP 地址和端口
def read_ips_from_file():
    ips_with_ports = []
    try:
        with open('ip.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        ip = parts[0]
                        port = ':' + parts[1]
                        ips_with_ports.append((ip, port))
    except FileNotFoundError:
        print("IPV.txt 文件未找到。")
    return ips_with_ports


urls = []

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/ZHGXTV/Public/json/live_interface.txt"
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

# 从 ip.txt 文件中读取 IP 和端口
with open('ip.txt', 'r', encoding='utf-8') as file:
    ip_ports = file.readlines()

# 将读取到的 IP 和端口添加到 urls 列表中
for ip_port in ip_ports:
    ip_port = ip_port.strip()
    if ip_port:
        urls.append(f"http://{ip_port}")  # 添加协议头

# 去重得到唯一的 URL 列表
urls = list(set(urls))

valid_urls = []
# 多线程获取可用 URL
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for url in urls:
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

print(f"找到 {len(valid_urls)} 个有效URL")
print(f"{valid_urls}")
results = []
# 遍历网址列表,获取JSON文件并解析
    # 遍历网址列表,获取JSON文件并解析
for url in valid_urls:
        try:
            json_url = f"{url}"
            response = requests.get(json_url, timeout=8)
            json_data = response.content.decode('utf-8')
            try:
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
                                # 替换播放列表中的 IP 地址为当前 IP 和端口
                                current_ip, current_port = url_data[2].split(':')
                                urld = f"{urls[0]}//{current_ip}:{current_port}/{urls[3]}"
                            else:
                                urld = f"{urls}"
                            print(f"{name},{urld}")  #关闭频道名称和频道地址打印,缩短运行时间
                            if name and urld:
                                name = name.replace("高清电影", "影迷电影")
                                name = name.replace("中央", "CCTV")
                                name = name.replace("高清", "")
                                name = name.replace("HD", "")
                                name = name.replace("标清", "")
                                name = name.replace("超高", "")
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
                                #urld = urld.replace("index.m3u8", "index.m3u8?$智慧光迅听说名字越长越好看")
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
        print(result)  # 关闭频道名称和频道地址打印,缩短运行时间
print("频道列表文件iptv.txt获取完成！")
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
import requests
import re
import concurrent.futures
from urllib.parse import urlparse

# 定义一个空的 URL 列表，用于存储从 ip.txt 文件中读取的 IP 和端口
urls = []

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

# 从 ip.txt 文件中读取 IP 和端口
with open('ip.txt', 'r', encoding='utf-8') as file:
    ip_ports = file.readlines()

# 将读取到的 IP 和端口添加到 urls 列表中
for ip_port in ip_ports:
    ip_port = ip_port.strip()
    if ip_port:
        urls.append(f"http://{ip_port}")  # 添加协议头

# 去重得到唯一的 URL 列表
urls = list(set(urls))

valid_urls = []
# 多线程获取可用 URL
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for url in urls:
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

print(f"找到 {len(valid_urls)} 个有效URL")

results = []
# 遍历网址列表, 获取 JSON 文件并解析
for url in valid_urls:
    try:
        ip_start_index = url.find("//") + 2
        ip_dot_start = url.find(".", ip_start_index) + 1
        ip_index_second = url.find("/", ip_dot_start)
        base_url = url[:ip_start_index]
        ip_address = url[ip_start_index:ip_index_second]
        url_x = f"{base_url}{ip_address}"
        json_url = url
        
        response = requests.get(json_url, timeout=3)
        json_data = response.json()
        
        # 解析 JSON 文件，获取频道信息
        if 'data' in json_data and isinstance(json_data['data'], list):
            for item in json_data['data']:
                if isinstance(item, dict):
                    name = item.get('name', '')
                    urlx = item.get('url', '')
                    
                    # 跳过包含 'udp' 或 'rtp' 的 url
                    if 'udp' in urlx or 'rtp' in urlx:
                        continue
                    
                    # 构建最终URL
                    if urlx.startswith('http'):
                        urld = urlx
                    else:
                        urld = f"{url_x}{urlx}"
                    print(f"{name},{urld}")
                    
                    # 频道名称清理
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
                    name = name.replace("湖南电视台", "湖南卫视")
                    name = name.replace("少儿科教", "少儿")
                    name = name.replace("TV星河2）", "星河")
                    name = name.replace("影视剧", "影视")
                    name = name.replace("电视剧", "影视")
                    name = name.replace("奥运匹克", "")
                    name = name.replace("TVBTVB", "TVB")
                    name = name.replace("星空卫视", "动物杂技")
                    
                    results.append(f"{name},{urld}")
        else:
            print(f"URL {url} 返回的JSON格式不符合预期")
            
    except Exception as e:
        print(f"处理URL {url} 时出错: {e}")

# 将结果写入文件
with open("iptv.txt", 'a', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")

print("频道列表文件iptv.txt写入成功！")

# 去重函数
def remove_duplicates(input_file, output_file):
    seen_urls = set()
    output_lines = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"去重前的行数：{len(lines)}")
        
        for line in lines:
            urls = re.findall(r'https?://[^\s,]+', line)
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"去重后的行数：{len(output_lines)}")

# 过滤组播地址函数
def filter_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    filtered_lines = []
    for line in lines:
        if ('/' in line or 'tsfile' in line) and \
           not any(word in line for word in ['udp', 'rtp', 'BM', 'B1', 'B2', 'B3', '1TY']):
            filtered_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as output:
        output.writelines(filtered_lines)

# 执行去重和过滤
remove_duplicates('iptv.txt', 'iptv_temp.txt')
filter_lines('iptv_temp.txt', 'iptv.txt')

print("去重和过滤完成！最终结果保存在 iptv.txt")

os.remove("iptv_temp.txt")
input("按任意键退出...")