#本程序主体构造如下
#搜素有效IP并生成文件追加写入到相应列表文件后去重
#检测组播列表所有文件中IP有效性
#合并整理自用直播源，与组播无关
#合并所有组播文件并过滤严重掉帧的视频以保证流畅性
#提取检测后的频道进行分类输出优选组播源
#提取优选组播源中分类追加到自用直播源
#后续整理
#没了！！！！！！！！！！！！
import time
from datetime import datetime, timedelta  # 确保 timedelta 被导入
import concurrent.futures
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
# -*- coding: utf-8 -*-
import random
from fake_useragent import UserAgent  # 需要先安装：pip install fake-useragent

# 创建输出目录
os.makedirs('playlist', exist_ok=True)

# 配置参数
DELAY_RANGE = (3, 6)     # 随机延迟时间范围（秒）
MAX_RETRIES = 3          # 最大重试次数
REQUEST_TIMEOUT = 10     # 请求超时时间（秒）

def get_random_header():
    """生成随机请求头"""
    return {
        'User-Agent': UserAgent().random,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://fofa.info/'
    }

def safe_request(url):
    """带重试机制的请求函数"""
    for attempt in range(MAX_RETRIES):
        try:
            # 随机延迟防止被封
            time.sleep(random.uniform(*DELAY_RANGE))

            response = requests.get(
                url,
                headers=get_random_header(),
                timeout=REQUEST_TIMEOUT
            )

            # 检查HTTP状态码
            if response.status_code == 429:
                wait_time = 30  # 遇到反爬等待30秒
                print(f"遇到反爬机制，等待{wait_time}秒后重试")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"请求失败（第{attempt+1}次重试）: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                raise

def validate_video(url, mcast):
    """验证视频流有效性"""
    video_url = f"{url}/rtp/{mcast}"
    print(f"正在验证: {video_url}")

    try:
        # 发送请求，尝试下载 1 千字节的数据
        response = requests.get(video_url, headers=get_random_header(), timeout=REQUEST_TIMEOUT, stream=True)
        response.raise_for_status()

        content_length = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                content_length += len(chunk)
                if content_length >= 64:
                    break
        return content_length >= 16

    except Exception as e:
        print(f"视频验证异常: {str(e)}")
        return False

def main():
    # 获取需要处理的文件列表
    files = [f.split('.')[0] for f in os.listdir('rtp') if f.endswith('.txt')]
    print(f"待处理频道列表: {files}")

    for filename in files:
        province_isp = filename.split('_')
        if len(province_isp) != 2:
            continue

        province, isp = province_isp
        print(f"\n正在处理: {province}{isp}")

        # 读取组播地址
        try:
            with open(f'rtp/{filename}.txt', 'r', encoding='utf-8') as f:
                mcast = f.readline().split('rtp://')[1].split()[0].strip()
        except Exception as e:
            print(f"文件读取失败: {str(e)}")
            continue

        # 构造搜索请求
        search_txt = f'"udpxy" && country="CN" && region="{province}" && is_domain=true'
        encoded_query = base64.b64encode(search_txt.encode()).decode()
        search_url = f'https://fofa.info/result?qbase64={encoded_query}'

        # 执行搜索
        try:
            html = safe_request(search_url)
        except Exception as e:
            print(f"搜索失败: {str(e)}")
            continue

        # 解析搜索结果，修改正则表达式以匹配IP和域名
        soup = BeautifulSoup(html, 'html.parser')
        pattern = re.compile(r"http://(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\w[\w.-]*\w):\d+")
        found_urls = set(pattern.findall(html))
        print(f"找到{len(found_urls)}个有效地址")

        # 验证地址有效性
        valid_urls = [url for url in found_urls if validate_video(url, mcast)]
        print(f"验证通过{len(valid_urls)}个有效地址")

        # 生成播放列表
        if valid_urls:
            output_file = f'playlist/{province}{isp}.txt'
            with open(f'rtp/{filename}.txt', 'r') as src, open(output_file, 'a') as dst:
                original_content = src.read()
                for url in valid_urls:
                    modified = original_content.replace('rtp://', f'{url}/rtp/')
                    dst.write(modified + '\n')
            print(f"已生成播放列表: {output_file}")

if __name__ == '__main__':
    main()


print('对playlist文件夹里面的所有txt文件进行去重处理')
def remove_duplicates_keep_order(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            lines = set()
            unique_lines = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line not in lines:
                        unique_lines.append(line)
                        lines.add(line)
            # 将保持顺序的去重后的内容写回原文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(unique_lines)
# 使用示例
folder_path = 'playlist'  # 替换为你的文件夹路径
remove_duplicates_keep_order(folder_path)
print('文件去重完成！移除存储的旧文件！')
import os
import time
from tqdm import tqdm
import sys
import requests  # 新增requests库

# 初始化字典以存储IP检测结果
detected_ips = {}

def get_ip_key(url):
    """从URL中提取IP地址或域名，并构造一个唯一的键"""
    start = url.find('://') + 3
    end = url.find('/', start)
    if end == -1:
        end = len(url)
    return url[start:end].strip()

folder_path = 'playlist'

if not os.path.isdir(folder_path):
    print("指定的文件夹不存在。")
    sys.exit()

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as output_file:
            for line in tqdm(lines, total=len(lines), desc=f"Processing {filename}"):
                parts = line.split(',', 1)
                if len(parts) >= 2:
                    channel_name, url = parts
                    channel_name = channel_name.strip()
                    url = url.strip()
                    ip_key = get_ip_key(url)
                    
                    if ip_key in detected_ips:
                        if detected_ips[ip_key]['status'] == 'ok':
                            output_file.write(line)
                        continue
                    
                    # 修改后的下载检测逻辑
                    success = False
                    start_time = time.time()
                    try:
                        with requests.get(url, stream=True, timeout=8) as r:  # 总超时8秒
                            r.raise_for_status()
                            downloaded = 0
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:  # 过滤保活帧
                                    downloaded += len(chunk)
                                    if downloaded >= 1024 * 1024:  # 达到1024KB
                                        success = True
                                        break
                                if time.time() - start_time > 8:  # 超时中断
                                    break
                    except Exception as e:
                        pass
                    
                    detected_ips[ip_key] = {'status': 'ok' if success else 'fail'}
                    if success:
                        output_file.write(line)

# 打印检测结果（保持不变）
for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")
