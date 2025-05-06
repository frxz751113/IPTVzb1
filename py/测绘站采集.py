from lxml import etree
import time
import datetime
from datetime import datetime, timedelta  # 确保 timedelta 被导入
import concurrent.futures
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import os
import threading
from queue import Queue
import queue
from datetime import datetime
import fileinput
from tqdm import tqdm
from pypinyin import lazy_pinyin
from opencc import OpenCC
import base64
import cv2
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from translate import Translator  # 导入Translator类,用于文本翻译
## 定义txt文件的URL列表
urls = [
       'https://dimaston.github.io/live.m3u',  #假m3u
       'https://raw.githubusercontent.com/xiongjian83/TvBox/refs/heads/main/live.txt',
       'https://raw.github.com/ddhola/file/d7afb504b1ba4fef31813e1166cb892215a9c063/0609test',
       'https://raw.github.com/vbskycn/iptv/2738b3bec8c298f57e0e2052b155846ab6ea3787/dsyy/hd.txt',
       'https://raw.github.com/frxz751113/AAAAA/main/IPTV/TW.txt',
       'https://raw.github.com/ljlfct01/ljlfct01.github.io/main/list.%E8%87%AA%E7%94%A8',
       'https://notabug.org/qcfree/TVBox-api/raw/main/live.txt', #通用源
       'https://raw.github.com/KAN314go/A/e81a1c22cd1b9f459bc363bd916c13133e235510/tv/%E5%AE%89%E5%8D%9A8K.txt',
       'https://gitlab.com/tvtg/vip/-/raw/main/log.txt',
       'https://raw.github.com/frxz751113/IPTVzb1/main/%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       'https://raw.github.com/ssili126/tv/main/itvlist.txt',
       'https://raw.github.com/Supprise0901/TVBox_live/main/live.txt',
       'https://raw.github.com/Guovin/TV/gd/result.txt',
       'https://raw.github.com/gaotianliuyun/gao/master/list.txt',
       'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
       'https://raw.github.com/mlvjfchen/TV/main/iptv_list.txt',
       'https://raw.github.com/fenxp/iptv/main/live/tvlive.txt',
       'https://raw.github.com/zwc456baby/iptv_alive/master/live.txt',
       'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt',
       'https://raw.github.com/PizazzGY/TVBox/main/live.txt',
       'https://gitcode.net/MZ011/BHJK/-/raw/master/BHZB1.txt',
       'https://raw.github.com/vbskycn/iptv/master/tv/iptv4.txt',
       'https://raw.github.com/junge3333/juds6/main/yszb1.txt',
       'https://raw.github.com/zzmaze/iptv/main/iptv.txt',
       'https://raw.github.com/kimwang1978/collect-tv-txt/main/others_output.txt',
       'https://raw.github.com/newrecha/TVBOX/5cdd7dcc228f14e4c7f343278e330481aae84eee/live/free.txt',
       'https://bbs.ysctv.cn/tv/live.txt',
       'https://axzzz-my.sharepoint.com/personal/axzzzpan4_axzzz_top/_layouts/15/download.aspx?UniqueId=a357e310-4e3d-45ee-aa68-6913ec533fcc&Translate=false&tempauth=v1.eyJzaXRlaWQiOiIzZGU4M2VmZS0xYWNlLTQ1YWEtODVhNS02YmVlMWM4MTVhZjMiLCJhcHBfZGlzcGxheW5hbWUiOiJBeHp6euS6keebmChvZDQpIiwiYXBwaWQiOiI2NjM3NjZiNi1kYjgwLTQwZjYtYjRkMi1kNWM2NDY0NmQxMjYiLCJhdWQiOiIwMDAwMDAwMy0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvYXh6enotbXkuc2hhcmVwb2ludC5jb21AYzdhMzU1YTUtODgxMS00YzQwLWI1NTktMDk0ZDIzMDMxMjdiIiwiZXhwIjoiMTcyNzkyMjY5MCJ9.CgoKBHNuaWQSAjY0EgsI0ITAwqTVsT0QBRoOMjAuMTkwLjE0NC4xNzEqLGpUa2s3dW1UWFJxYUdMbm9KSVdYS28wbzZnUjJFSWdHemRmcGlpNkliSVk9MJQBOAFCEKFWItxKYAAw1b_et5n_RcNKEGhhc2hlZHByb29mdG9rZW5yKTBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwMzJjNzIwZWQ2QGxpdmUuY29tegEyggESCaVVo8cRiEBMEbVZCU0jAxJ7kgEEcGFuNJoBBUF4enp6ogETYXh6enpwYW40QGF4enp6LnRvcKoBEDEwMDMyMDAzMkM3MjBFRDayAQ5hbGxmaWxlcy53cml0ZcgBAQ._ZmDMLJ917RtVteaBChKC03v2IfufJb1x2SSLpDihu4&ApiVersion=2.0',
       'https://d.kstore.space/download/8209/港澳台终极版.txt',
       'http://wp.wadg.pro/down.php/c7a364c3b23d0b7d3b01e9e731414efc.txt;',
       'https://aiwoa2003.oss-cn-hangzhou.aliyuncs.com/%E5%A4%A9%E5%91%BD%E4%BA%BA.txt',
       'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1715581924111/live1.txt',
       'https://gitea.moe/xiangjiao-ge/yifa169/raw/branch/main/yiyifafa.txt',
       'https://d.kstore.space/download/3701/%E8%8A%B8%E6%B1%90%E7%94%B5%E8%A7%86.txt',
       'https://bbs.ysctv.cn/tv/live.txt',
       'https://d.kstore.space/download/8209/%E6%B8%AF%E6%BE%B3%E5%8F%B0%E7%BB%88%E6%9E%81%E7%89%88.txt',
       'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1724505579710/%E6%80%BB%E7%BB%9F%E7%94%B5%E8%A7%8627.txt',
       'https://raw.bgithub.xyz/luoye20230624/NETZB/6d8798a6a9aef8fce48597b283011e123e0caa2f/%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       '',
       ''
]
# 合并文件的函数
def merge_txt_files(urls, output_filename='汇总.txt'):
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for url in urls:
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # 确保请求成功
                    # 尝试将响应内容解码为UTF-8，如果失败则尝试其他编码
                    try:
                        content = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = response.content.decode('gbk')  # 尝试GBK编码
                    outfile.write(content + '\n')
                except requests.RequestException as e:
                    print(f'Error downloading {url}: {e}')
    except IOError as e:
        print(f'Error writing to file: {e}')

