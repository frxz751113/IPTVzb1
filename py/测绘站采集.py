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
        search_txt = f'"udpxy" && country="CN" && region="{province}"'
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

######################################################
#####################################################
######################################################################################################################

#################################################################################
###############检测playlist文件夹内所有txt文件内的组播
###############检测playlist文件夹内所有txt文件内的组播
###############检测playlist文件夹内所有txt文件内的组播

import os
import cv2
import time
from tqdm import tqdm
import sys

# 初始化字典以存储IP检测结果
detected_ips = {}

def get_ip_key(url):
    """从URL中提取IP地址或域名，并构造一个唯一的键"""
    start = url.find('://') + 3
    end = url.find('/', start)
    if end == -1:
        end = len(url)
    return url[start:end].strip()

# 设置固定的文件夹路径
folder_path = 'playlist'

# 确保文件夹路径存在
if not os.path.isdir(folder_path):
    print("指定的文件夹不存在。")
    sys.exit()

# 遍历文件夹中的所有.txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 准备写回文件
        with open(file_path, 'w', encoding='utf-8') as output_file:
            # 使用 tqdm 显示进度条
            for line in tqdm(lines, total=len(lines), desc=f"Processing {filename}"):
                parts = line.split(',', 1)
                if len(parts) >= 2:
                    channel_name, url = parts
                    channel_name = channel_name.strip()
                    url = url.strip()
                    ip_key = get_ip_key(url)
                    
                    # 检查IP或域名是否已经被检测过
                    if ip_key in detected_ips:
                        # 如果之前检测成功，则写入该行
                        if detected_ips[ip_key]['status'] == 'ok':
                            output_file.write(line)
                        continue  # 无论之前检测结果如何，都不重新检测
                    
                    # 初始化帧计数器和成功标志
                    frame_count = 0
                    success = False
                    # 尝试打开视频流
                    cap = cv2.VideoCapture(url)
                    start_time = time.time()
                    while (time.time() - start_time) < 8:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        frame_count += 1
                        # 如果在8秒内读取到1帧以上，设置成功标志
                        if frame_count >= 1:
                            success = True
                            break
                    cap.release()
                    
                    # 根据检测结果更新字典
                    if success:
                        detected_ips[ip_key] = {'status': 'ok'}
                        output_file.write(line)
                    else:
                        detected_ips[ip_key] = {'status': 'fail'}

# 打印检测结果
for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")
######################################################################################################################
######################################################################################################################

#  获取远程直播源文件,打开文件并输出临时文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/refs/heads/main/IPTV/%E6%B1%87%E6%B1%87.txt"          #源采集地址
r = requests.get(url)
open('综合源.txt','wb').write(r.content)         #打开源文件并临时写入


