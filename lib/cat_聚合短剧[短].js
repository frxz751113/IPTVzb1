/*
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '聚合短剧[短]',
  lang: 'cat'
})
*/


import 'assets://js/lib/crypto-js.js';


const UA = 'Mozilla/5.0 (Linux; Android 9; V2196A Build/PQ3A.190705.08211809; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:416;packageName:com.jp3.xg3';
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
    },
    niuniu: {
      'Cache-Control': 'no-cache',
      'Content-Type': 'application/json;charset=UTF-8',
      'User-Agent': 'okhttp/4.12.0'
    }
  },
  platform: {
    百度: {
      host: 'https://yunzhiapi.cn',
      url1: '/API/bddjss.php?name=fyclass&page=fypage',
      url2: '/API/bddjss.php?id=fyid',
      search: '/API/bddjss.php?name=**&page=fypage'
    },
    甜圈: {
      host: 'https://mov.cenguigui.cn',
      url1: '/duanju/api.php?classname',
      url2: '/duanju/api.php?book_id',
      search: '/duanju/api.php?name'
    },
    锦鲤: {
      host: 'https://api.jinlidj.com',
      search: '/api/search',
      url2: '/api/detail'
    },
    番茄: {
      host: 'https://reading.snssdk.com',
      url1: '/reading/bookapi/bookmall/cell/change/v',
      url2: 'https://fqgo.52dns.cc/catalog',
      search: 'https://fqgo.52dns.cc/search'
    },
    星芽: {
      host: 'https://app.whjzjx.cn',
      url1: '/cloud/v2/theater/home_page?theater_class_id',
      url2: '/v2/theater_parent/detail',
      search: '/v3/search',
      loginUrl: 'https://u.shytkjgs.com/user/v1/account/login'
    },
    西饭: {
      host: 'https://xifan-api-cn.youlishipin.com',
      url1: '/xifan/drama/portalPage',
      url2: '/xifan/drama/getDuanjuInfo',
      search: '/xifan/search/getSearchList'
    },
    软鸭: {
      host: 'https://api.xingzhige.com',
      url1: '/API/playlet',
      search: '/API/playlet'
    },
    七猫: {
      host: 'https://api-store.qmplaylet.com',
      url1: '/api/v1/playlet/index',
      url2: 'https://api-read.qmplaylet.com/player/api/v1/playlet/info',
      search: '/api/v1/playlet/search'
    },
    牛牛: {
      host: 'https://new.tianjinzhitongdaohe.com',
      url1: '/api/v1/app/screen/screenMovie',
      url2: '/api/v1/app/play/movieDetails',
      search: '/api/v1/app/search/searchMovie'
    },
    围观: {
      host: 'https://api.drama.9ddm.com',
      url1: '/drama/home/shortVideoTags',
      url2: '/drama/home/shortVideoDetail',
      search: '/drama/home/search'
    },
    碎片: {
      host: 'https://free-api.bighotwind.cc',
      url1: '/papaya/papaya-api/theater/tags',
      url2: '/papaya/papaya-api/videos/info',
      search: '/papaya/papaya-api/videos/page'
    }
  },
  platformList: [
    { name: '甜圈短剧', id: '甜圈' },
    { name: '锦鲤短剧', id: '锦鲤' },
    { name: '番茄短剧', id: '番茄' },
    { name: '星芽短剧', id: '星芽' },
    { name: '西饭短剧', id: '西饭' },
    { name: '软鸭短剧', id: '软鸭' },
    { name: '七猫短剧', id: '七猫' },
    //{ name: '牛牛短剧', id: '牛牛' },
    { name: '百度短剧', id: '百度' },
    { name: '围观短剧', id: '围观' },
    { name: '碎片剧场', id: '碎片' }
  ],
  search: {
    limit: 30,
    timeout: 6000
  }
};

const ruleFilterDef = {
  百度: { area: '逆袭' },
  甜圈: { area: '推荐榜' },
  锦鲤: { area: '' },
  番茄: { area: 'videoseries_hot' },
  星芽: { area: '1' },
  西饭: { area: '' },
  软鸭: { area: '战神' },
  七猫: { area: '0' },
  牛牛: { area: '现言' },
  围观: { area: '' },
  碎片: { area: '' }
};