# 调用函数
merge_txt_files(urls)







#简体转繁体
# 创建一个OpenCC对象,指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('汇总.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()
# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)
# 将转换后的简体字写入txt文件
with open('汇总.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)



with open('汇总.txt', 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
#定义替换规则的字典对频道名替换
replacements = {
    	"CCTV-1高清测试": "",
    	"CCTV-2高清测试": "",
    	"CCTV-7高清测试": "",
    	"CCTV-10高清测试": "",
    	"中央": "CCTV",
    	"高清""": "",
    	"HD": "",
    	"标清": "",
    	"amc": "AMC",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"国际": "",
    	"5体育": "5",
    	"6电影": "6",
    	"军农": "",
    	"8影视": "8",
    	"9纪录": "9",
    	"0科教": "0",
    	"2社会与法": "2",
    	"3新闻": "3",
    	"4少儿": "4",
    	"5音乐": "5",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"咪咕": "",
    	"": "",
    	"超清": "",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
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
    	"LD": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	" ": "",
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
    	"电视剧": "影视",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}
with open('汇总.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除行尾的换行符
        line = line.rstrip('\n')
        # 分割行，获取逗号前的字符串
        parts = line.split(',', 1)
        if len(parts) > 0:
            # 替换逗号前的字符串
            before_comma = parts[0]
            for old, new in replacements.items():
                before_comma = before_comma.replace(old, new)
            # 将替换后的逗号前部分和逗号后部分重新组合成一行，并写入新文件
            new_line = f'{before_comma},{parts[1]}\n' if len(parts) > 1 else f'{before_comma}\n'
            new_file.write(new_line)






# 打开文本文件进行读取
def read_and_process_file(input_filename, output_filename, encodings=['utf-8', 'gbk']):
    for encoding in encodings:
        try:
            with open(input_filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"Cannot decode file '{input_filename}' with any of the provided encodings")

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if '$' in line:
                processed_line = line.split('$')[0].rstrip('\n')
                outfile.write(processed_line + '\n')
            else:
                outfile.write(line)

# 调用函数
read_and_process_file('汇总.txt', '汇总.txt')  # 修改输出文件名以避免覆盖原始文件

###################################################################去重#####################################
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
            urls = re.findall(r'[https]?[http]?[rtsp]?[rtmp]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
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
remove_duplicates('汇总.txt', '2.txt')   






######################################################################################提取goodiptv
import re
import os
# 定义一个包含所有要排除的关键词的列表
excluded_keywords = ['epg', 'mitv', 'udp', 'rtp', 'P2p', 'p2p', 'p3p', 'P2P', '新闻综合', 'P3p', 'jdshipin#', '9930/qilu', 'gitcode.net', '151:99', '21dtv', 'txmov2', 'gcw.bdcdn', 'metshop', 
                     'shandong', 'goodiptv', '购物', '[', 'P3P', '腔', '曲', '//1', '/hls/', '春节', '网络收集', '95.179', 'hlspull', 'github', 'lunbo', 'tw.ts138', '114:8278', '//tvb', 'extraott', 
                     '22:8891', 'fanmingming', '43:22222', 'etv.xhgvip', 'free.xiptv', 'www.zhixun', 'xg.52sw', 'iptv.yjxfz.com', 'zb.qc', 'CHC', '/vd', '/TV2/']   #, 'CHC', '/TV2/'

# 定义一个包含所有要提取的关键词的列表
extract_keywords = ['1905', '凤凰卫视', '人间卫视', '亚洲卫视', '香港卫视', '神乐', '翡翠台', '凤凰香港', '凤凰中文', '凤凰资讯', 'AXN', 'AMC', '电影台', '大爱', '东森', 
                    '华视', '中天', '天良', '美亚', '星影', '纬来', '天映', '无线', '华剧台', '华丽台', '剧台', '三立', '八大', '采昌', '民视', '数位', '影视2', 
                    '影视3', '中视', '豬哥亮', 'TVB', '公视', '寰宇', '戏剧', '靖天', '靖洋', '龙华', '龙祥', '猪哥亮', '影迷', '影剧', '电视剧', 
                    '中华小当家', '中天娱乐', '公视戏剧', '珍珠台', '台视', '华视', '环球电视', '美亚C+', '番薯']


# 读取文件并处理每一行
with open('2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

    # 创建或打开一个输出文件用于写入处理后的数据
    with open('网络收集.txt', 'w', encoding='utf-8') as outfile:
        for line in lines:
            # 首先检查行是否包含任何提取关键词
            if any(keyword in line for keyword in extract_keywords):
                # 如果包含提取关键词，进一步检查行是否不包含任何排除关键词
                if not any(keyword in line for keyword in excluded_keywords):
                    outfile.write(line)  # 写入符合条件的行到文件


###############################################################
import re
def parse_file(input_file_path, output_file_name):
    # 正则表达式匹配从'//'开始到第一个'/'或第一个'::'结束的部分
    ip_or_domain_pattern = re.compile(r'//([^/:]*:[^/:]*::[^/:]*|[^/]*)')
    # 用于存储每个IP或域名及其对应的行列表
    ip_or_domain_to_lines = {}
    # 读取原始文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # 如果行是分类标签行，则跳过
            if ",#genre#" in line:
                continue
            # 检查行是否包含IP或域名
            match = ip_or_domain_pattern.search(line)
            if match:
                # 提取匹配到的IP或域名
                matched_text = match.group(1)
                # 去除IP或域名后的剩余部分，只保留匹配到的IP或域名
                ip_or_domain = matched_text.split('://')[-1].split('/')[0].split('::')[0]
                # 将行添加到对应的IP或域名列表中
                if ip_or_domain not in ip_or_domain_to_lines:
                    ip_or_domain_to_lines[ip_or_domain] = []
                ip_or_domain_to_lines[ip_or_domain].append(line)
    ############################################################################### 过滤掉小于1500字节的IP或域名段
    filtered_ip_or_domain_to_lines = {ip_or_domain: lines for ip_or_domain, lines in ip_or_domain_to_lines.items()
                                      if sum(len(line) for line in lines) >= 300}
    # 如果没有满足条件的IP或域名段，则不生成文件
    if not filtered_ip_or_domain_to_lines:
        print("没有满足条件的IP或域名段，不生成文件。")
        return
    # 合并所有满足条件的IP或域名的行到一个文件
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for ip_or_domain, lines in filtered_ip_or_domain_to_lines.items():
            # 写入IP或域名及其对应的行到输出文件
            output_file.write(f"频道,#genre#\n")
            for line in lines:
                output_file.write(line + '\n')
            output_file.write('\n')  # 在每个小段后添加一个空行作为分隔
# 调用函数并传入文件路径和输出文件名
parse_file('网络收集.txt', '网络收集.txt')



import cv2
import time
from tqdm import tqdm
import os

# 存储文件路径
file_path = "网络收集.txt"
output_file_path = "网络收集.txt"

def get_ip_key(url):
    """从 URL 中提取 IP 地址，并构造一个唯一的键"""
    start = url.find('://') + 3
    end = url.find('/', start)
    return url[start:end] if end!= -1 else None

def merge_and_filter():
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)

    # 处理输入文件中的数据并进行检测
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        for i, line in tqdm(enumerate(lines), total=total_lines, desc="Processing", unit='line'):
            if 'genre' in line:
                output_file.write(line)
                continue
            parts = line.split(',', 1)
            if len(parts) == 2:
                channel_name, url = parts
                channel_name = channel_name.strip()
                url = url.strip()
                ip_key = get_ip_key(url)
                if ip_key and ip_key in detected_ips:
                    if detected_ips[ip_key]['status'] == 'ok':
                        output_file.write(line)
                elif ip_key:
                    cap = cv2.VideoCapture(url)
                    start_time = time.time()
                    frame_count = 0
                    while frame_count < 50 and (time.time() - start_time) < 3:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        frame_count += 1
                    cap.release()
                    if frame_count >= 50:
                        detected_ips[ip_key] = {'status': 'ok'}
                        output_file.write(line)
                    else:
                        detected_ips[ip_key] = {'status': 'fail'}

    # 合并任意字符加上网络收集.txt 的文件
    all_files = [f for f in os.listdir(os.getcwd()) if f.endswith('网络收集.txt')]
    with open(output_file_path, 'a', encoding='utf-8') as main_output:
        for file_name in all_files:
            if file_name!= output_file_path:
                with open(file_name, 'r', encoding='utf-8') as other_file:
                    content = other_file.read()
                    if content:
                        main_output.write('\n')
                        main_output.write(content)

detected_ips = {}
merge_and_filter()

for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")



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
remove_duplicates('网络收集.txt', '网络收集.txt')





######################连通性检测

import requests
import time
import cv2
from urllib.parse import urlparse
from tqdm import tqdm

# 测试HTTP连接并尝试下载数据
def test_connectivity_and_download(url, initial_timeout=1, retry_timeout=1):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ['http', 'https']:
        # 非HTTP(s)协议，尝试RTSP检测
        return test_rtsp_connectivity(url, retry_timeout)
    else:
        # HTTP(s)协议，使用原始方法
        try:
            with requests.get(url, stream=True, timeout=initial_timeout) as response:
                if response.status_code == 200:
                    start_time = time.time()
                    while time.time() - start_time < initial_timeout:
                        chunk = response.raw.read(51200)  # 尝试下载1KB数据
                        if chunk:
                            return True  # 成功下载数据
        except requests.RequestException as e:
            print(f"请求异常: {e}")
            pass #这行删掉则会在下载不到数据流的时候进行连通性测试

    return False  # 默认返回False

print("/" * 80)

# 测试RTSP连接并尝试读取流
def test_rtsp_connectivity(url, timeout=3):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        return False
    start_time = time.time()
    while time.time() - start_time < timeout:
        ret, _ = cap.read()
        if ret:
            return True  # 成功读取帧
    cap.release()
    return False

# 主函数
def main(输入, 输出):
    with open(输入, "r", encoding="utf-8") as source_file:
        lines = source_file.readlines()

    results = []
    for line_number, line in enumerate(tqdm(lines, desc="检测中")):
        parts = line.strip().split(",")
        if len(parts) == 2 and parts[1]:  # 确保有URL，并且URL不为空
            channel_name, channel_url = parts
            try:
                is_valid = test_connectivity_and_download(channel_url)
            except Exception as e:
                print(f"检测URL {channel_url} 时发生错误: {e}")
                is_valid = False  # 将异常的URL视为无效

            status = "有效" if is_valid else "无效"

            if "genre" in line.lower() or status == "有效":
                results.append((channel_name.strip(), channel_url.strip(), status))

    # 写入文件
    with open(输出, "w", encoding="utf-8") as output_file:
        for channel_name, channel_url, status in results:
            output_file.write(f"{channel_name},{channel_url}\n")

    print(f"任务完成, 有效源数量: {len([x for x in results if x[2] == '有效'])}, 无效源数量: {len([x for x in results if x[2] == '无效'])}")

if __name__ == "__main__":
    输入 =  "网络收集.txt"    #input('请输入utf-8编码的直播源文件路径:')
    输出 = "网络收集.txt"
    main(输入, 输出)




import re
from pypinyin import lazy_pinyin
# 打开一个utf-8编码的文本文件
with open("网络收集.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')
# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))
# 将排序后的行写入新的utf-8编码的文本文件
with open("网络收集.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)




def parse_file(input_file_path, output_file_name):    #
    # 正则表达式匹配从'//'开始到第一个'/'或第一个'::'结束的部分
    ip_or_domain_pattern = re.compile(r'//([^/:]*:[^/:]*::[^/:]*|[^/]*)')
    # 用于存储每个IP或域名及其对应的行列表
    ip_or_domain_to_lines = {}
    # 用于生成分类名的字母和数字计数器
    alphabet_counter = 0  # 字母计数器，从0开始
    number_counter = 1     # 数字计数器，从1开始
    # 读取原始文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # 如果行是分类标签行，则跳过
            if ",#genre#" in line:
                continue
            # 检查行是否包含IP或域名
            match = ip_or_domain_pattern.search(line)
            if match:
                # 提取匹配到的IP或域名
                matched_text = match.group(1)
                # 去除IP或域名后的剩余部分，只保留匹配到的IP或域名
                ip_or_domain = matched_text.split('://')[-1].split('/')[0].split('::')[0]
                # 将行添加到对应的IP或域名列表中
                if ip_or_domain not in ip_or_domain_to_lines:
                    ip_or_domain_to_lines[ip_or_domain] = []
                ip_or_domain_to_lines[ip_or_domain].append(line)
    # 过滤掉小于1000字节的IP或域名段
    filtered_ip_or_domain_to_lines = {ip_or_domain: lines for ip_or_domain, lines in ip_or_domain_to_lines.items()
                                      if sum(len(line) for line in lines) >= 250}   # 过滤掉小于1000字节的IP或域名段
    # 如果没有满足条件的IP或域名段，则不生成文件
    if not filtered_ip_or_domain_to_lines:
        print("没有满足条件的IP或域名段，不生成文件。")
        return
    # 合并所有满足条件的IP或域名的行到一个文件
############################################################
    with open(output_file_name, 'w', encoding='utf-8') as output_file:   #output_
        for ip_or_domain, lines in filtered_ip_or_domain_to_lines.items():
            # 检查是否需要递增数字计数器
            if alphabet_counter >= 26:
                number_counter += 1
                alphabet_counter = 0  # 重置字母计数器          
 ######################################################              
            # 生成分类名
            genre_name = chr(65 + alphabet_counter)# + str(number_counter)
            output_file.write(f"港澳{genre_name}组,#genre#\n")
            for line in lines:
                output_file.write(line + '\n')
            output_file.write('\n')  # 在每个小段后添加一个空行作为分隔
            alphabet_counter += 1  # 递增字母计数器
# 调用函数并传入文件路径和输出文件名
parse_file('网络收集.txt', '网络收集.txt')





import datetime
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
current_time = now.strftime("%Y/%m/%d %H:%M")
# 打开文本文件并将时间添加到开头
file_path = "网络收集.txt"
with open(file_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(f'{current_time}更新,#genre#\n')
    f.write(f'虚情的爱,https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n{content}')
       

################################################################################################任务结束，删除不必要的过程文件
files_to_remove = ["2.txt", "汇总.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
print("任务运行完毕，频道列表可查看文件夹内源.txt文件！")
