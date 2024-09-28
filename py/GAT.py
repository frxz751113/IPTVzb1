import requests
from bs4 import BeautifulSoup
import re
import os
from opencc import OpenCC
from tqdm import tqdm
import cv2
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time


keywords = ['1905', '凤凰卫视', '人间卫视', '亚洲卫视', '香港卫视', '神乐', '翡翠台', '凤凰香港', '凤凰中文', '凤凰资讯', 'AXN', 'AMC', '好莱坞',  '东森', 'TVB', \
            '龙华', '龙祥', '猪哥亮', '数位', 'AMC', '美亚',  '番薯',  '八大', '三立',  '电影台',  '戏剧台']  # 这里定义你的搜索关键词列表
output_file = 'gat.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for keyword in keywords:
        url = f'http://tonkiang.us/?&iqtv={keyword}'
        response = requests.get(url)
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容并提取文本
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            f.write(text_content + '\n')
        else:
            print(f'请求 {url} 失败，状态码：{response.status_code}')

            
with open('gat.txt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

new_lines = []
for i in range(len(lines)):
    line = lines[i]
    if 'http' in line:
        # 找到当前行之前的非空行作为频道名称
        for j in range(i - 1, -1, -1):
            if lines[j].strip():
                channel_name = lines[j].strip()
                break
        channel_url = line.strip()
        new_lines.append(f'{channel_name},{channel_url}\n')

with open('gat.txt', 'w', encoding='utf-8') as outfile:
    outfile.writelines(new_lines)



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
            urls = re.findall(r'://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))

# 使用方法
remove_duplicates('gat.txt', 'gat.txt')
print("处理完成，去重完成")




################简体转繁体
# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('gat.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入txt文件
with open('gat.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)
print("处理完成，繁体转换完成")







def filter_lines(file_path):
    with open('gat.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    filtered_lines = []
    for line in lines:
        if ',' in line:
         if 'epg' not in line and 'mitv' not in line and 'udp' not in line and 'rtp' not in line \
            and 'P2p' not in line and 'p2p' not in line and 'p3p' not in line and 'P2P' not in line and 'P3p' not in line and 'P3P' not in line:
          filtered_lines.append(line)
    
    return filtered_lines

def write_filtered_lines(output_file_path, filtered_lines):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(filtered_lines)

if __name__ == "__main__":
    input_file_path = 'gat.txt'
    output_file_path = "gat.txt"
    
    filtered_lines = filter_lines(input_file_path)
    write_filtered_lines(output_file_path, filtered_lines)

print("/" * 80)






# ###########################################定义替换规则的字典,对整行内的内容进行替换
replacements = {
        " ": "",
}

# 打开原始文件读取内容，并写入新文件
with open('gat.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建新文件并写入替换后的内容
with open('gat.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():
            line = line.replace(old, new)
        new_file.write(line)   





import cv2
import time
from tqdm import tqdm

# 存储文件路径
file_path = "gat.txt"
output_file_path = "gat.txt"

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
            # 进行检测
            cap = cv2.VideoCapture(url)
            start_time = time.time()
            frame_count = 0
            # 尝试捕获10秒内的帧
            while frame_count < 40 and (time.time() - start_time) < 3:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
            # 释放资源
            cap.release()
            # 根据捕获的帧数判断状态并记录结果
            if frame_count >= 40:  # 10秒内超过200帧则写入
                output_file.write(line)  # 写入检测通过的行

# 无需再打印酒店源，因为这里是对所有URL进行检测，而不是基于IP分组检测



with open('gat.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()

lines.sort()

with open('gat.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)



import re
from pypinyin import lazy_pinyin

# 打开一个utf-8编码的文本文件
with open("gat.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))

# 将排序后的行写入新的utf-8编码的文本文件
with open("gat.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)


print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")