const filterOptions = {
  "甜圈": [{
    "key": "area",
    "name": "剧情",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "推荐榜", "v": "推荐榜"},
      {"n": "热播榜", "v": "热播榜"},
      {"n": "新书榜", "v": "新书榜"},
      {"n": "完结榜", "v": "完结榜"},
      {"n": "连载榜", "v": "连载榜"},
      {"n": "免费榜", "v": "免费榜"},
      {"n": "新剧", "v": "新剧"},
      {"n": "逆袭", "v": "逆袭"},
      {"n": "霸总", "v": "霸总"},
      {"n": "现代言情", "v": "现代言情"},
      {"n": "打脸虐渣", "v": "打脸虐渣"},
      {"n": "豪门恩怨", "v": "豪门恩怨"},
      {"n": "神豪", "v": "神豪"},
      {"n": "马甲", "v": "马甲"},
      {"n": "都市日常", "v": "都市日常"},
      {"n": "战神归来", "v": "战神归来"},
      {"n": "小人物", "v": "小人物"},
      {"n": "女性成长", "v": "女性成长"},
      {"n": "大女主", "v": "大女主"},
      {"n": "穿越", "v": "穿越"},
      {"n": "都市修仙", "v": "都市修仙"},
      {"n": "强者回归", "v": "强者回归"},
      {"n": "亲情", "v": "亲情"},
      {"n": "古装", "v": "古装"},
      {"n": "重生", "v": "重生"},
      {"n": "闪婚", "v": "闪婚"},
      {"n": "赘婿逆袭", "v": "赘婿逆袭"},
      {"n": "虐恋", "v": "虐恋"},
      {"n": "追妻", "v": "追妻"},
      {"n": "天下无敌", "v": "天下无敌"},
      {"n": "家庭伦理", "v": "家庭伦理"},
      {"n": "萌宝", "v": "萌宝"},
      {"n": "古风权谋", "v": "古风权谋"},
      {"n": "职场", "v": "职场"},
      {"n": "奇幻脑洞", "v": "奇幻脑洞"},
      {"n": "异能", "v": "异能"},
      {"n": "无敌神医", "v": "无敌神医"},
      {"n": "古风言情", "v": "古风言情"},
      {"n": "传承觉醒", "v": "传承觉醒"},
      {"n": "现言甜宠", "v": "现言甜宠"},
      {"n": "奇幻爱情", "v": "奇幻爱情"},
      {"n": "乡村", "v": "乡村"},
      {"n": "历史古代", "v": "历史古代"},
      {"n": "王妃", "v": "王妃"},
      {"n": "高手下山", "v": "高手下山"},
      {"n": "娱乐圈", "v": "娱乐圈"},
      {"n": "强强联合", "v": "强强联合"},
      {"n": "破镜重圆", "v": "破镜重圆"},
      {"n": "暗恋成真", "v": "暗恋成真"},
      {"n": "民国", "v": "民国"},
      {"n": "欢喜冤家", "v": "欢喜冤家"},
      {"n": "系统", "v": "系统"},
      {"n": "真假千金", "v": "真假千金"},
      {"n": "龙王", "v": "龙王"},
      {"n": "校园", "v": "校园"},
      {"n": "穿书", "v": "穿书"},
      {"n": "女帝", "v": "女帝"},
      {"n": "团宠", "v": "团宠"},
      {"n": "年代爱情", "v": "年代爱情"},
      {"n": "玄幻仙侠", "v": "玄幻仙侠"},
      {"n": "青梅竹马", "v": "青梅竹马"},
      {"n": "悬疑推理", "v": "悬疑推理"},
      {"n": "皇后", "v": "皇后"},
      {"n": "替身", "v": "替身"},
      {"n": "大叔", "v": "大叔"},
      {"n": "喜剧", "v": "喜剧"},
      {"n": "剧情", "v": "剧情"}
    ]
  }],
  "锦鲤": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "情感关系", "v": "1"},
      {"n": "成长逆袭", "v": "2"},
      {"n": "奇幻异能", "v": "3"},
      {"n": "战斗热血", "v": "4"},
      {"n": "伦理现实", "v": "5"},
      {"n": "时空穿越", "v": "6"},
      {"n": "权谋身份", "v": "7"}
    ]
  }],
  "番茄": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "热剧", "v": "videoseries_hot"},
      {"n": "新剧", "v": "firstonlinetime_new"},
      {"n": "逆袭", "v": "cate_739"},
      {"n": "总裁", "v": "cate_29"},
      {"n": "现言", "v": "cate_3"},
      {"n": "打脸", "v": "cate_1051"},
      {"n": "马甲", "v": "cate_266"},
      {"n": "豪门", "v": "cate_1053"},
      {"n": "都市", "v": "cate_261"},
      {"n": "神豪", "v": "cate_20"}
    ]
  }],
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
  }],
  "西饭": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "都市", "v": "68@都市"},
      {"n": "青春", "v": "68@青春"},
      {"n": "现代言情", "v": "81@现代言情"},
      {"n": "豪门", "v": "81@豪门"},
      {"n": "大女主", "v": "80@大女主"},
      {"n": "逆袭", "v": "79@逆袭"},
      {"n": "打脸虐渣", "v": "79@打脸虐渣"},
      {"n": "穿越", "v": "81@穿越"}
    ]
  }],
  "软鸭": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "战神", "v": "战神"},
      {"n": "逆袭", "v": "逆袭"},
      {"n": "霸总", "v": "霸总"},
      {"n": "神豪", "v": "神豪"},
      {"n": "都市", "v": "都市"},
      {"n": "玄幻", "v": "玄幻"},
      {"n": "言情", "v": "言情"}
    ]
  }],
  "七猫": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "推荐", "v": "0"},
      {"n": "新剧", "v": "-1"},
      {"n": "都市情感", "v": "1273"},
      {"n": "古装", "v": "1272"},
      {"n": "都市", "v": "571"},
      {"n": "玄幻仙侠", "v": "1286"},
      {"n": "奇幻", "v": "570"},
      {"n": "乡村", "v": "590"},
      {"n": "民国", "v": "573"},
      {"n": "年代", "v": "572"},
      {"n": "青春校园", "v": "1288"},
      {"n": "武侠", "v": "371"},
      {"n": "科幻", "v": "594"},
      {"n": "末世", "v": "556"},
      {"n": "二次元", "v": "1289"},
      {"n": "逆袭", "v": "400"},
      {"n": "穿越", "v": "373"},
      {"n": "复仇", "v": "795"},
      {"n": "系统", "v": "787"},
      {"n": "权谋", "v": "790"},
      {"n": "重生", "v": "784"},
      {"n": "女性成长", "v": "1294"},
      {"n": "打脸虐渣", "v": "716"},
      {"n": "闪婚", "v": "480"},
      {"n": "强者回归", "v": "402"},
      {"n": "追妻火葬场", "v": "715"},
      {"n": "家庭", "v": "670"},
      {"n": "马甲", "v": "558"},
      {"n": "职场", "v": "724"},
      {"n": "宫斗", "v": "343"},
      {"n": "高手下山", "v": "1299"},
      {"n": "娱乐明星", "v": "1295"},
      {"n": "异能", "v": "727"},
      {"n": "宅斗", "v": "342"},
      {"n": "替身", "v": "712"},
      {"n": "穿书", "v": "338"},
      {"n": "商战", "v": "723"},
      {"n": "种田经商", "v": "1291"},
      {"n": "伦理", "v": "1293"},
      {"n": "社会话题", "v": "1290"},
      {"n": "致富", "v": "492"},
      {"n": "偷听心声", "v": "1258"},
      {"n": "脑洞", "v": "526"},
      {"n": "豪门总裁", "v": "624"},
      {"n": "萌宝", "v": "356"},
      {"n": "战神", "v": "527"},
      {"n": "真假千金", "v": "812"},
      {"n": "赘婿", "v": "36"},
      {"n": "神医", "v": "1269"},
      {"n": "神豪", "v": "37"},
      {"n": "小人物", "v": "1296"},
      {"n": "团宠", "v": "545"},
      {"n": "欢喜冤家", "v": "464"},
      {"n": "女帝", "v": "617"},
      {"n": "银发", "v": "1297"},
      {"n": "兵王", "v": "28"},
      {"n": "虐恋", "v": "16"},
      {"n": "甜宠", "v": "21"},
      {"n": "悬疑", "v": "27"},
      {"n": "搞笑", "v": "793"},
      {"n": "灵异", "v": "1287"}
    ]
  }],
  "牛牛": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""},
      {"n": "现言", "v": "现言"},
      {"n": "古言", "v": "古言"},
      {"n": "玄幻", "v": "玄幻"},
      {"n": "都市", "v": "都市"},
      {"n": "科幻", "v": "科幻"},
      {"n": "悬疑", "v": "悬疑"},
      {"n": "喜剧", "v": "喜剧"}
    ]
  }],
  
  "百度": [{
    "key": "area",
    "name": "分类",
    "value": [
    {"n": "逆袭", "v": "逆袭"},
    {"n": "战神", "v": "战神"},
    {"n": "都市", "v": "都市"},
    {"n": "穿越", "v": "穿越"},
    {"n": "重生", "v": "重生"},
    {"n": "古装", "v": "古装"},
    {"n": "言情", "v": "言情"},
    {"n": "虐恋", "v": "虐恋"},
    {"n": "甜宠", "v": "甜宠"},
    {"n": "神医", "v": "神医"},
    {"n": "萌宝", "v": "萌宝"}
    ]
  }],
  "围观": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""}
    ]
  }],
  "碎片": [{
    "key": "area",
    "name": "分类",
    "value": [
      {"n": "全部", "v": ""}
    ]
  }]
};

