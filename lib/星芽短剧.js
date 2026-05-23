/* 星芽短剧 独立完整抽取代码 */
import 'assets://js/lib/crypto-js.js';

// 1. 全局UA、星芽专属配置
const UA = 'Mozilla/5.0 (Linux; Android 9; V2196A Build/PQ3A.190705.08211809; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:416;packageName:com.jp3.xg3';

// 聚合配置仅保留星芽相关
const aggConfig = {
  keys: 'd3dGiJc651gSQ8w1',
  charMap: {
    '+': 'P', '/': 'X', '0': 'M', '1': 'U', '2': 'l', '3': 'E', '4': 'r', '5': 'Y', '6': 'W', '7': 'b', '8': 'd', '9': 'J',
    'A': '9', 'B': 's', 'C': 'a', 'D': 'I', 'E': '0', 'F': 'o', 'G': 'y', 'H': '_', 'I': 'H', 'J': 'G', 'K': 'i', 'L': 't',
    'M': 'g', 'N': 'N', 'O': 'A', 'P': '8', 'Q': 'F', 'R': 'k', 'S': '3', 'T': 'h', 'U': 'f', 'V': 'R', 'W': 'q', 'X': 'C',
    'Y': '4', 'Z': 'p', 'a': 'm', 'b': 'B', 'c': 'O', 'd': 'u', 'e': 'c', 'f': '6', 'g': 'K', 'h': 'x', 'i': '5', 'j': 'T',
    'k': '-', 'l': '2', 'm': 'z', 'n': 'S', 'o': 'Z', 'p': '1', 'q': 'V', 'r': 'v', 's': 'j', 't': 'Q', 'u': '7', 'v': 'D',
    'w': 'w', 'x': 'n', 'y': 'L', 'z': 'e'
  },
  headers: {
    default: {
      'User-Agent': 'okhttp/3.12.11',
      'content-type': 'application/json; charset=utf-8'
    }
  },
  // 仅星芽平台接口域名与路由
  platform: {
    星芽: {
      host: 'https://app.whjzjx.cn',
      url1: '/cloud/v2/theater/home_page?theater_class_id',
      url2: '/v2/theater_parent/detail',
      search: '/v3/search',
      loginUrl: 'https://u.shytkjgs.com/user/v1/account/login'
    }
  },
  platformList: [
    { name: '星芽短剧', id: '星芽' }
  ],
  search: {
    limit: 30,
    timeout: 6000
  }
};

// 筛选规则定义 仅星芽
const ruleFilterDef = {
  星芽: { area: '1' }
};

// 筛选选项 仅星芽
const filterOptions = {
  "星芽": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "剧场", "v": "1"},
      {"n": "热播剧", "v": "2"},
      {"n": "会员专享", "v": "8"},
      {"n": "星选好剧", "v": "7"},
      {"n": "新剧", "v": "3"},
      {"n": "阳光剧场", "v": "5"}
    ]
  }]
};

// 星芽全局header缓存
let xingya_headers = {};

// 2. 公共工具函数
function base64Encode(text) {
    return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(text));
}
function base64Decode(text) {
    return CryptoJS.enc.Utf8.stringify(CryptoJS.enc.Base64.parse(text));
}
async function request(url, options = {}) {
    const { method = 'GET', headers = {}, body, timeout = 5000 } = options;
    const isPost = method.toUpperCase() === 'POST';
    
    let requestBody = body;
    if (body && typeof body === 'object') {
        requestBody = JSON.stringify(body);
    }
    
    if (typeof req !== 'undefined') {
        const reqOptions = {
            method: method,
            headers: { ...aggConfig.headers.default, ...headers },
            body: isPost ? requestBody : null,  
            timeout: timeout,
        };
        
        const response = await req(url, reqOptions);
        return response.content;
    }
}
async function md5(str) {
  try {
    return CryptoJS.MD5(str).toString(CryptoJS.enc.Hex).toLowerCase();
  } catch (error) {
    return "";
  }
}
function aesDecrypt(encryptedContent, key, iv) {
  try {
    const parsedKey = CryptoJS.enc.Utf8.parse(key || 'IjhHsCB2B5^#%0Ag');
    const parsedIv = CryptoJS.enc.Utf8.parse(iv || 'y8_m.3rauW/>j,}.');
    const encrypted = CryptoJS.enc.Base64.parse(encryptedContent);
    const decrypted = CryptoJS.AES.decrypt(
      { ciphertext: encrypted },
      parsedKey,
      { 
        iv: parsedIv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
      }
    );
    return decrypted.toString(CryptoJS.enc.Utf8);
  } catch (error) {
    return encryptedContent;
  }
}
function encHex(txt) {
  try {
    const key = CryptoJS.enc.Utf8.parse("p0sfjw@k&qmewu#w");
    const encrypted = CryptoJS.AES.encrypt(
      CryptoJS.enc.Utf8.parse(txt),
      key,
      {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
      }
    );
    return encrypted.ciphertext.toString(CryptoJS.enc.Hex);
  } catch (error) {
    return "";
  }
}
function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0,
      v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