#简体转繁体#
#简体转繁体
# 创建一个OpenCC对象,指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('综合源.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()
# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)
# 将转换后的简体字写入txt文件
with open('综合源.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)




#任务结束,删除不必要的过程文件#
files_to_remove = ['组播源.txt', "TW.txt", "a.txt", "主.txt", "b.txt", "b1.txt", "港澳.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file} 不存在,跳过删除。")
print("任务运行完毕,分类频道列表可查看文件夹内综合源.txt文件！")



######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# 合并自定义频道文件,优选源整理
# 假设filter_files是一个自定义函数，它返回playlist目录下所有.txt文件的路径列表
def filter_files(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]
# 获取playlist目录下的所有.txt文件
files = filter_files('playlist', '.txt')
# 打开输出文件
with open("4.txt", "w", encoding="utf-8") as output:
    for file_path in files:
        with open(os.path.join('playlist', file_path), 'r', encoding="utf-8") as file:
            content = file.read()
            output.write(content + '\n\n')
print("电视频道成功写入")
    
#################文本排序
# 打开原始文件读取内容,并写入新文件
with open('4.txt', 'r', encoding='utf-8') as file:
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
with open('5.txt', "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)
print(f"文件已排序并保存为: {output_file_path}")
import cv2
import time
from tqdm import tqdm
# 初始化酒店源字典
detected_ips = {}
# 存储文件路径
file_path = "5.txt"
output_file_path = "2.txt"
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
                # 尝试捕获10秒内的帧
                while frame_count < 200 and (time.time() - start_time) < 10:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame_count += 1
                # 释放资源
                cap.release()
                # 根据捕获的帧数判断状态并记录结果
                if frame_count >= 200:  #10秒内超过230帧则写入
                    detected_ips[ip_key] = {'status': 'ok'}
                    output_file.write(line)  # 写入检测通过的行
                else:
                    detected_ips[ip_key] = {'status': 'fail'}
# 打印酒店源
for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")
########################################################################################################################################################################################
################################################################定义关键词分割规则
def check_and_write_file(input_file, output_file, keywords):
    # 使用 split(', ') 来分割关键词
    keywords_list = keywords.split(', ')
    pattern = '|'.join(re.escape(keyword) for keyword in keywords_list)
    # 读取输入文件并提取包含关键词的行
    extracted_lines = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
          if "genre" not in line:
            if re.search(pattern, line):
                extracted_lines.append(line)
    # 如果至少提取到一行,写入头部信息和提取的行到输出文件
    if extracted_lines:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(f"{keywords_list[0]},#genre#\n")  # 写入头部信息
            out_file.writelines(extracted_lines)  # 写入提取的行
        # 获取头部信息的大小
        header_size = len(f"{keywords_list[0]},#genre#\n")
        
        # 检查文件的总大小
        file_size = os.path.getsize(output_file)
        
        # 如果文件大小小于30字节（假设的最小文件大小）,删除文件
        if file_size < 200:
            os.remove(output_file)
            print(f"文件只包含头部信息,{output_file} 已被删除。")
        else:
            print(f"文件已提取关键词并保存为: {output_file}")
    else:
        print(f"未提取到关键词,不创建输出文件 {output_file}。")

# 按类别提取关键词并写入文件
check_and_write_file('2.txt',  'a.txt',  keywords="央视频道, CCTV, CHC, 全球大片, 星光院线, 8K, 4K, 4k")
check_and_write_file('2.txt',  'b.txt',  keywords="卫视频道, 卫视, 凤凰, 星空")
check_and_write_file('2.txt',  'c0.txt',  keywords="组播剧场, 第一剧场, 怀旧剧场, 风云音乐, 风云剧场, 欢笑剧场, 都市剧场, 高清电影, 家庭影院, 动作电影, 影迷, 峨眉, 重温, 女性, 地理")
check_and_write_file('2.txt',  'c.txt',  keywords="组播剧场, 爱动漫, SiTV, 爱怀旧, 爱经典, 爱科幻, 爱青春, 爱悬疑, 爱幼教, 爱院线")
check_and_write_file('2.txt',  'd.txt',  keywords="北京频道, 北京")
###############################################################################################################################################################################################################################
##############################################################对生成的文件进行合并
file_contents = []
file_paths = ["a.txt", "b.txt", "c0.txt", "c.txt", "d.txt"]  # 替换为实际的文件路径列表
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
###############################################################################################################################################################################################################################
##############################################################对生成的文件进行网址及文本去重复,避免同一个频道出现在不同的类中
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
remove_duplicates('去重.txt', '分类.txt')

#从整理好的文本中进行特定关键词替换以规范频道名#
for line in fileinput.input("分类.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("CCTV1,", "CCTV1-综合,")  
    line = line.replace("CCTV2,", "CCTV2-财经,")  
    line = line.replace("CCTV3,", "CCTV3-综艺,")  
    line = line.replace("CCTV4,", "CCTV4-国际,")  
    line = line.replace("CCTV5,", "CCTV5-体育,")  
    line = line.replace("CCTV5+,", "CCTV5-体育plus,")  
    line = line.replace("CCTV6,", "CCTV6-电影,")  
    line = line.replace("CCTV7,", "CCTV7-军事,")  
    line = line.replace("CCTV8,", "CCTV8-电视剧,")  
    line = line.replace("CCTV9,", "CCTV9-纪录,")  
    line = line.replace("CCTV10,", "CCTV10-科教,")  
    line = line.replace("CCTV11,", "CCTV11-戏曲,")  
    line = line.replace("CCTV11+,", "CCTV11-戏曲,")  
    line = line.replace("CCTV12,", "CCTV12-社会与法,")  
    line = line.replace("CCTV13,", "CCTV13-新闻,")  
    line = line.replace("CCTV14,", "CCTV14-少儿,")  
    line = line.replace("CCTV15,", "CCTV15-音乐,")  
    line = line.replace("CCTV16,", "CCTV16-奥林匹克,")  
    line = line.replace("CCTV17,", "CCTV17-农业农村,") 
    line = line.replace("CHC", "") 
    print(line, end="")   


# 打开文档并读取所有行 
with open('分类.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
# 使用列表来存储唯一的行的顺序 
unique_lines = []
seen_lines = set()
# 遍历每一行，如果是新的就加入unique_lines
for line in lines:
    if line not in seen_lines:
        unique_lines.append(line)
        seen_lines.add(line)

# 将唯一的行写入第一个文件
with open('组播优选.txt', 'w', encoding="utf-8") as file:
    for line in unique_lines:
        file.write(line)  # 确保每行后面有换行符 + '\n'
# 将唯一的行追加到第二个文件
#with open('综合源.txt', 'a', encoding="utf-8") as file:
    #for line in unique_lines:
        #file.write(line)  # 确保每行后面有换行符 + '\n'

# 定义要排除的关键词列表
excluded_keywords = ['CCTV', '卫视', '关键词3']
# 定义例外关键词列表，即使它们在排除列表中，也应该被保留
exception_keywords = ['4K', '8K', '例外关键词']
# 打开原始文本文件并读取内容
with open('组播优选.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 过滤掉包含关键词的行，但是允许含有例外关键词的行
filtered_lines = []
for line in lines:
    # 检查行是否包含排除关键词
    contains_excluded = any(keyword in line for keyword in excluded_keywords)
    # 检查行是否包含例外关键词
    contains_exception = any(keyword in line for keyword in exception_keywords)
    # 如果行包含排除关键词，但是不包含例外关键词，则过滤掉该行
    if contains_excluded and not contains_exception:
        continue
    else:
        # 如果行不包含排除关键词，或者同时包含排除关键词和例外关键词，则保留该行
        filtered_lines.append(line)
# 将过滤后的内容追加写入新的文本文件
with open('综合源.txt', 'a', encoding='utf-8') as file:
    file.writelines(filtered_lines)

#从整理好的文本中进行特定关键词替换以规范频道名#
for line in fileinput.input("综合源.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("CCTV164K", "CCTV16-4K")  
    line = line.replace("CCTV4K", "CCTV-4K")  
    print(line, end="")   



################################################################################################任务结束,删除不必要的过程文件
files_to_remove = ['去重.txt', '分类.txt', "2.txt", "4.txt", "5.txt", "a.txt", "b.txt", "c0.txt", "c.txt", "d.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file} 不存在,跳过删除。")
print("任务运行完毕,分类频道列表可查看文件夹内综合源.txt文件！")
# 打印酒店源
for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")