let xingya_headers = {};

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

async function getQmParamsAndSign() {
  try {
    const sessionId = Math.floor(Date.now()).toString();
    let data = {
      "static_score": "0.8", 
      "uuid": "00000000-7fc7-08dc-0000-000000000000",
      "device-id": "20250220125449b9b8cac84c2dd3d035c9052a2572f7dd0122edde3cc42a70",
      "mac": "", 
      "sourceuid": "aa7de295aad621a6", 
      "refresh-type": "0", 
      "model": "22021211RC",
      "wlb-imei": "", 
      "client-id": "aa7de295aad621a6", 
      "brand": "Redmi", 
      "oaid": "",
      "oaid-no-cache": "", 
      "sys-ver": "12", 
      "trusted-id": "", 
      "phone-level": "H",
      "imei": "", 
      "wlb-uid": "aa7de295aad621a6", 
      "session-id": sessionId
    };
    
    const jsonStr = JSON.stringify(data);
    const base64Str = base64Encode(unescape(encodeURIComponent(jsonStr)));

    let qmParams = '';
    for (const c of base64Str) {
      qmParams += aggConfig.charMap[c] || c;
    }
    const paramsStr = `AUTHORIZATION=app-version=10001application-id=com.duoduo.readchannel=unknownis-white=net-env=5platform=androidqm-params=${qmParams}reg=${aggConfig.keys}`;
    
    const sign = await md5(paramsStr);
    return { qmParams, sign };
  } catch (e) {
    throw e;
  }
}

async function getHeaderX() {
  const { qmParams, sign } = await getQmParamsAndSign();
  return {
    'net-env': '5', 
    'reg': '', 
    'channel': 'unknown', 
    'is-white': '', 
    'platform': 'android',
    'application-id': 'com.duoduo.read', 
    'authorization': '', 
    'app-version': '10001',
    'user-agent': 'webviewversion/0', 
    'qm-params': qmParams, 
    'sign': sign
  };
}

function getRandomItem(items) {
  return items[Math.random() * items.length | 0];
}

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

//分类
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