function getRandomItem(items) {
  return items[Math.random() * items.length | 0];
}

// 3. 星芽专属Header获取
async function getXingyaHeaders() {
  if (xingya_headers && xingya_headers.authorization) {
    return xingya_headers;
  }
  return aggConfig.headers.default;
}

// 4. 星芽初始化（登录获取token）
async function init(cfg) {
  try {
    const data = {
      'device': '24250683a3bdb3f118dff25ba4b1cba1a'
    };
    const options = {
      method: 'POST',
      headers: {
        'User-Agent': 'okhttp/4.10.0',
        'platform': '1',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    };
    
    let response = await request(aggConfig.platform.星芽.loginUrl, options);
    const res = JSON.parse(response);
    
    if (res) {
      const token = res?.data?.token || 
                    res?.data?.data?.token || 
                    res?.token || 
                    res?.result?.token ||
                    res?.access_token;
      
      if (token) {
        xingya_headers = { ...aggConfig.headers.default, authorization: token };
      } else {
        xingya_headers = aggConfig.headers.default;
      }
    } 
  } catch (e) {
    xingya_headers = aggConfig.headers.default;
  }
  return true;
}

// 5. 分类栏目接口
async function home(filter) {
  const classes = aggConfig.platformList.map(item => ({
    type_name: item.name,
    type_id: item.id
  }));
  const filters = {};
  aggConfig.platformList.forEach(item => {
    const platformId = item.id;
    if (filterOptions[platformId]) {
      filters[platformId] = filterOptions[platformId];
    }
  });
  return JSON.stringify({
    class: classes,
    filters: filters
  });
}

// 6. 首页推荐
async function homeVod(params) {
  return await recommend();
}
async function recommend() {
  let recommendList = [];
  if (aggConfig.platformList && aggConfig.platformList.length > 0) {
    const randomPlat = getRandomItem(aggConfig.platformList);
    const platBaseConfig = aggConfig.platform[randomPlat.id];
    const platDefaultFilter = ruleFilterDef[randomPlat.id] || {};
    const defaultArea = platDefaultFilter.area || '';
    try {
      let platContentList = [];
      // 星芽推荐逻辑
      const headers = await getXingyaHeaders();
      const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}=${defaultArea}&type=1&class2_ids=0&page_num=1&page_size=10`;
      const response = await request(requestUrl, { headers });
      const res = JSON.parse(response);
      if (res && res.data && res.data.list) {
        platContentList = res.data.list.map(item => {
          const detailUrl = `${platBaseConfig.host}${platBaseConfig.url2}?theater_parent_id=${item.theater.id}`;
          return {
            vod_id: `星芽@${detailUrl}`,
            vod_name: item.theater.title || '',
            vod_pic: item.theater.cover_url || '',
            vod_remarks: `星芽短剧 | ${item.theater.total || 0}集 | 播放量:${item.theater.play_amount_str || 0}`,
            vod_content: ''
          };
        });
      }
      recommendList.push(...platContentList.slice(0, 10));
    } catch (error) {
      recommendList.push({
        vod_id: '',
        vod_name: '推荐加载失败',
        vod_pic: '',
        vod_remarks: `当前平台（${randomPlat.name}）数据获取异常，请稍后重试`,
        vod_content: ''
      });
    }
  }
  return JSON.stringify({
    list: recommendList
  });
}

// 7. 分类列表（一级分页）
async function category(tid, pg, filter, extend) {
  const videos = [];
  const page = pg || 1;
  const plat = aggConfig.platform[tid];
  const area = filter && filter.area ? filter.area : ruleFilterDef[tid]?.area || '';
  if (!plat) {
    return JSON.stringify({
      list: videos,
      page: page,
      pagecount: 1,
      limit: 0,
      total: 0
    });
  }
  // 星芽分类
  if (tid === '星芽') {
    const headers = await getXingyaHeaders();
    const url = `${plat.host}${plat.url1}=${area}&type=1&class2_ids=0&page_num=${page}&page_size=24`;
    const response = await request(url, { headers });
    const res = JSON.parse(response);
    if (res && res.data && res.data.list) {
      res.data.list.forEach(it => {
        const id = `${plat.host}${plat.url2}?theater_parent_id=${it.theater.id}`;
        videos.push({
          vod_id: `星芽@${id}`,
          vod_name: it.theater.title || '',
          vod_pic: it.theater.cover_url || '',
          vod_remarks: `${it.theater.total || 0}集`,
          vod_content: `播放量:${it.theater.play_amount_str || 0}`
        });
      });
    }
  }
  return JSON.stringify({
    list: videos,
    page: page,
    pagecount: page + 1,
    limit: videos.length,
    total: videos.length * (page + 1)
  });
}

// 8. 短剧详情（二级）
async function detail(id) {
  const parts = id.split('@');
  const platform = parts[0];
  const did = parts.slice(1).join('@');
  const plat = aggConfig.platform[platform];
  let vod = {};
  if (!plat) {
    return JSON.stringify({
      list: [{
        vod_id: id,
        vod_name: '平台不支持',
        vod_pic: '',
        vod_remarks: '该平台暂不支持',
        vod_content: '',
        vod_play_from: '',
        vod_play_url: ''
      }]
    });
  }
  // 星芽详情
  if (platform === '星芽') {
    const headers = await getXingyaHeaders();
    const response = await request(did, { headers });
    const res = JSON.parse(response);
    if (res && res.data) {
      const data = res.data;
      const playUrls = data.theaters ? 
        data.theaters.map(it => `${it.num}$${it.son_video_url}`) : [];
      vod = {
        vod_id: id,
        vod_name: data.title || '',
        vod_type: data.score || '',
        vod_pic: data.cover_url || '',
        vod_area: `收藏${data.collect_number || 0}`,
        vod_actor: `点赞${data.like_num || 0}`,
        vod_director: `评分${data.score || 0}`,
        vod_remarks: (data.desc_tags || '') + '',
        vod_content: data.introduction || '',
        vod_play_from: '星芽短剧',
        vod_play_url: playUrls.join('#')
      };
    }
  }
  return JSON.stringify({
    list: [vod]
  });
}

// 9. 播放地址解析
async function play(flag, id, flags) {
  // 星芽直接返回原播放地址，无需额外解析
  if (/星芽/.test(flag)) {
    return JSON.stringify({ parse: 0, url: id });
  }
  return JSON.stringify({ parse: 0, url: id });
}

// 10. 星芽搜索
async function search(wd, quick, pg) {
  const videos = [];
  const page = pg || 1;
  const searchLimit = aggConfig.search.limit || 20;
  const searchTimeout = aggConfig.search.timeout || 6000;
  const searchPromises = aggConfig.platformList.map(async (platform) => {
    try {
      const plat = aggConfig.platform[platform.id];
      let results = [];
      if (platform.id === '星芽') {
        const body = JSON.stringify({ text: wd });
        const response = await request(`${plat.host}${plat.search}`, { 
          method: 'POST',
          headers: await getXingyaHeaders(), 
          body: body,
          timeout: searchTimeout 
        });
        const res = JSON.parse(response);
        if (res && res.data) {
          results = res.data.theater.search_data.map(item => {
            const id = `${plat.host}${plat.url2}?theater_parent_id=${item.id}`;
            return {
              vod_id: `星芽@${id}`,
              vod_name: item.title || '',
              vod_pic: item.cover_url || '',
              vod_remarks: `星芽短剧 | ${item.total || 0}集`,
              vod_content: item.introduction || ''
            };
          });
        }
      }
      return { platform: platform.name, results };
    } catch (error) {
      return { platform: platform.name, results: [] };
    }
  });
  try {
    const searchResults = await Promise.allSettled(searchPromises);
    searchResults.forEach(result => {
      if (result.status === 'fulfilled' && result.value.results && result.value.results.length > 0) {
        videos.push(...result.value.results);
      }
    });
  } catch (error) {
  }
  const filteredResults = videos.filter(item => {
    const title = item.vod_name || '';
    return title.toLowerCase().includes(wd.toLowerCase());
  });
  return JSON.stringify({
    list: filteredResults,
    page: page,
    pagecount: page + 1,
    limit: filteredResults.length,
    total: filteredResults.length * (page + 1)
  });
}

// 导出入口函数（和原框架保持一致）
export function __jsEvalReturn() {
  return {
    init: init,
    home: home,
    homeVod: homeVod,
    category: category,
    detail: detail,
    play: play,
    proxy: null,
    search: search
  };
}
