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
import requests
from tqdm import tqdm
import threading
import re

print("本程序只检测地址中带m3u/php/live的，其它的无论是否有效一律不检测不输出\n")
print("如果你确定不含这种关键词的地址是有效源请预先备份\n")

# 测试HTTP连接
def test_connectivity(url, max_attempts=2):
    #if "udp" in url or "rtp" in url:
        #print("\n组播地址: 跳过检测")
        #return False

    video_formats = ["m3u", "1", "/", "rtsp"]
    if not any(re.search(keyword, url, re.I) for keyword in video_formats):
        print("\n特殊网址: 跳过检测")
        return False

    for _ in range(max_attempts):
        try:
            response = requests.get(url, timeout=0.3)
            return response.status_code == 200
        except requests.RequestException:
            pass

    return False

# 处理每一行的函数
def process_line(line, output_file, valid_count, invalid_count):
    parts = line.strip().split(",")
    if len(parts) == 2:
        channel_name, channel_url = parts
        if "genre" in line.lower():
            with threading.Lock():
                output_file.write("\n" +line)  # 直接写入原始行
        elif test_connectivity(channel_url):
            with threading.Lock():
                output_file.write(f"{channel_name},{channel_url}\n")
                valid_count[0] += 1
        else:
            with threading.Lock():
                invalid_count[0] += 1
    else:
        with threading.Lock():
            invalid_count[0] += 1

# 主函数
def main(source_file_path, output_file_path):
    with open(source_file_path, "r", encoding="utf-8") as source_file:
        lines = source_file.readlines()

    valid_count = [0]
    invalid_count = [0]

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        threads = []
        for line in tqdm(lines, desc="地址有效"):
            thread = threading.Thread(target=process_line, args=(line, output_file, valid_count, invalid_count))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    print(f"任务完成,有效源数量: {valid_count[0]}, 无效源数量: {invalid_count[0]}")
if __name__ == "__main__":
    try:
        source_file_path = "iptv.txt"
        output_file_path = "酒店源.txt"
        main(source_file_path, output_file_path)
    except Exception as e:
        print(f"程序发生错误: {e}")