//推荐
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

      if (randomPlat.id === '百度') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1.replace('fyclass', defaultArea).replace('fypage', '1')}`;
        const response = await request(requestUrl, { headers: aggConfig.headers.default });
        const res = JSON.parse(response);
        if (res && res.data) {
          platContentList = res.data.map(item => ({
            vod_id: `百度@${item.id}`,
            vod_name: item.title || '未知标题',
            vod_pic: item.cover || '',
            vod_remarks: `更新至${item.totalChapterNum || 0}集`,
            vod_content: `百度短剧 | ${item.title || '无简介'}`
          }));
        }
      } else if (randomPlat.id === '甜圈') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}=${defaultArea}&offset=1`;
        const response = await request(requestUrl, { headers: aggConfig.headers.default });
        const res = JSON.parse(response);
        if (res && res.data) {
          platContentList = res.data.map(item => ({
            vod_id: `甜圈@${item.book_id}`,
            vod_name: item.title || '未知标题',
            vod_pic: item.cover || '',
            vod_remarks: item.copyright || '未知',
            vod_content: `甜圈短剧 | ${item.sub_title || '无简介'}`
          }));
        }
      } else if (randomPlat.id === '锦鲤') {
        const requestBody = JSON.stringify({
          page: 1,
          limit: 10,
          type_id: defaultArea,
          year: '',
          keyword: ''
        });
        const response = await request(
          `${platBaseConfig.host}${platBaseConfig.search}`,
          { method: 'POST', body: requestBody }
        );
        const res = JSON.parse(response);
        if (res && res.data && res.data.list) {
          platContentList = res.data.list.map(item => ({
            vod_id: `锦鲤@${item.vod_id}`,
            vod_name: item.vod_name || '未知短剧',
            vod_pic: item.vod_pic || '',
            vod_remarks: `锦鲤短剧 | ${item.vod_total || 0}集`,
            vod_content: item.vod_tag || ''
          }));
        }
      } else if (randomPlat.id === '番茄') {
        const fmSessionId = new Date().toISOString().slice(0, 16).replace(/-|T:/g, '');
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?change_type=0&selected_items=${defaultArea}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${fmSessionId}`;
        const response = await request(requestUrl, { headers: aggConfig.headers.default });
        const res = JSON.parse(response);
        const fmItems = res?.data?.cell_view?.cell_data || [];
        platContentList = fmItems.map(item => {
          const videoInfo = item.video_data?.[0] || item;
          return {
            vod_id: `番茄@${videoInfo.series_id || videoInfo.book_id || ''}`,
            vod_name: videoInfo.title || '未知标题',
            vod_pic: videoInfo.cover || videoInfo.horiz_cover || '',
            vod_remarks: `番茄短剧 | ${videoInfo.sub_title || '无简介'}`,
            vod_content: ''
          };
        });
      } else if (randomPlat.id === '星芽') {
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
      } else if (randomPlat.id === '西饭') {
        const [typeId, typeName] = defaultArea.split('@');
        const ts = Math.floor(Date.now() / 1000);
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?reqType=aggregationPage&offset=0&categoryId=${typeId}&quickEngineVersion=-1&scene=&categoryNames=${encodeURIComponent(typeName)}&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTZjMWQ3NWI3ZDAiLCJpZCI6IjNiMzViZmYzYWE0OTgxNDQxNDBlZjI5N2JkMDY5NGNhIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
        const response = await request(requestUrl, { headers: aggConfig.headers.default });
        const res = JSON.parse(response);
        const xfElements = res.result.elements || [];
        platContentList = [];
        xfElements.forEach(soup => {
          soup.contents.forEach(vod => {
            const dj = vod.duanjuVo;
            platContentList.push({
              vod_id: `西饭@${dj.duanjuId}#${dj.source}`,
              vod_name: dj.title || '',
              vod_pic: dj.coverImageUrl || '',
              vod_remarks: `西饭短剧 | ${dj.total || 0}集`,
              vod_content: ''
            });
          });
        });
      } else if (randomPlat.id === '软鸭') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}/?keyword=${encodeURIComponent(defaultArea)}&page=1`;
        const response = await request(requestUrl, { headers: aggConfig.headers.default });
        const res = JSON.parse(response);
        if (res && res.data) {
          platContentList = res.data.map(item => {
            const purl = `${item.title}@${item.cover}@${item.author}@${item.type}@${item.desc}@${item.book_id}`;
            return {
              vod_id: `软鸭@${encodeURIComponent(purl)}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.cover || '',
              vod_remarks: `软鸭短剧 | ${item.type || '无分类'}`,
              vod_content: ''
            };
          });
        }
      } else if (randomPlat.id === '七猫') {
        let signStr = `operation=1playlet_privacy=1tag_id=${defaultArea}${aggConfig.keys}`;
        const sign = await md5(signStr);
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?tag_id=${defaultArea}&playlet_privacy=1&operation=1&sign=${sign}`;
        const headers = { ...await getHeaderX(), ...aggConfig.headers.default };
        const response = await request(requestUrl, { method: 'GET', headers });
        const res = JSON.parse(response);
        platContentList = (res?.data?.list || []).map(item => ({
          vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
          vod_name: item.title || '未知标题',
          vod_pic: item.image_link || '',
          vod_remarks: `七猫短剧 | ${item.tags || ''} ${item.total_episode_num || 0}集`,
          vod_content: ''
        }));
      } else if (randomPlat.id === '牛牛') {
        const requestBody = JSON.stringify({
          condition: { classify: defaultArea, typeId: 'S1' },
          pageNum: '1',
          pageSize: 10
        });
        const response = await request(
          `${platBaseConfig.host}${platBaseConfig.url1}`,
          { method: 'POST', headers: aggConfig.headers.niuniu, body: requestBody }
        );
        console.log(`✅[response]: ${response}`);
        const res = JSON.parse(response);
        platContentList = (res.data?.records || []).map(item => ({
          vod_id: `牛牛@${item.id}`,
          vod_name: item.name || '',
          vod_pic: item.cover || '',
          vod_remarks: `牛牛短剧 | ${item.totalEpisode || 0}集`,
          vod_content: ''
        }));
      } else if (randomPlat.id === '围观') {
        const postData = JSON.stringify({
          "audience": "",
          "page": 1,
          "pageSize": 10,
          "searchWord": "",
          "subject": ""
        });
        const response = await request(
          `${platBaseConfig.host}${platBaseConfig.search}`,
          { method: 'POST', body: postData }
        );
        const res = JSON.parse(response);
        if (res && res.data) {
          platContentList = res.data.map(it => ({
            vod_id: `围观@${it.oneId}`,
            vod_name: it.title || '',
            vod_pic: it.vertPoster || '',
            vod_remarks: `围观短剧 | 集数:${it.episodeCount || 0} 播放:${it.viewCount || 0}`,
            vod_content: it.description || ''
          }));
        }
      } else if (randomPlat.id === '碎片') {
        let openId = (await md5(guid())).substring(0, 16);
        let api = "https://free-api.bighotwind.cc/papaya/papaya-api/oauth2/uuid";
        let body = JSON.stringify({ "openId": openId });
        let key = encHex(Date.now().toString());
        
        const tokenResponse = await request(api, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            "key": key
          },
          body: body
        });
        
        const tokenRes = JSON.parse(tokenResponse);
        if (tokenRes && tokenRes.data && tokenRes.data.token) {
          const headers = { ...aggConfig.headers.default, 'Authorization': tokenRes.data.token };
          const requestUrl = `${platBaseConfig.host}${platBaseConfig.search}?type=5&tagId=&pageNum=1&pageSize=10`;
          const response = await request(requestUrl, { headers });
          const res = JSON.parse(response);
          
          if (res && res.list) {
            platContentList = res.list.map(it => {
              let compoundId = it.itemId + '@' + it.videoCode;
              return {
                vod_id: `碎片@${compoundId}`,
                vod_name: it.title || '',
                vod_pic: "https://speed.howdbm.com/papaya/papaya-file/files/download/" + it.imageKey + "/" + it.imageName,
                vod_remarks: `碎片剧场 | 集数:${it.episodesMax || 0} 播放:${it.hitShowNum || 0}`,
                vod_content: it.content || it.description || ''
              };
            });
          }
        }
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

async function getXingyaHeaders() {
  if (xingya_headers && xingya_headers.authorization) {
    return xingya_headers;
  }
  return aggConfig.headers.default;
}

//一级
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

  switch (tid) {
    case '百度': {
      const url = `${plat.host}${plat.url1.replace('fyclass', area).replace('fypage', page)}`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `百度@${it.id}`,
            vod_name: it.title || '未知标题',
            vod_pic: it.cover || '',
            vod_remarks: `更新至${it.totalChapterNum || 0}集`
          });
        });
      }
      break;
    }
    case '甜圈': {
      const url = `${plat.host}${plat.url1}=${area}&offset=${page}`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `甜圈@${it.book_id}`,
            vod_name: it.title || '未知标题',
            vod_pic: it.cover || '',
            vod_remarks: it.copyright || ''
          });
        });
      }
      break;
    }
    case '锦鲤': {
      const body = JSON.stringify({ page: page, limit: 24, type_id: area, year: '', keyword: '' });
      const response = await request(plat.host + plat.search, { method: 'POST', body });
      const res = JSON.parse(response);
      if (res && res.data && res.data.list) {
        res.data.list.forEach(item => {
          videos.push({
            vod_id: `锦鲤@${item.vod_id}`,
            vod_name: item.vod_name || '',
            vod_pic: item.vod_pic || '',
            vod_remarks: `${item.vod_total || 0}集`,
            vod_content: item.vod_tag || ''
          });
        });
      }
      break;
    }
    case '番茄': {
      const sessionId = new Date().toISOString().slice(0, 16).replace(/-|T:/g, '');
      let url = `${plat.host}${plat.url1}?change_type=0&selected_items=${area}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${sessionId}`;
      if (page > 1) url += `&offset=${(page - 1) * 12}`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      
      let items = [];
      if (res?.data?.cell_view?.cell_data) items = res.data.cell_view.cell_data;
      else if (res?.search_tabs) items = res.search_tabs.find(t => t.title === '短剧' && t.data)?.data || [];
      else if (Array.isArray(res?.data)) items = res.data;
      else if (res?.data) items = [res.data];
      else items = [res || {}];

      items.forEach(item => {
        const videoData = item.video_data?.[0] || item;
        videos.push({
          vod_id: `番茄@${videoData.series_id || videoData.book_id || videoData.id || ''}`,
          vod_name: videoData.title || '未知短剧',
          vod_pic: videoData.cover || videoData.horiz_cover || '',
          vod_remarks: videoData.sub_title || videoData.rec_text || ''
        });
      });
      break;
    }
    case '星芽': {
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
      break;
    }
    case '西饭': {
      const [typeId, typeName] = area.split('@');
      const ts = Math.floor(Date.now() / 1000);
      const url = `${plat.host}${plat.url1}?reqType=aggregationPage&offset=${(page - 1) * 30}&categoryId=${typeId}&quickEngineVersion=-1&scene=&categoryNames=${encodeURIComponent(typeName)}&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTY2YzFkNzViN2QwIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      if (res && res.result && res.result.elements) {
        res.result.elements.forEach(soup => {
          soup.contents.forEach(vod => {
            const dj = vod.duanjuVo;
            videos.push({
              vod_id: `西饭@${dj.duanjuId}#${dj.source}`,
              vod_name: dj.title || '',
              vod_pic: dj.coverImageUrl || '',
              vod_remarks: `${dj.total || 0}集`
            });
          });
        });
      }
      break;
    }
    case '软鸭': {
      const url = `${plat.host}${plat.url1}/?keyword=${encodeURIComponent(area)}&page=${page}`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      if (res && res.data) {
        res.data.forEach(item => {
          const purl = `${item.title}@${item.cover}@${item.author}@${item.type}@${item.desc}@${item.book_id}`;
          videos.push({
            vod_id: `软鸭@${encodeURIComponent(purl)}`,
            vod_name: item.title || '',
            vod_pic: item.cover || '',
            vod_remarks: item.type || '',
            vod_content: item.author || ''
          });
        });
      }
      break;
    }
    case '七猫': {
      let signStr = `operation=1playlet_privacy=1tag_id=${area}${aggConfig.keys}`;
      const sign = await md5(signStr);
      const url = `${plat.host}${plat.url1}?tag_id=${area}&playlet_privacy=1&operation=1&sign=${sign}`;
      const headers = { ...await getHeaderX(), ...aggConfig.headers.default };
      const response = await request(url, { method: 'GET', headers });
      const res = JSON.parse(response);
      if (res?.data?.list) {
        (res.data.list || []).forEach(item => {
          videos.push({
            vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
            vod_name: item.title || '',
            vod_pic: item.image_link || '',
            vod_remarks: `${item.total_episode_num || 0}集`,
            vod_content: item.tags || ''
          });
        });
      }
      break;
    }
    case '牛牛': {
      const body = JSON.stringify({
        condition: { classify: area, typeId: 'S1' },
        pageNum: page,
        pageSize: 24
      });
      console.log(`✅[input]: ${plat.host + plat.url1}`);
      console.log(`✅[aggConfig.headers.niuniu的结果: ]${JSON.stringify(aggConfig.headers.niuniu, null, 4)}`);
      console.log(`✅[body的结果: ]${JSON.stringify(body, null, 4)}`);
      const response = await request(plat.host + plat.url1, { method: 'POST', headers: aggConfig.headers.niuniu, body });
      console.log(`✅[response的结果: ]${JSON.stringify(response, null, 4)}`);
      const res = JSON.parse(response);
      if (res.data?.records) {
        (res.data.records || []).forEach(item => {
          videos.push({
            vod_id: `牛牛@${item.id}`,
            vod_name: item.name || '',
            vod_pic: item.cover || '',
            vod_remarks: `${item.totalEpisode || 0}集`,
            vod_content: ''
          });
        });
      }
      break;
    }
    case '围观': {
      const postData = JSON.stringify({
        "audience": "全部受众",
        "page": page,
        "pageSize": 30,
        "searchWord": "",
        "subject": "全部主题"
      });
      const response = await request(`${plat.host}${plat.search}`, { 
        method: 'POST', 
        headers: aggConfig.headers.default, 
        body: postData 
      });
      const res = JSON.parse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `围观@${it.oneId}`,
            vod_name: it.title || '',
            vod_pic: it.vertPoster || '',
            vod_remarks: `集数:${it.episodeCount || 0} 播放:${it.viewCount || 0}`,
            vod_content: it.description || ''
          });
        });
      }
      break;
    }
    case '碎片': {
      let openId = (await md5(guid())).substring(0, 16);
      let api = "https://free-api.bighotwind.cc/papaya/papaya-api/oauth2/uuid";
      let body = JSON.stringify({ "openId": openId });
      let key = encHex(Date.now().toString());
      
      const tokenResponse = await request(api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "key": key
        },
        body: body
      });
      
      const tokenRes = JSON.parse(tokenResponse);
      if (tokenRes && tokenRes.data && tokenRes.data.token) {
        const headers = { ...aggConfig.headers.default, 'Authorization': tokenRes.data.token };
        const requestUrl = `${plat.host}${plat.search}?type=5&tagId=&pageNum=${page}&pageSize=24`;
        const response = await request(requestUrl, { headers });
        const res = JSON.parse(response);
        if (res && res.list) {
          res.list.forEach(it => {
            let compoundId = it.itemId + '@' + it.videoCode;
            videos.push({
              vod_id: `碎片@${compoundId}`,
              vod_name: it.title || '',
              vod_pic: "https://speed.howdbm.com/papaya/papaya-file/files/download/" + it.imageKey + "/" + it.imageName,
              vod_remarks: `集数:${it.episodesMax || 0} 播放:${it.hitShowNum || 0}`,
              vod_content: it.content || it.description || ''
            });
          });
        }
      }
      break;
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

