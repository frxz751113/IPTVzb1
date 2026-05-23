/*
@header({
  name: '星芽短剧',
  version: '1.0',
  type: 3,
  searchable: 1,
  quickSearch: 1,
  filterable: 1
})
*/

/// === import start ===
import 'assets://js/lib/crypto-js.js';
/// === import end ===

/// === global config ===
const HOST = 'https://app.whjzjx.cn';
const LOGIN_URL = 'https://u.shytkjgs.com/user/v1/account/login';
const DETAIL_PATH = '/v2/theater_parent/detail';
const LIST_PATH = '/cloud/v2/theater/home_page';

let TOKEN = '';
let HEADERS = {
  'User-Agent': 'okhttp/3.12.11',
  'Content-Type': 'application/json; charset=utf-8'
};

/// === utils ===
async function req(url, opt = {}) {
  return await fetch(url, {
    method: opt.method || 'GET',
    headers: opt.headers || HEADERS,
    body: opt.body ? JSON.stringify(opt.body) : undefined
  }).then(r => r.text());
}

async function md5(str) {
  return CryptoJS.MD5(str).toString(CryptoJS.enc.Hex);
}

/// === init（登录拿 token）===
async function init(cfg) {
  try {
    const body = {
      device: '242506832wEedY4qWiT9to1EZCFXmw48e63XVy6oW'
    };

    const res = JSON.parse(
      await req(LOGIN_URL, {
        method: 'POST',
        headers: {
          'User-Agent': 'okhttp/4.10.0',
          'platform': '1',
          'Content-Type': 'application/json'
        },
        body
      })
    );

    TOKEN =
      res?.data?.token ||
      res?.data?.data?.token ||
      res?.token ||
      res?.access_token ||
      '';

    if (TOKEN) {
      HEADERS.Authorization = TOKEN;
    }
  } catch (e) {
    TOKEN = '';
  }
  return true;
}

/// === home（分类）===
async function home(filter) {
  return JSON.stringify({
    class: [
      { type_id: '1', type_name: '剧场' },
      { type_id: '2', type_name: '热播剧' },
      { type_id: '8', type_name: '会员专享' },
      { type_id: '7', type_name: '星选好剧' },
      { type_id: '3', type_name: '新剧' },
      { type_id: '5', type_name: '阳光剧场' }
    ],
    filters: {
      1: [{ key: 'area', name: '分类', value: [{ n: '全部', v: '' }] }]
    }
  });
}

/// === category（列表）===
async function category(tid, pg, filter, extend) {
  const page = pg || 1;
  const area = filter?.area || tid || '1';
  const url = `${HOST}${LIST_PATH}?theater_class_id=${area}&type=1&class2_ids=0&page_num=${page}&page_size=24`;

  const res = JSON.parse(await req(url));
  const videos = [];

  if (res?.data?.list) {
    res.data.list.forEach(it => {
      videos.push({
        vod_id: `${HOST}${DETAIL_PATH}?theater_parent_id=${it.theater.id}`,
        vod_name: it.theater.title,
        vod_pic: it.theater.cover_url,
        vod_remarks: `${it.theater.total || 0}集`,
        vod_content: `播放量:${it.theater.play_amount_str || 0}`
      });
    });
  }

  return JSON.stringify({
    list: videos,
    page,
    pagecount: page + 1
  });
}

/// === detail（详情 + 播放）===
async function detail(ids) {
  const url = ids[0];
  const res = JSON.parse(await req(url));
  const data = res?.data || {};

  const urls = (data.theaters || []).map(
    ep => `${ep.num}$${ep.son_video_url}`
  );

  return JSON.stringify({
    list: [{
      vod_id: url,
      vod_name: data.title || '',
      vod_pic: data.cover_url || '',
      vod_remarks: `${data.theaters?.length || 0}集`,
      vod_content: data.introduction || '',
      vod_play_from: '星芽短剧',
      vod_play_url: urls.join('#')
    }]
  });
}

/// === search ===
async function search(wd, quick) {
  const url = `${HOST}/v3/search?keyword=${encodeURIComponent(wd)}`;
  const res = JSON.parse(await req(url));
  const videos = [];

  if (res?.data?.list) {
    res.data.list.forEach(it => {
      videos.push({
        vod_id: `${HOST}${DETAIL_PATH}?theater_parent_id=${it.theater.id}`,
        vod_name: it.theater.title,
        vod_pic: it.theater.cover_url,
        vod_remarks: `${it.theater.total || 0}集`
      });
    });
  }

  return JSON.stringify({ list: videos });
}

/// === player（直接透传）===
async function player(flag, id, flags) {
  return JSON.stringify({
    url: id,
    header: HEADERS
  });
}