print("本程序只检测地址中带m3u/php的，其它的无论是否有效一律不检测不输出\n\n本程序只检测地址有效性，不检测是否有视频流返回\n")
print("如果你确定不含这种关键词的地址是有效源请预先备份\n")
print("注意！！！直播源名称不支持特殊字符！！！！！！！\n")
import cv2
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests
from tqdm import tqdm
import re
from opencc import OpenCC
#a = input('请动动你发财的小手吧\n\n拖入utf-8直播源文件回车后运行:')
with open('酒店源.txt', 'r', encoding="utf-8") as f:#拖入文件操作


 def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open('酒店源.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[http?][https?][rtsp?][rtmp?]://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open('去重.txt', 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))

# 使用方法
remove_duplicates('1.txt', '去重.txt')



# 导入fileinput模块
import fileinput

# 定义替换规则的字典
replacements = {
    	"CCTV-1高清测试": "",
    	"CCTV-2高清测试": "",
    	"CCTV-7高清测试": "",
    	"CCTV-10高清测试": "",
    	"中央": "CCTV",
    	"高清": "",
    	"HD": "",
    	"标清": "",
    	"2.5M1080HEVC": "",
    	"[720*576]": "",
    	"[720*480]": "",
    	"[720*576]": "",
    	"[3840*2160]": "",
    	"[1024*576]": "",
    	"[1080p]": "",
    	"[2160p]": "",
    	"720p": "",
    	"-": "",
    	"超清": "",
    	"4k": "4K",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	"[1920x1080]": "",
    	"[1280x720]": "",
    	" ": "",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"熊猫影院": "熊猫电影",
    	"熊猫爱生活": "熊猫生活",
    	"爱宠宠物": "宠物生活",
    	"[ipv6]": "",
    	"专区": "",
    	"卫视超": "卫视",
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
    	"_4M1080HEVC": "",
    	"_2.5M1080HEVC": "",
    	"SD": "",
    	"[1280*720]": "",
    	"LD": "",
    	"[1920*1080]": "",
    	"[1280*720]": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	"测试cctv": "CCTV",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"CCTV4国际": "CCTV4",
    	"CCTV4中文国际": "CCTV4",
    	"CCTV4欧洲": "CCTV4",
    	"CCTV5体育": "CCTV5",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV6电影": "CCTV6",
    	"CCTV7军事": "CCTV7",
    	"CCTV7军农": "CCTV7",
    	"CCTV7农业": "CCTV7",
    	"CCTV7国防军事": "CCTV7",
    	"CCTV8电视剧": "CCTV8",
    	"CCTV8影视": "CCTV8",
    	"CCTV8纪录": "CCTV9",
    	"CCTV9记录": "CCTV9",
    	"CCTV9纪录": "CCTV9",
    	"CCTV10科教": "CCTV10",
    	"CCTV11戏曲": "CCTV11",
    	"CCTV12社会与法": "CCTV12",
    	"CCTV13新闻": "CCTV13",
    	"CCTV新闻": "CCTV13",
    	"CCTV14少儿": "CCTV14",
    	"央视14少儿": "CCTV14",
    	"CCTV少儿超": "CCTV14",
    	"CCTV15音乐": "CCTV15",
    	"CCTV音乐": "CCTV15",
    	"CCTV16奥林匹克": "CCTV16",
    	"CCTV17农业农村": "CCTV17",
    	"CCTV17军农": "CCTV17",
    	"CCTV17农业": "CCTV17",
    	"CCTV5+体育赛视": "CCTV5+",
    	"CCTV5+赛视": "CCTV5+",
    	"CCTV5+体育赛事": "CCTV5+",
    	"CCTV5+赛事": "CCTV5+",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV5赛事": "CCTV5+",
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
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10",
    	"_": ""
}

# 打开原始文件读取内容，并写入新文件
with open('去重.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建新文件并写入替换后的内容
with open('去重.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        parts = line.strip().split(',', 1)  # 以英文逗号分割，最多分割一次，获取前面部分和后面部分（如果有）
        if len(parts) > 0:
            first_part = parts[0]
            for old, new in replacements.items():
                first_part = first_part.replace(old, new)
            new_line = first_part
            if len(parts) > 1:
                new_line += "," + parts[1]
            new_file.write(new_line + "\n")
        else:
            new_file.write(line)

print("替换完成，新文件已保存。")


################简体转繁体
# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('去重.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入txt文件
with open('去重.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)







from pypinyin import lazy_pinyin
import re
import os
#a = input('FileName(DragHere):')
#with open(a, 'r', encoding="utf-8") as f:#拖入文件操作

# 打开一个utf-8编码的文本文件
with open("去重.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))

# 将排序后的行写入新的utf-8编码的文本文件
with open("2.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)



###############################        
with open('2.txt', 'r', encoding='utf-8') as file:
#从整理好的文本中按类别进行特定关键词提取#############################################################################################
 keywords = "CCTV, 风云音乐, 女性, 地理, 风云剧场, 怀旧剧场, 第一剧场, 家庭, 影迷, 高清电影, 动作电影, CHC, 世界地理, 兵器, \
             央视台球, 第一剧场, 风云足球, 高尔夫, 动作电影, 家庭影院, 影迷电影, 世界地理, 4K, 8K"  # 需要提取的关键字列表
 pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:    #####定义临时文件名
    a.write('央视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         a.write(line)  # 将该行写入输出文件 

################
keywords = "卫视, 星空, 凤凰"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:    #####定义临时文件名
    b.write('\n卫视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line and 'epg' not in line:       
        if re.search(pattern, line):  # 如果行中有任意关键字
         b.write(line)  # 将该行写入输出文件

         
################
keywords = "爱情喜剧, 爱喜喜剧, 惊嫊悬疑, 东北热剧, 重温经典, 都市剧场, 海外剧场, 欢笑剧场, NewT, 重温经典, 军事评论, 农业致富, 哒啵赛事, 怡伴健康, 明星大片, 武博世界, HOT, 中国功夫, 军旅, 炫舞未来, 精品体育, 精品萌宠, 精品记录, 超级体育, 超级, 金牌, \
            东北热剧, 中国功夫, 军旅剧场, 古装剧场, 家庭剧场, 惊悚悬疑, 欢乐剧场, 潮妈辣婆, 爱情喜剧, 精品大剧, 超级影视, 超级电影, 黑莓动画, 黑莓电影, \
            海外剧场, 精彩影视, 七彩戏剧, 东方影视, 无名影视, 潮婆辣妈, 超级剧, 热播精选, 武术世界, 求索动物, 求索, 求索科学, 求索记录, 爱谍战, 爱动漫, 爱科幻, 爱科幻, 爱科学, 爱浪漫, 爱历史, 爱旅行, 爱奇谈, 爱赛车, 爱体育, 爱玩具, \
            爱玩具, 爱喜剧, 爱悬疑, 爱幼教, 爱院线, 精品纪录" # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n影视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
       if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'epg' not in line and '江苏' not in line and '浙江' not in line and '安徽' not in line and '上虞' not in line and '黑龙江' not in line and '四川' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件

############
keywords = "amc, 影视, TVB, 三立, CNA, FOX, RTHK, Movie, 八大, 中天, 中视, 东森, 凤凰, 天映, 美亚, 环球, 翡翠, 亚洲, 大爱, 大愛, 龙华, 寰宇, 澳门, \
            明珠, 半岛, AMC, 龙祥, 台视, 1905, 纬来, 神话, 经典都市, 视界, 番薯, 私人, 酒店, TVB, 凤凰, 半岛, 星光视界, 番薯, 大愛, 新加坡, 星河, 明珠, 环球, 翡翠台"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
with open('2.txt', 'r', encoding='utf-8') as file, open('d.txt', 'w', encoding='utf-8') as d:    #####定义临时文件名
    d.write('\n港澳频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and '哈' not in line and '超级' not in line and '黑龙江' not in line and '江苏' not in line and '浙江' not in line and '四川' not in line and 'genre' not in line and 'epg' not in line:
          if re.search(pattern, line): 
              d.write(line)  # 将该行写入输出文件

################
keywords = "江苏, 常州, 淮安, 连云港, 南京, 南通, 高邮, 苏州, 宿迁, 泰州, 无锡, 徐州, 盐城, 扬州, 镇江"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('e.txt', 'w', encoding='utf-8') as e:    #####定义临时文件名
    e.write('\n江苏频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:   
        if re.search(pattern, line):  # 如果行中有任意关键字
         e.write(line)  # 将该行写入输出文件

################
keywords = "江西, 抚州, 赣州, 吉安, 景德镇, 九江, 南昌, 萍乡, 上饶, 新余, 宜春, 鹰潭"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('e1.txt', 'w', encoding='utf-8') as e1:    #####定义临时文件名
    e1.write('\n江西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:   
        if re.search(pattern, line):  # 如果行中有任意关键字
         e1.write(line)  # 将该行写入输出文件

         
################
keywords = "河北, 石家庄, 承德, 丰宁, 临漳, 井陉, 井陉矿区, 保定, 元氏, 兴隆, 内丘, 南宫, 吴桥, 唐县, 唐山, 安平, 定州, 大厂, 张家口, 徐水, 成安, \
            承德, 故城, 康保, 廊坊, 晋州, 景县, 武安, 枣强, 柏乡, 涉县, 涞水, 涞源, 涿州, 深州, 深泽, 清河, 秦皇岛, 衡水, 遵化, 邢台, 邯郸, \
            邱县, 隆化, 雄县, 阜平, 高碑店, 高邑, 魏县, 黄骅, 饶阳, 赵县, 睛彩河北, 滦南, 玉田, 崇礼, 平泉, 容城, 文安, 三河, 清河" # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f.txt', 'w', encoding='utf-8') as f:    #####定义临时文件名
    f.write('\n河北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f.write(line)  # 将该行写入输出文件




################f1
keywords = "河南, 焦作, 开封, 卢氏, 洛阳, 孟津, 安阳, 渑池, 南阳, 内黄, 平顶山, 淇县, 杞县, 汝阳, 三门峡, 卫辉, 淅川, \
            新密, 新乡, 信阳, 新郑, 延津, 叶县, 义马, 永城, 禹州, 原阳, 镇平, 郑州, 周口"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f1.txt', 'w', encoding='utf-8') as f1:    #####定义临时文件名
    f1.write('\n河南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f1.write(line)  # 将该行写入输出文件




         
################
keywords = "浙江, 杭州, 宁波, 丽水, 上虞, 舟山, 新密, 衢州, 嘉兴, 绍兴, 温州, 湖州, 永嘉, 诸暨, 钱江, 松阳, 苍南, 遂昌, 青田, 龙泉, 余杭, 新昌, 杭州, 余杭, 丽水, 龙泉, \
            青田, 松阳, 遂昌, 宁波, 余姚, 上虞, 新商都, 绍兴, 温州, 永嘉, 诸暨, 钱江, 金华, 国际, 苍南"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('g.txt', 'w', encoding='utf-8') as g:    #####定义临时文件名
    g.write('\n浙江频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         g.write(line)  # 将该行写入输出文件



################
keywords = "湖北, 武汉, 松滋, 十堰, 咸宁, 远安, 黄石, 荆州, 当阳, 恩施, 五峰, 来凤, 枝江, 黄冈, 随州, 荆门, 秭归, 孝感, \
            鄂州, 湖北, 五峰, 来凤, 枝江, 随州, 荆门, 秭归, 孝感, 鄂州, 武汉, 松滋, 十堰, 咸宁, 黄石, 垄上, 荆州, 当阳, 恩施, 宜都" # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('h.txt', 'w', encoding='utf-8') as h:    #####定义临时文件名
    h.write('\n湖北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         h.write(line)  # 将该行写入输出文件




################
keywords = "湖南, 长沙, 常德, 郴州, 衡阳, 怀化, 吉首, 娄底, 邵阳, 湘潭, 益阳, 永州, 岳阳, 张家界, 株洲" # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('h1.txt', 'w', encoding='utf-8') as h1:    #####定义临时文件名
    h1.write('\n湖南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         h1.write(line)  # 将该行写入输出文件







################
keywords = "陕西, 安康, 宝鸡, 汉中, 商洛, 铜川, 渭南, 西安, 咸阳, 延安, 榆林"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('i.txt', 'w', encoding='utf-8') as i:    #####定义临时文件名
    i.write('\n陕西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         i.write(line)  # 将该行写入输出文件








################
keywords = "黑龙江, 大庆, 大兴安岭, 哈尔滨, 鹤岗, 黑河, 鸡西, 佳木斯, 牡丹江, 七台河, 齐齐哈尔, 双鸭山, 绥化, 伊春"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('j.txt', 'w', encoding='utf-8') as j:    #####定义临时文件名
    j.write('\n黑龙江频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         j.write(line)  # 将该行写入输出文件











################
keywords = "广东, 潮州, 东莞, 佛山, 广州, 河源, 惠州, 江门, 揭阳, 茂名, 梅州, 清远, 汕头, 汕尾, 韶关, 深圳, 阳江, 云浮, 湛江, \
            肇庆, 中山, 珠海"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('k.txt', 'w', encoding='utf-8') as k:    #####定义临时文件名
    k.write('\n广东频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         k.write(line)  # 将该行写入输出文件









################
keywords = "广西, 百色, 北海, 防城港, 桂林, 河池, 柳州, 南宁, 钦州, 梧州, 玉林"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('k1.txt', 'w', encoding='utf-8') as k1:    #####定义临时文件名
    k1.write('\n广西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         k1.write(line)  # 将该行写入输出文件











################
keywords = "云南, 版纳, 保山, 楚雄, 大理, 德宏, 迪庆, 红河, 昆明, 丽江, 临沧, 怒江, 曲靖, 思茅, 文山, 玉溪, 昭通, 西双版纳, 贵州, \
            安顺, 毕节, 都匀, 贵阳, 凯里, 六盘水, 铜仁, 兴义, 遵义"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('m.txt', 'w', encoding='utf-8') as m:    #####定义临时文件名
    m.write('\n云贵频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         m.write(line)  # 将该行写入输出文件


################
keywords = "四川, 阿坝, 巴中, 成都, 达州, 德阳, 甘孜, 广安, 广元, 乐山, 凉山, 泸州, 眉山, 绵阳, 内江, 南充, 攀枝花, 遂宁, 雅安, \
            宜宾, 资阳, 自贡, 上海, 东方, 财经, 五星, 四川, 黑水, 金川, 乐至, 双流, 万源, 马尔康, 泸县, 文山, 什邡, 西青, 长宁, 达州, 红河"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('n.txt', 'w', encoding='utf-8') as n:    #####定义临时文件名
    n.write('\n四川上海,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         n.write(line)  # 将该行写入输出文件



################
keywords = "安徽, 安庆, 蚌埠, 亳州, 巢湖, 池州, 滁州, 阜阳, 合肥, 淮北, 淮南, 黄山, 六安, 马鞍山, 宿州, 铜陵, 芜湖, 宣城, 山东, 滨州, \
            德州, 东营, 菏泽, 济南, 济宁, 莱芜, 聊城, 临沂, 青岛, 日照, 泰安, 威海, 潍坊, 烟台, 枣庄, 淄博, 山西, 长治, 大同, 晋城, \
            晋中, 临汾, 吕梁, 朔州, 太原, 忻州, 阳泉, 运城"  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('o.txt', 'w', encoding='utf-8') as o:    #####定义临时文件名
    o.write('\n安徽山东,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         o.write(line)  # 将该行写入输出文件
                  
################         
                  
                
################
keywords = ","  # 需要提取的关键字列表
pattern = '|'.join(re.escape(keyword) for keyword in keywords.split(', '))  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('l.txt', 'w', encoding='utf-8') as l:    #####定义临时文件名
    l.write('\n其他频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         l.write(line)  # 将该行写入输出文件









            

############
file_contents = []
file_paths = ["a.txt", "b.txt", "d.txt", "c.txt", "e.txt", "e1.txt", "f.txt", "f1.txt", "g.txt", "h.txt", "i.txt", "k.txt", "h1.txt",  "k1.txt",  "j.txt",  "m.txt",  \
              "n.txt",  "o.txt", "l.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    try:
        file_size = os.path.getsize(file_path)
        if file_size >= 500:
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()
                file_contents.append(content)
        else:
            print(f"文件 {file_path} 小于500字节，已忽略该文件。")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，已忽略该文件。")
# 写入合并后的文件
with open("去重.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))


# 打开文档并读取所有行
with open('去重.txt', 'r', encoding="utf-8") as file:
    lines = file.readlines()

# 使用列表来存储唯一的行的顺序
unique_lines = []
seen_lines = set()

# 遍历每一行，如果是新的就加入unique_lines
for line in lines:
    if line not in seen_lines:
        unique_lines.append(line)
        seen_lines.add(line)

# 计算去重前的行数和去重后的行数
original_count = len(lines)
unique_count = len(unique_lines)

# 将唯一的行写入新的文档
with open('酒店源.txt', 'w', encoding="utf-8") as file:
    file.writelines(unique_lines)

# 输出去重前后的行数
print(f"去重前的行数：{original_count}")
print(f"去重后的行数：{unique_count}")





os.remove("a.txt")
os.remove("b.txt")
os.remove("c.txt")
os.remove("d.txt")
os.remove("2.txt")
os.remove("e.txt")
os.remove("e1.txt")
os.remove("f.txt")
os.remove("f1.txt")
os.remove("g.txt")
os.remove("h.txt")
os.remove("h1.txt")
os.remove("k1.txt")
os.remove("i.txt")
os.remove("j.txt")
os.remove("k.txt")
os.remove("m.txt")
os.remove("n.txt")
os.remove("o.txt")
os.remove("l.txt")
os.remove("去重.txt")
os.remove("iptv.txt")
os.remove("iptv_temp.txt")
