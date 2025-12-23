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
       'https://raw.githubusercontent.com/AnonymousOrz/IPTV/92ee0bf5c26dd20ac118503563d6b7fffa3f0349/Live/collect/CR_250713.txt',  
       'https://raw.githubusercontent.com/lai1tony/git_catvod/bb831377a6622e97ef32e6f8e87069bcb0c50e77/hk1box/live.txt',
       'https://raw.githubusercontent.com/AA999OK/TVBOX/f4b90f95ab2630674318f4a100df07dd3315c96f/CK/017/lib/bhzb2.txt',
       'https://raw.githubusercontent.com/quninainaixi/quninainaixi/6359176dc427bb1afecdd4b160400d8d2bb3109a/DSJ2024417.txt',
       'https://raw.githubusercontent.com/Alan-Alana/IPTV/097f6fa3ecd2ea51521ae03397a418fa16ebed60/channl.txt',
       'https://raw.githubusercontent.com/co115/nh/fb314b614f542b2896ba4b65e88f941dd0e21974/zo.txt',
       'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
       'https://raw.githubusercontent.com/mlzlzj/hnyuan/refs/heads/main/iptv_list.txt',
       'https://live.kakaxi-1.ink/iptv.txt',
       'https://raw.githubusercontent.com/fenxp/iptv/refs/heads/main/live/tvlive.txt',
       'https://myernestlu.github.io/zby.txt',
       'https://raw.githubusercontent.com/adminouyang/231006/refs/heads/main/py/%E4%BC%98%E8%B4%A8%E6%BA%90/output/ipv4/result.txt',
       'https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt',
       'https://raw.githubusercontent.com/alenin-zhang/IPTV/refs/heads/main/lenin.txt',
       'https://raw.githubusercontent.com/frxz751113/IPTVzb1/refs/heads/main/%E7%BD%91%E7%BB%9C%E6%94%B6%E9%9B%86.txt',
       'https://raw.githubusercontent.com/qingtingjjjjjjj/config-tv/refs/heads/main/live.txt',
       'https://raw.githubusercontent.com/zzmaze/iptv/main/itvlist.txt',
       'https://raw.githubusercontent.com/junge3333/juds6/main/yszb1.txt',
       'https://raw.githubusercontent.com/XO-TV/iptv/refs/heads/master/output/hz.txt',
       'https://raw.githubusercontent.com/XO-TV/iptv/refs/heads/master/output/iptv.txt',
       'http://47.120.41.246:8899/zb.txt',
       'http://bxtv.3a.ink/live.txt',
       'https://3043.kstore.space/bhvip/bhzb.txt',
       'https://live.zhoujie218.top/tv/iptv4.txt',
       'https://tv.850930.xyz/kdsb.txt',
       'https://live.zbds.org/tv/iptv6.txt',
       'https://live.zbds.org/tv/iptv4.txt',
       'http://tvv.tw/github.com/fafa002/yf2025/blob/main/yiyifafa.txt',
       'https://freetv.fun/test_channels_original_new.txt',
       'https://jihulab.com/-/snippets/5265/raw/main/.txt',
       'https://raw.githubusercontent.com/cyalias/mytvs-github/refs/heads/main/mytv.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/refs/heads/main/merged_output.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/refs/heads/main/others_output.txt',
       'https://raw.githubusercontent.com/jiangnan1224/iptv_ipv4_live/refs/heads/main/live_ipv4.txt',
       'https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.txt',
       'https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/refs/heads/main/S_CCTV.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/refs/heads/main/S_weishi.txt',
       'https://raw.githubusercontent.com/MemoryCollection/IPTV/refs/heads/main/hotel.txt',
       'https://raw.githubusercontent.com/mlzlzj/hnyuan/refs/heads/main/iptv_list.txt',
       'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
       'https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
       'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt',
       'https://raw.githubusercontent.com/junge3333/juds6/main/yszb1.txt',
       'https://raw.githubusercontent.com/zzmaze/iptv/main/itvlist.txt',
       'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
       'https://raw.githubusercontent.com/n3rddd/CTVLive/refs/heads/main/live.txt',
       'https://raw.githubusercontent.com/xiongjian83/TvBox/refs/heads/main/live.txt',
       'https://raw.githubusercontent.com/yoursmile66/TVBox/refs/heads/main/live.txt',
       'https://raw.githubusercontent.com/alienlu/iptv/refs/heads/master/iptv.txt',
       'https://raw.githubusercontent.com/yuanzl77/IPTV/refs/heads/main/live.txt',
       'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1715581924111/live1.txt',
       'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1715581924675/live2.txt',
       'https://cc-im-kefu-cos.7moor-fs2.com/im/2768a390-5474-11ea-afc9-7b323e3e16c0/d4fe44c5-107c-4511-af02-aa08fb10dff7/2024-04-25/2024-04-25_17:22:21/1714036941087/98644330/wexiptv.txt',
       'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1716213337323/live3.txt',
       'https://live.zbds.top/tv/iptv4.txt',
       'https://live.zbds.top/tv/iptv6.txt',
       'http://home.jundie.top:81/Cat/tv/live.txt',
       'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt',
       'https://m3u.ibert.me/txt/fmml_ipv6.txt',
       'https://m3u.ibert.me/txt/ycl_iptv.txt',
       'https://m3u.ibert.me/txt/y_g.txt',
       'https://gitee.com/tushaoyong/live/raw/master/%E6%8E%A5%E5%8F%A3/IPV6.txt',
       'http://tot.totalh.net/tttt.txt',
       'https://d.kstore.dev/download/6529/tvbox/fmzb_livetv.txt',
       'https://qu.ax/yfFxv.txt',
       'http://txt.kesug.com/users/HKTV.txt',
       'http://txt.kesug.com/users/hulanlu.txt',
       'http://gm.scvip.net.cn/iptv/iptv.txt',
       'https://raw.githubusercontent.com/mlvjfchen/TV/refs/heads/main/output/result.txt',
       'https://9239.kstore.space/jisuTV2.txt',
       'http://175.178.251.183:6689/live.txt',
       'http://102.134.54.106:3099/live/全国酒店源mini.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt',
       'https://raw.githubusercontent.com/PizazzGY/TVBox/main/live.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/main/S_CCTV.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/main/S_weishi.txt',
       'http://mdxgh.tpddns.cn:9999/new/mdzb.txt',
       'http://www.xzitv.top/tvy/iTV.txt',
       'http://tm.tttttttttt.top/txt/7788.txt',
       'https://raw.githubusercontent.com/qinvision/Film-Television/main/dujuejiami.txt',
       'https://gitee.com/lixiao-1-98/iptv/raw/master/ipv4.txt',
       'https://d.kstore.space/download/7395/xiaohei.txt',
       'https://2912.kstore.space/520.txt',
       'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
       'https://raw.githubusercontent.com/Guovin/iptv-api/refs/heads/gd/output/result.txt',
       'https://m3u.ibert.me/txt/o_cn.txt',
       'https://m3u.ibert.me/txt/j_iptv.txt',
       'https://m3u.ibert.me/txt/fmml_ipv6.txt',
       'https://m3u.ibert.me/txt/ycl_iptv.txt',
       'https://m3u.ibert.me/txt/y_g.txt',
       'https://m3u.ibert.me/txt/j_home.txt',
       'https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
       'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
       'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
       'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt',
       'http://117.72.68.25:9230/latest.txt',
       'https://raw.githubusercontent.com/junge3333/juds6/main/yszb1.txt',
       'https://raw.githubusercontent.com/zzmaze/iptv/main/iptv.txt',
       'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt',
       'https://raw.githubusercontent.com/gdstchdr1/IPTV/main/bc.txt',
       'https://raw.githubusercontent.com/lalifeier/IPTV/main/txt/IPTV.txt',
       'https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt',
       'https://raw.githubusercontent.com/pxiptv/live/main/iptv.txt',
       'https://raw.githubusercontent.com/Andreayoo/ming/main/IPTV.txt',
       'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
       'https://raw.githubusercontent.com/Fairy8o/IPTV/main/PDX-V4.txt',
       'http://ww.weidonglong.com/dsj.txt',
       'https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt',
       'https://gitee.com/tutu316/tv/raw/main/live.txt',
       'https://8249.kstore.space/lswj/tv.txt',
       'https://live.iptv365.org/live.txt',
       'http://8.138.7.223/live.txt',
       'https://l.gmbbk.com/upload/14781478.txt',
       'https://raw.githubusercontent.com/qinvision/Film-Television/main/dujuejiami.txt',
       'http://l.gmbbk.com/upload/30123012.txt',
       'https://live.zbds.top/tv/iptv4.txt',
       'http://175.178.251.183:6689/live.txt',
       'https://cdn.jsdelivr.net/gh/xzw832/cmys@main/S_CCTV.txt',
       'https://cdn.jsdelivr.net/gh/xzw832/cmys@main/S_weishi.txt',
       'https://cdn.jsdelivr.net/gh/asdjkl6/tv@tv/.m3u/整套直播源/测试/整套直播源/l.txt',
       'https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt',
       'https://github.com/mlzlzj/IPTV2/blob/main/txt/jiudian/%E5%85%A8%E5%9B%BD.txt',
       'https://live.zhoujie218.top/tv/iptv4.txt',
       'http://ww.weidonglong.com/dsj.txt',
       'https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.txt',
       'http://live.nctv.top/x.txt',
       'https://raw.githubusercontent.com/develop202/migu_video/refs/heads/main/interface.txt',
       'https://raw.githubusercontent.com/alenin-zhang/IPTV/refs/heads/main/lenin.txt',
       'https://raw.githubusercontent.com/kakaxi-1/IPTV/refs/heads/main/ipv4.txt',
       'http://bxtv.3a.ink/live.txt',
       'https://15280.kstore.space/%E5%A5%A5%E5%8F%B0.txt',
       'http://38.165.20.168/js/%E7%9B%B4%E6%92%AD.txt',
       'https://chuxinya.top/f/XooOhO/%E6%B8%AF%E6%BE%B3%E5%8F%B0%E8%B5%84%E6%BA%90.txt',
       'https://chuxinya.top/f/VPk3ig/Rig1Ie5B_%E6%B8%AF%E6%BE%B3%E5%8F%B0%E8%B5%84%E6%BA%90.txt',
       'https://raw.githubusercontent.com/frxz751113/IPTVzb1/refs/heads/main/%E7%BD%91%E7%BB%9C%E6%94%B6%E9%9B%86.txt',
       'https://raw.githubusercontent.com/Cx4x/6/refs/heads/main/tx.txt',
       'https://raw.githubusercontent.com/Cx4x/6/refs/heads/main/mg.txt',
       'https://c.cxics.com/ds/%E7%A7%92%E6%92%AD.txt',
       'http://gg.7749.org/z/i/5788.txt',
       'http://gg.7749.org/z/i/HKTV28.txt',
       'http://gg.7749.org//i/ds.txt',
       'https://3043.kstore.space/bhvip/bhzb.txt',
       'http://is.is-great.org/i/0947307.txt',
       'https://raw.githubusercontent.com/alantang1977/X/refs/heads/main/live/go.txt',
       'https://raw.githubusercontent.com/lml1971/tv/refs/heads/main/tv.txt',
       'http://txt.kesug.com/users/NOW.txt',
       'http://aktv.top/live.txt',
       'http://8.138.7.223/live.txt',
       'https://live.izbds.com/tv/iptv4.txt',
       'https://tv.850930.xyz/kdsb.txt',
       'http://47.120.41.246:8899/zb.txt',
       'http://cccccccoccccccc.ccccocccc.cc/uploads/%E6%8A%AC%E6%89%9B_1.txt',
       'http://kkk.jjjj.jiduo.me/user/tttt/api.txt',
       'https://tzdr.com/iptv.txt',
       'http://ww.weidonglong.com/dsj.txt',
       'http://wx.thego.cn/hk.txt',
       'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/refs/heads/main/S_CCTV.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/refs/heads/main/S_weishi.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/assets/special/special.txt',
       'https://live.zhoujie218.top/tv/iptv6.txt',
       'http://mdxgh.tpddns.cn:9999/new/mdzb.txt',
       'https://raw.githubusercontent.com/mlzlzj/hnyuan/refs/heads/main/iptv_list.txt',
       'http://ttkx.cc:55/lib/kx2024.txt',
       'http://ttkx.live:55/lib/kx2024.txt',
       'http://xnur0a.xndkw.xn6qq986b3xl/down.php/a7c9d038627e11f037adcad788da129e.txt',
       'http://kxrj.site:55/lib/kx2024.txt',
       'https://live.zbds.top/tv/iptv4.txt',
       'https://cdn05042023.gitlink.org.cn/liliang74120/cmds/raw/branch/master/myDS.txt',
       'https://cdn05042023.gitlink.org.cn/api/v1/repos/xuanbei/ysv/raw/live.txt',
       'https://2912.kstore.space/520.txt',
       'https://github.com/frxz751113/IPTVzb1/blob/main/%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       'https://raw.githubusercontent.com/frxz751113/IPTVzb1/refs/heads/main/{MMdd}%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       'https://raw.githubusercontent.com/frxz751113/IPTVzb1/refs/heads/main/{MMdd-1}%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       'https://gitlab.com/tvtg/vip/-/raw/main/log.txt',
       'https://d.kstore.space/download/7395/xiaohei.txt',
       'http://117.72.68.25:9230/latest.txt',
       'http://home.jundie.top:81/Cat/tv/live.txt',
       'http://175.178.251.183:6689/live.txt',
       'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
       'https://10085.kstore.space/%E8%93%9D%E5%A4%A9%E7%99%BD%E4%BA%91.txt',
       'https://m3u.ibert.me/txt/fmml_ipv6.txt',
       'https://m3u.ibert.me/txt/ycl_iptv.txt',
       'https://m3u.ibert.me/txt/y_g.txt',
       'https://m3u.ibert.me/txt/j_home.txt',
       'http://vip.vip0531.com/viptv/live202405.txt',
       'https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
       'https://raw.githubusercontent.com/fenxp/iptv/main/live/tvlive.txt',
       'https://raw.githubusercontent.com/fenxp/iptvs/dist/live.txt',
       'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
       'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt',
       'https://raw.githubusercontent.com/PizazzGY/TVBox/main/live.txt',
       'https://raw.githubusercontent.com/wwb521/live/main/tv.txt',
       'https://gitcode.net/MZ011/BHJK/-/raw/master/BHZB1.txt',
       'http://47.99.102.252/live.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt',
       'http://xhztv.top/v6.txt',
       'https://tvkj.top/tvlive.txt',
       'https://raw.githubusercontent.com/junge3333/juds6/main/yszb1.txt',
       'https://raw.githubusercontent.com/zzmaze/iptv/main/iptv.txt',
       'https://raw.githubusercontent.com/zzmaze/iptv/main/itvlist.txt',
       'http://wp.wadg.pro/down.php/d7b52d125998d00e2d2339bac6abd2b5.txt',
       'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
       'https://raw.githubusercontent.com/kimwang1978/TV/master/output/result.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/refs/heads/main/assets/freetv/freetv_output_other.txt',
       'http://1805842a.123nat.com:66/agent/2.txt',
       'https://gongdian.top/tv/gongdian.txt',
       'https://gitea.moe/Fathers/EkfkgH/raw/branch/main/yyfug.txt',
       'https://raw.gitcode.com/hjf520/00/raw/main/sirenzb.txt',
       'http://154.9.252.167:190/tvlive.txt',
       'https://gitee.com/tushaoyong/live/raw/master/%E6%8E%A5%E5%8F%A3/IPV6.txt',
       'https://raw.githubusercontent.com/MemoryCollection/IPTV/main/itvlist.txt',
       'https://raw.githubusercontent.com/zzj2678/IPTVzb1/refs/heads/main/iptv_list.txt',
       'http://120.79.4.185/new/mdlive.txt',
       'http://l.gmbbk.com/upload/16401640.txt',
       'http://122.228.85.203:5988/uploads/tvbox/tv.txt',
       'https://raw.githubusercontent.com/lystv/short/main/影视/tvb/MTV.txt',
       'http://xhztv.top/zbc.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt',
       'http://175.178.251.183:6689/aktvlive.txt',
       'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
       'https://live.zbds.top/tv/iptv4.txt',
       'https://raw.githubusercontent.com/asdjkl6/tv/tv/.m3u/整套直播源/测试/整套直播源/l.txt',
       'https://raw.githubusercontent.com/asdjkl6/tv/tv/.m3u/整套直播源/测试/整套直播源/kk.txt',
       'https://live.zbds.top/tv/iptv6.txt',
       'http://xhztv.top/new.txt',
       'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt',
       'https://live.zhoujie218.top/tv/iptv6.txt',
       'https://raw.githubusercontent.com/cymz6/AutoIPTV-Hotel/main/lives.txt',
       'https://raw.githubusercontent.com/PizazzGY/TVBox_warehouse/main/live.txt',
       'https://m3u.ibert.me/txt/o_cn.txt',
       'https://m3u.ibert.me/txt/j_iptv.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/main/S_CCTV.txt',
       'https://raw.githubusercontent.com/xzw832/cmys/main/S_weishi.txt',
       'https://iptv.b2og.com/txt/fmml_ipv6.txt',
       'http://xhztv.top/zbc.txt',
       'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output_simple.txt',
       'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/黑龙江PLTV移动CDN版.txt',
       'https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt',
       'https://live.zhoujie218.top/tv/iptv4.txt',
       'https://live.zbds.org/tv/yd.txt',
       'https://live.zbds.org/tv/iptv6.txt',
       'https://chinaiptv.pages.dev/Unicast/anhui/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/fujian/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/guangxi/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/hebei/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/heilongjiang/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/henan/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/hubei/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/jiangxi/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/jiangsu/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/shan3xi/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/shandong/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/zhejiang/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/shanghai/mobile.txt',
       'https://chinaiptv.pages.dev/Unicast/liaoning/mobile.txt',
       'https://mycode.zhoujie218.top/me/jsyd.txt',
       'https://raw.githubusercontent.com/q1017673817/iptv_zubo/refs/heads/main/hnyd.txt',
       'https://raw.githubusercontent.com/suxuang/myIPTV/refs/heads/main/%E7%A7%BB%E5%8A%A8%E4%B8%93%E4%BA%AB.txt',
       'https://live.zbds.org/tv/zjyd.txt',
       'https://live.zbds.org/tv/zjyd1.txt',
       'https://live.zbds.org/tv/jxyd.txt',
       'https://live.zbds.org/tv/sxyd.txt',
       'https://vdyun.com/hbm3u.txt',
       'https://vdyun.com/hbcm.txt',
       'https://vdyun.com/hbcm1.txt',
       'https://vdyun.com/hbcm2.txt',
       'https://vdyun.com/yd.txt',
       'https://vdyun.com/yd2.txt',
       'https://vdyun.com/ipv6.txt',
       'https://vdyun.com/sjzcm1.txt',
       'https://vdyun.com/sjzcm2.txt',
       'https://vdyun.com/hljcm.txt',
       'https://d.kstore.dev/download/15114/TVSolo.txt',
       'https://raw.githubusercontent.com/adminouyang/231006/refs/heads/main/py/TV/output/ipv4/result.txt',
       'https://raw.githubusercontent.com/250992941/iptv/717bd6b563a826f77e46daeb41c2bc7ba4e36644/ZB.txt',
       'https://raw.githubusercontent.com/luoye20230624/NETZB/455e4be621bbe07a129365b87ca5d12abc71936f/%E7%BD%91%E7%BB%9C%E6%94%B6%E9%9B%86.txt',
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
excluded_keywords = ['epg', 'mitv', 'udp', 'rtp', 'P2p', 'p2p', 'p3p', 'P2P', 'P3p', 'jdshipin#', '9930/qilu', 'gitcode.net', '151:99', 
                     '21dtv', 'txmov2', 'gcw.bdcdn', 'metshop', 'shandong', 'goodiptv', '购物', '[', 'P3P', '腔', '曲', '//1', '/hls/', '/tsfile/', 
                     '春节', '网络收集', '95.179', 'hlspull', 'github', 'lunbo', 'tw.ts138', '//tvb', 'extraott', 
                     '22:8891', 'fanmingming', '43:22222', 'etv.xhgvip', 'free.xiptv', 'www.zhixun', 'xg.52sw', 'iptv.yjxfz.com', 
                     'zb.qc', '/vd', '/TV2/']   #, 'CHC', '/TV2/'