//二级
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

  switch (platform) {
    case '百度': {
      const response = await request(`${plat.host}${plat.url2.replace('fyid', did)}`);
      const res = JSON.parse(response);
      if (res) {
        vod = {
          vod_id: id,
          vod_name: res.title || '未知标题',
          vod_pic: res.data?.[0]?.cover || '',
          vod_remarks: `更新至:${res.total || 0}集`,
          vod_content: '',
          vod_play_from: '百度短剧',
          vod_play_url: res.data ? res.data.map(item => `${item.title}$${item.video_id}`).join("#") : ''
        };
      }
      break;
    }
    case '甜圈': {
      const response = await request(`${plat.host}${plat.url2}=${did}`);
      const res = JSON.parse(response);
      if (res) {
        vod = {
          vod_id: id,
          vod_name: res.book_name || '未知标题',
          vod_type: res.category || '',
          vod_pic: res.book_pic || '',
          vod_remarks: res.duration || '',
          vod_year: `更新时间:${res.time || '未知'}`,
          vod_actor: res.author || '',
          vod_content: res.desc || '',
          vod_play_from: '甜圈短剧',
          vod_play_url: res.data && Array.isArray(res.data) 
            ? res.data.map(item => `${item.title || '第1集'}$${item.video_id || item.id || ''}`).join('#')
            : ''
        };
      }
      break;
    }
    case '锦鲤': {
      const response = await request(`${plat.host}${plat.url2}/${did}`);
      const res = JSON.parse(response);
      if (res && res.data) {
        const list = res.data;
        const playUrls = list.player ? Object.keys(list.player).map(key => `${key}$${list.player[key]}`) : [];
        vod = {
          vod_id: list.vod_id || '暂无id',
          vod_name: list.vod_name || '暂无名称',
          vod_type: list.vod_class || '暂无类型',
          vod_pic: list.vod_pic || '暂无图片',
          vod_remarks: list.vod_remarks || '暂无备注',
          vod_year: list.vod_year || '暂无年份',
          vod_area: list.vod_area || '暂无地区',
          vod_actor: list.vod_actor || '暂无演员',
          vod_director: list.vod_director || '暂无导演',
          vod_content: list.vod_blurb || '暂无剧情',
          vod_play_from: '锦鲤短剧',
          vod_play_url: playUrls.join('#')
        };
      }
      break;
    }
    case '番茄': {
      const response = await request(`${plat.url2}?book_id=${did}`);
      const res = JSON.parse(response);
      if (res && res.data) {
        const bookInfo = res.data.book_info;
        const playList = res.data.item_data_list ? 
          res.data.item_data_list.map(item => `${item.title}$${item.item_id}`).join('#') : '';
        vod = {
          vod_id: bookInfo.book_id || '',
          vod_name: bookInfo.book_name || '',
          vod_type: bookInfo.tags || '',
          vod_year: bookInfo.create_time || '',
          vod_pic: bookInfo.thumb_url || bookInfo.audio_thumb_uri || '',
          vod_content: bookInfo.abstract || bookInfo.book_abstract_v2 || '',
          vod_remarks: bookInfo.sub_info || `更新至${res.data.item_data_list?.length || 0}集`,
          vod_play_from: '番茄短剧',
          vod_play_url: playList
        };
      }
      break;
    }
    case '星芽': {
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
      break;
    }
    case '西饭': {
      const [duanjuId, source] = did.split('#');
      const url = `${plat.host}${plat.url2}?duanjuId=${duanjuId}&source=${source}&openFrom=homescreen&type=&pageID=page_inner_flow&density=1.5&version=2001001&androidVersionCode=28&requestId=1740658944980aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BH_1FlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk4LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTY2YzFkNzViN2QwIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
      const response = await request(url, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      if (res && res.result) {
        const data = res.result;
        const playUrls = data.episodeList ? 
          data.episodeList.map(ep => `${ep.index}$${ep.playUrl}`) : [];
        vod = {
          vod_id: id,
          vod_name: data.title || '',
          vod_pic: data.coverImageUrl || '',
          vod_content: data.desc || '未知',
          vod_remarks: data.updateStatus === 'over' ? `${data.total || 0}集 已完结` : `更新${data.total || 0}集`,
          vod_play_from: '西饭短剧',
          vod_play_url: playUrls.join('#')
        };
      }
      break;
    }
    case '软鸭': {
      const didDecoded = decodeURIComponent(did);
      const [title, img, author, type, desc, book_id] = didDecoded.split('@');
      const detailUrl = `${plat.host}${plat.url1}/?book_id=${book_id || did.split('@')[5]}`;
      const response = await request(detailUrl, { headers: aggConfig.headers.default });
      const res = JSON.parse(response);
      const playUrls = (res.data?.video_list || []).map(ep => `${ep.title}$${ep.video_id}`).join('#');
      vod = {
        vod_id: id,
        vod_name: title || '',
        vod_pic: img || '',
        vod_actor: author || '',
        vod_remarks: type || '',
        vod_content: desc || '',
        vod_play_from: '软鸭短剧',
        vod_play_url: playUrls
      };
      break;
    }
    case '七猫': {
      const didDecoded = decodeURIComponent(did);
      const sign = await md5(`playlet_id=${didDecoded}${aggConfig.keys}`);
      const url = `${plat.url2}?playlet_id=${didDecoded}&sign=${sign}`;
      const headers = { ...await getHeaderX(), ...aggConfig.headers.default };
      const response = await request(url, { method: 'GET', headers });
      const res = JSON.parse(response);
      if (res && res.data) {
        const data = res.data;
        vod = {
          vod_id: id,
          vod_name: data.title || '未知标题',
          vod_pic: data.image_link || '未知图片',
          vod_actor: '',
          vod_remarks: `${data.tags || ''} ${data.total_episode_num || 0}集`,
          vod_content: data.intro || '未知剧情',
          vod_play_from: '七猫短剧',
          vod_play_url: data.play_list ? data.play_list.map(it => `${it.sort}$${it.video_url}`).join('#') : ''
        };
      }
      break;
    }
    case '牛牛': {
      const body = JSON.stringify({ id: did, source: 0, typeId: 'S1', userId: '223664' });
      const response = await request(plat.host + plat.url2, {
        method: 'POST',
        headers: aggConfig.headers.niuniu,
        body
      });
      const res = JSON.parse(response);
      const data = res.data || {};
      const playUrls = (data.episodeList || []).map(ep => `${ep.episode}$${did}@${ep.id}`);
      
      vod = {
        vod_id: id,
        vod_name: data.name || '未知名称',
        vod_pic: data.cover || '',
        vod_content: data.introduce || '暂无剧情',
        vod_play_from: '牛牛短剧',
        vod_play_url: playUrls.join('#') || '暂无播放地址$0'
      };
      break;
    }
    case '围观': {
      const response = await request(
        `${plat.host}${plat.url2}?oneId=${did}&page=1&pageSize=1000`,
        { headers: aggConfig.headers.default }
      );
      const res = JSON.parse(response);
      if (res && res.data && res.data.length > 0) {
        const data = res.data;
        const firstEpisode = data[0];
        vod = {
          vod_id: id,
          vod_name: firstEpisode.title || '',
          vod_pic: firstEpisode.vertPoster || '',
          vod_remarks: `共${data.length || 0}集`,
          vod_content: `播放量:${firstEpisode.collectionCount || 0} 评论:${firstEpisode.commentCount || 0}`,
          vod_play_from: '围观短剧',
          vod_play_url: data.map(episode => {
            return `${episode.title}第${episode.playOrder || 1}集$${episode.playSetting || ''}`;
          }).join('#')
        };
      }
      break;
    }
    case '碎片': {
      const [itemId, videoCode] = did.split('@');
      
      let openId = (await md5(guid())).substring(0, 16);
      let api = "https://free-api.bighotwind.cc/papaya/papaya-api/oauth2/uuid";
      let body = JSON.stringify({ "openId": openId });
      let key = encHex(Date.now().toString());
      
      const tokenResponse = await request(api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "key": key
        },
        body: body
      });
      
      const tokenRes = JSON.parse(tokenResponse);
      if (tokenRes && tokenRes.data && tokenRes.data.token) {
        const headers = { ...aggConfig.headers.default, 'Authorization': tokenRes.data.token };
        const requestUrl = `${plat.host}${plat.url2}?videoCode=${videoCode}&itemId=${itemId}`;
        const response = await request(requestUrl, { headers });
        const res = JSON.parse(response);
        if (res) {
          const data = res.data || res;
          vod = {
            vod_id: id,
            vod_name: data.title || '',
            vod_pic: "https://speed.howdbm.com/papaya/papaya-file/files/download/" + (data.imageKey || '') + "/" + (data.imageName || ''),
            vod_remarks: `共${data.episodesMax || 0}集`,
            vod_content: data.content || data.description || `播放量:${data.hitShowNum || 0} 点赞:${data.likeNum || 0}`,
            vod_play_from: '碎片剧场',
            vod_play_url: (data.episodesList || []).map(episode => {
              let episodeTitle = `第${episode.episodes || 1}集`;
              let playUrl = "";

              if (episode.resolutionList && episode.resolutionList.length > 0) {
                episode.resolutionList.sort((a, b) => b.resolution - a.resolution);
                let bestResolution = episode.resolutionList[0];
                playUrl = `https://speed.howdbm.com/papaya/papaya-file/files/download/${bestResolution.fileKey}/${bestResolution.fileName}`;
              }
              return playUrl ? `${episodeTitle}$${playUrl}` : null;
            }).filter(item => item !== null).join('#')
          };
        }
      }
      break;
    }
  }

  return JSON.stringify({
    list: [vod]
  });
}
//播放
async function play(flag, id, flags) {
  if (/百度/.test(flag)) {
    const response = await request(`https://yunzhiapi.cn/API/bddjss.php?video_id=${id}`);
    const item = JSON.parse(response);
    if (item && item.data && item.data.qualities) {
      let qualities = item.data.qualities;
      let urls = [];

      const qualityOrder = ["1080p", "sc", "sd"];
      const qualityNames = {
        "1080p": "蓝光",
        "sc": "超清",
        "sd": "标清"
      };

      qualityOrder.forEach(qualityKey => {
        let quality = qualities.find(q => q.quality === qualityKey);
        if (quality) {
          urls.push(qualityNames[qualityKey], quality.download_url);
        }
      });

      return JSON.stringify({
        parse: 0,
        url: urls
      });
    }
  }
  if (/甜圈/.test(flag)) {
    return JSON.stringify({ 
      parse: 0, 
      url: `https://mov.cenguigui.cn/duanju/api.php?video_id=${id}&type=mp4` 
    });
  }
  if (/锦鲤/.test(flag)) {
    const url = `${id}&auto=1`;
    try {
      const response = await request(`${url}`);
      const html = response;
      const match = html.match(/let data\s*=\s*({[^;]*});/);
      if (match) {
        const data = JSON.parse(match[1]);
        return JSON.stringify({ parse: 0, url: data.url });
      }
    } catch (error) {
    }
  }
  if (/番茄/.test(flag)) {
    const response = await request(`https://fqgo.52dns.cc/video?item_ids=${id}`, { headers: aggConfig.headers.default });
    const res = JSON.parse(response);
    if (res && res.data && res.data[id]) {
      const videoModel = JSON.parse(res.data[id].video_model);
      const url = videoModel?.video_list?.video_1 ? base64Decode(videoModel.video_list.video_1.main_url) : '';
      return JSON.stringify({ parse: 0, url });
    }
  }
  if (/软鸭/.test(flag)) {
    const response = await request(`${aggConfig.platform.软鸭.host}/API/playlet/?video_id=${id}&quality=1080p`, { headers: aggConfig.headers.default });
    const res = JSON.parse(response);
    return JSON.stringify({ parse: 0, url: res.data?.video?.url || '' });
  }
  if (/牛牛/.test(flag)) {
    const [videoId, episodeId] = id.split('@');
    const body = JSON.stringify({ episodeId, id: videoId, source: 0, typeId: 'S1', userId: '223664' });
    const response = await request(`${aggConfig.platform.牛牛.host}/api/v1/app/play/movieDetails`, {
      method: 'POST',
      headers: aggConfig.headers.niuniu,
      body
    });
    const res = JSON.parse(response);
    return JSON.stringify({
      parse: 0,
      url: res.data?.url || '',
      header: { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36' }
    });
  }
  if (/围观/.test(flag)) {
    let playSetting;
    try {
      playSetting = typeof id === 'string' ? JSON.parse(id) : id;
    } catch (e) {
      return JSON.stringify({ parse: 0, url: id });
    }
    let urls = [];
    if (playSetting.super) {
      urls.push("超清", playSetting.super);
    }
    if (playSetting.high) {
      urls.push("高清", playSetting.high);
    }
    if (playSetting.normal) {
      urls.push("流畅", playSetting.normal);
    }
    return JSON.stringify({ parse: 0, url: urls });
  }
  return JSON.stringify({ parse: 0, url: id });
}

//搜索
async function search(wd, quick, pg) {
  const videos = [];
  const page = pg || 1;
  const searchLimit = aggConfig.search.limit || 20;
  const searchTimeout = aggConfig.search.timeout || 6000;

  const searchPromises = aggConfig.platformList.map(async (platform) => {
    try {
      const plat = aggConfig.platform[platform.id];
      let results = [];

      switch (platform.id) {
        case '百度': {
          const url = `${plat.host}${plat.search.replace('**', encodeURIComponent(wd)).replace('fypage', page)}`;
          const response = await request(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data) {
            results = res.data.map(item => ({
              vod_id: `百度@${item.id}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.cover || '',
              vod_remarks: `更新至${item.totalChapterNum || 0}集`,
              vod_content: `百度短剧 | ${item.title || '无简介'}`
            }));
          }
          break;
        }
        case '甜圈': {
          const url = `${plat.host}${plat.search}=${encodeURIComponent(wd)}&offset=${page}`;
          const response = await request(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data) {
            results = res.data.map(item => ({
              vod_id: `甜圈@${item.book_id}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.cover || '',
              vod_remarks: item.copyright || '未知',
              vod_content: `甜圈短剧 | ${item.sub_title || '无简介'}`
            }));
          }
          break;
        }
        case '锦鲤': {
          const body = JSON.stringify({ page: page, limit: searchLimit, type_id: '', year: '', keyword: wd });
          const response = await request(plat.host + plat.search, { method: 'POST', body, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data && res.data.list) {
            results = res.data.list.map(item => ({
              vod_id: `锦鲤@${item.vod_id}`,
              vod_name: item.vod_name || '未知短剧',
              vod_pic: item.vod_pic || '',
              vod_remarks: `锦鲤短剧 | ${item.vod_total || 0}集`,
              vod_content: ''
            }));
          }
          break;
        }
        case '番茄': {
          const url = `${plat.search}?keyword=${encodeURIComponent(wd)}&page=${page}`;
          const response = await request(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data && Array.isArray(res.data)) {
            results = res.data.map(item => ({
              vod_id: `番茄@${item.series_id || ''}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.cover || '',
              vod_remarks: `番茄短剧 | ${item.sub_title || '未知'}`,
              vod_content: ''
            }));
          }
          break;
        }
        case '星芽': {
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
          break;
        }
        case '西饭': {
          const ts = Math.floor(Date.now() / 1000);
          const url = `${plat.host}${plat.search}?reqType=search&offset=${(page - 1) * searchLimit}&keyword=${encodeURIComponent(wd)}&quickEngineVersion=-1&scene=&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciIowiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTZjMWQ3NWI3ZDAiLCJpZCI6IjNiMzViZmYzYWE0OTgxNDQxNDBlZjI5N2JkMDY5NGNhIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
          const response = await request(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.result && res.result.elements) {
            results = res.result.elements.map(vod => {
              const dj = vod.duanjuVo || {};
              return {
                vod_id: `西饭@${dj.duanjuId || ''}#${dj.source || ''}`,
                vod_name: dj.title || '未知标题',
                vod_pic: dj.coverImageUrl || '',
                vod_remarks: `西饭短剧 | ${dj.total || 0}集`,
                vod_content: ''
              };
            });
          }
          break;
        }
        case '软鸭': {
          const url = `${plat.host}${plat.search}/?keyword=${encodeURIComponent(wd)}&page=${page}`;
          const response = await request(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data) {
            results = res.data.map(item => {
              const purl = `${item.title}@${item.cover}@${item.author}@${item.type}@${item.desc}@${item.book_id}`;
              return {
                vod_id: `软鸭@${encodeURIComponent(purl)}`,
                vod_name: item.title || '',
                vod_pic: item.cover || '',
                vod_remarks: `软鸭短剧 | ${item.type || '无分类'}`,
                vod_content: ''
              };
            });
          }
          break;
        }
        case '七猫': {
          let signStr = `operation=2playlet_privacy=1search_word=${wd}${aggConfig.keys}`;
          const sign = await md5(signStr);
          const url = `${plat.host}${plat.search}?search_word=${encodeURIComponent(wd)}&playlet_privacy=1&operation=2&sign=${sign}`;
          const headers = { ...await getHeaderX(), ...aggConfig.headers.default };
          const response = await request(url, { method: 'GET', headers, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data && res.data.list) {
            results = res.data.list.map(item => ({
              vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.image_link || '',
              vod_remarks: `七猫短剧 | ${item.tags || ''} ${item.total_episode_num || 0}集`,
              vod_content: ''
            }));
          }
          break;
        }
        case '牛牛': {
          const body = JSON.stringify({
            condition: { name: wd, typeId: 'S1' },
            pageNum: page,
            pageSize: searchLimit
          });
          const response = await request(plat.host + plat.search, { method: 'POST', headers: aggConfig.headers.niuniu, body, timeout: searchTimeout });
          const res = JSON.parse(response);
          if (res && res.data && res.data.records) {
            results = res.data.records.map(item => ({
              vod_id: `牛牛@${item.id}`,
              vod_name: item.name || '',
              vod_pic: item.cover || '',
              vod_remarks: `牛牛短剧 | ${item.totalEpisode || 0}集`,
              vod_content: ''
            }));
          }
          break;
        }
        case '围观': {
          const postData = JSON.stringify({
            "audience": "",
            "page": page,
            "pageSize": searchLimit,
            "searchWord": wd,
            "subject": ""
          });
          const response = await request(
            `${plat.host}${plat.search}`,
            { method: 'POST', body: postData, timeout: searchTimeout }
          );
          const res = JSON.parse(response);
          if (res && res.data && Array.isArray(res.data)) {
            results = res.data.map(it => ({
              vod_id: `围观@${it.oneId || ''}`,
              vod_name: it.title || '未知标题',
              vod_pic: it.vertPoster || '',
              vod_remarks: `围观短剧 | 集数:${it.episodeCount || 0} 播放:${it.viewCount || 0}`,
              vod_content: it.description || ''
            }));
          }
          break;
        }
        case '碎片': {
          let openId = (await md5(guid())).substring(0, 16);
          let api = "https://free-api.bighotwind.cc/papaya/papaya-api/oauth2/uuid";
          let body = JSON.stringify({ "openId": openId });
          let key = encHex(Date.now().toString());
          
          const tokenResponse = await request(api, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              "key": key
            },
            body: body,
            timeout: searchTimeout
          });
          
          const tokenRes = JSON.parse(tokenResponse);
          if (tokenRes && tokenRes.data && tokenRes.data.token) {
            const headers = { ...aggConfig.headers.default, 'Authorization': tokenRes.data.token };
            const requestUrl = `${plat.host}${plat.search}?type=5&tagId=&pageNum=${page}&pageSize=${searchLimit}&title=${encodeURIComponent(wd)}`;
            const response = await request(requestUrl, { headers, timeout: searchTimeout });
            const res = JSON.parse(response);
            
            if (res && res.list) {
              results = res.list.map(it => {
                let compoundId = (it.itemId || '') + '@' + (it.videoCode || '');
                return {
                  vod_id: `碎片@${compoundId}`,
                  vod_name: it.title || '',
                  vod_pic: "https://speed.howdbm.com/papaya/papaya-file/files/download/" + (it.imageKey || '') + "/" + (it.imageName || ''),
                  vod_remarks: `碎片剧场 | 集数:${it.episodesMax || 0} 播放:${it.hitShowNum || 0}`,
                  vod_content: it.content || it.description || ''
                };
              });
            }
          }
          break;
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