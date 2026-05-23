/*
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '星芽短剧',
  lang: 'cat'
})
*/

import 'assets://js/lib/crypto-js.js';

const UA = 'Mozilla/5.0 (Linux; Android 9; V2196A Build/PQ3A.190705.08211809; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:416;packageName:com.jp3.xg3';

const aggConfig = {
  keys: 'd3dGiJc651gSQ8w1',
  headers: {
    default: {
      'User-Agent': 'okhttp/3.12.11',
      'content-type': 'application/json; charset=utf-8'
    }
  },
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
  ]
};

const ruleFilterDef = {
  星芽: { area: '1' }
};

const filterOptions = {
  星芽: [{
    key: "area",
    name: "分类",
    value: [
      {"n": "剧场", "v": "1"},
      {"n": "热播剧", "v": "2"},
      {"n": "会员专享", "v": "8"},
      {"n": "星选好剧", "v": "7"},
      {"n": "新剧", "v": "3"},
      {"n": "阳光剧场", "v": "5"}
    ]
  }]
};

let xingya_headers = {};

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
  } catch (e) {
    return "";
  }
}

function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c =>
    (c === 'x' ? (Math.random() * 16 | 0) : (Math.random() * 16 & 0x3 | 0x8)).toString(16)
  );
}

async function init(cfg) {
  try {
    const data = { device: '242506836G2NNdj4Vxcmgwb8RxPe35Ls7QftEqYi5' };
    const options = {
      method: 'POST',
      headers: {
        'User-Agent': 'okhttp/4.10.0',
        'platform': '1',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    };
    const res = JSON.parse(await request(aggConfig.platform.星芽.loginUrl, options));
    const token =
      res?.data?.token ||
      res?.data?.data?.token ||
      res?.token ||
      res?.result?.token ||
      res?.access_token;

    xingya_headers = token
      ? { ...aggConfig.headers.default, authorization: token }
      : aggConfig.headers.default;
  } catch (e) {
    xingya_headers = aggConfig.headers.default;
  }
  return true;
}

async function home(filter) {
  return JSON.stringify({
    class: [{ type_id: '星芽', type_name: '星芽短剧' }],
    filters: filterOptions
  });
}

async function homeVod() {
  return JSON.stringify({ list: [] });
}

async function category(tid, pg, filter, extend) {
  const page = pg || 1;
  const area = filter?.area || ruleFilterDef.星芽.area;
  const url = `${aggConfig.platform.星芽.host}${aggConfig.platform.星芽.url1}=${area}&type=1&class2_ids=0&page_num=${page}&page_size=24`;
  const res = JSON.parse(await request(url, { headers: xingya_headers }));
  const videos = [];

  if (res?.data?.list) {
    res.data.list.forEach(it => {
      const id = `${aggConfig.platform.星芽.host}${aggConfig.platform.星芽.url2}?theater_parent_id=${it.theater.id}`;
      videos.push({
        vod_id: `星芽@${id}`,
        vod_name: it.theater.title,
        vod_pic: it.theater.cover_url,
        vod_remarks: `${it.theater.total || 0}集`
      });
    });
  }

  return JSON.stringify({ list: videos, page, pagecount: page + 1 });
}

async function detail(id) {
  const realUrl = id.split('@')[1];
  const res = JSON.parse(await request(realUrl, { headers: xingya_headers }));
  const data = res?.data || {};
  const urls = (data.theaters || []).map(it => `${it.num}$${it.son_video_url}`);

  return JSON.stringify({
    list: [{
      vod_id: id,
      vod_name: data.title,
      vod_pic: data.cover_url,
      vod_content: data.introduction,
      vod_play_from: '星芽短剧',
      vod_play_url: urls.join('#')
    }]
  });
}

async function play(flag, id, flags) {
  return JSON.stringify({ parse: 0, url: id });
}

async function search(wd, quick, pg) {
  const page = pg || 1;
  const body = JSON.stringify({ text: wd });
  const res = JSON.parse(
    await request(`${aggConfig.platform.星芽.host}${aggConfig.platform.星芽.search}`, {
      method: 'POST',
      headers: xingya_headers,
      body
    })
  );

  const videos = [];
  if (res?.data?.theater?.search_data) {
    res.data.theater.search_data.forEach(it => {
      const id = `${aggConfig.platform.星芽.host}${aggConfig.platform.星芽.url2}?theater_parent_id=${it.id}`;
      videos.push({
        vod_id: `星芽@${id}`,
        vod_name: it.title,
        vod_pic: it.cover_url,
        vod_remarks: `${it.total || 0}集`
      });
    });
  }

  return JSON.stringify({ list: videos, page, pagecount: page + 1 });
}

export function __jsEvalReturn() {
  return { init, home, homeVod, category, detail, play, search };
}