# 定义一个包含所有要提取的关键词的列表
extract_keywords = ['1905', 'cctv1,', 'cctv15,', 'cctv3,', '风云音乐,', '凤凰卫视', '人间卫视', '亚洲卫视', '香港卫视', '神乐', '翡翠台', '凤凰香港', '凤凰中文', '凤凰资讯', 'AXN', 'AMC', '电影台', '大爱', '东森', 
                    '华视', '中天', '天良', '美亚', '星影', '纬来', '天映', '无线', '华剧台', '华丽台', '剧台', '三立', '八大', '采昌', '民视', '数位', '影视2', 
                    '影视3', '中视', '豬哥亮', 'TVB', '公视', '寰宇', '戏剧', '靖天', '靖洋', '龙华', '龙祥', '猪哥亮', '影迷', '影剧', '电视剧', 
                    '中华小当家', '中天娱乐', '公视戏剧', '珍珠台', '台视', '华视', '环球电视', '美亚C+', 'AMC', 'AXN', 'Asia', 'CNA', 'HBO', 'HITS', 
                    'Movies', '澳门', '八大', '半岛新闻', '东森', '凤凰', '环球电视', '寰宇', '翡翠', '龙华', '龙祥', '美亚', '明珠', '三立', '台视', 
                    '探索亚洲', '天映', '纬来', 'chc', '中视', '中天', '番薯']


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
                    while frame_count < 30 and (time.time() - start_time) < 3:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        frame_count += 1
                    cap.release()
                    if frame_count >= 30:
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
