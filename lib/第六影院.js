var rule = {
  类型: '影视',
  title: '第六影院',
  author: '不告诉你',
  host: 'https://www.nevatasoft.com',
  url: '/vod/fyfilter/',
  searchUrl: '/vod/search/?wd=**&page=fypage',
  headers: { 'User-Agent': 'MOBILE_UA', },
  searchable: 1, quickSearch: 1, timeout: 5000, play_parse: true, filterable: 1, invalid: true,
  class_name: '电影&电视剧&动漫&短剧&综艺&体育',
  class_url: 'dyp&lxj&dmp&dj&zyp&tyss',
  filter_url: 'dl{{fl.类型}}-fypage',
  filter_def: { 'dyp': { 类型: 'dyp' }, 'lxj': { 类型: 'lxj' }, 'dmp': { 类型: 'dmp' }, 'dj': { 类型: 'dj' }, 'zyp': { 类型: 'zyp' }, 'tyss': { 类型: 'tyss' } },
  推荐: '*',
  一级: 'ul.row li;a&&title;.lazyload&&data-original;span.pic-label&&Text;a&&href',
  二级: {
    title: 'ul.d-flex&&h2&&Text;ul.d-flex&&li:eq(1)&&Text',
    img: '.lazyload&&data-original||data-src||src',
    desc: 'ul.d-flex&&li:eq(4)&&Text;p.btn:eq(2) a&&Text;p.btn:eq(1) a&&Text;ul.d-flex&&li:eq(2)&&Text;ul.d-flex&&li:eq(3)&&Text',
    content: '.detail-info&&.intro-all&&Text',
    tabs: 'body&&.section.vod-play-list-box h2:not(:contains(备用))',
    lists: 'body&&.vod-play-list-box ul.row:eq(#id) a',
    tab_text: 'body&&Text',
  },
  搜索: '*',
  lazy: `js:
  let html = request(input);
  let hconf = html.match(/r player_.*?=(.*?)</)[1];
  let json = JSON5.parse(hconf);
  let url = json.url;
  if (json.encrypt == '1') {
    url = unescape(url);
  } else if (json.encrypt == '2') {
    url = unescape(base64Decode(url));
  }
  if (/\\.(m3u8|mp4|m4a|mp3)/.test(url)) {
    input = {
      parse: 0,
      jx: 0,
      url: url,
    };
  } else {
    input;
  }`,
  filter: {
    "dyp": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "dyp" }, { "n": "喜剧片", "v": "xjp" }, { "n": "科幻片", "v": "khp" }, { "n": "古装片", "v": "gzp" }, { "n": "邵氏电影", "v": "ssdy" }, { "n": "网络电影", "v": "wldy" }, { "n": "奇幻片", "v": "qhp" }, { "n": "同性片", "v": "txp" }, { "n": "其他片", "v": "qtp" }, { "n": "经典片", "v": "jdp" }, { "n": "犯罪片", "v": "fzp" }, { "n": "灾难片", "v": "znp" }, { "n": "惊悚片", "v": "jsp" }, { "n": "动作片", "v": "dzp" }, { "n": "爱情片", "v": "aqp" }, { "n": "剧情片", "v": "jqp" }, { "n": "战争片", "v": "zzp" }, { "n": "恐怖片", "v": "kbp" }, { "n": "动画片", "v": "dhp" }, { "n": "歌舞片", "v": "gwp" }, { "n": "悬疑片", "v": "xyp" }, { "n": "冒险片", "v": "mxp" }, { "n": "纪录片", "v": "jlp" }] }],
    "lxj": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "lxj" }, { "n": "大陆剧", "v": "dlj" }, { "n": "其他剧", "v": "qtj" }, { "n": "泰国剧", "v": "tgj" }, { "n": "海外剧", "v": "hwj" }, { "n": "日本剧", "v": "rbj" }, { "n": "香港剧", "v": "xgj" }, { "n": "台湾剧", "v": "twj" }, { "n": "韩国剧", "v": "hgj" }, { "n": "欧美剧", "v": "omj" }] }],
    "dmp": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "dmp" }, { "n": "国产动漫", "v": "gcdm" }, { "n": "日韩动漫", "v": "rhdm" }, { "n": "日本动漫", "v": "rbdm" }, { "n": "韩国动漫", "v": "hgdm" }, { "n": "港台动漫", "v": "gtdm" }, { "n": "欧美动漫", "v": "omdm" }, { "n": "海外动漫", "v": "hwdm" }, { "n": "其他动漫", "v": "qtdm" }] }],
    "zyp": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "zyp" }, { "n": "大陆综艺", "v": "dlzy" }, { "n": "其他综艺", "v": "qtzy" }, { "n": "欧美综艺", "v": "omzy" }, { "n": "韩国综艺", "v": "hgzy" }, { "n": "港台综艺", "v": "gtzy" }, { "n": "日韩综艺", "v": "rhzy" }, { "n": "日本综艺", "v": "rbzy" }] }],
    "dj": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "dj" }, { "n": "网络短剧", "v": "wldj" }, { "n": "影视解说", "v": "ysjs" }] }],
    "tyss": [{ "key": "类型", "name": "分类", "value": [{ "n": "全部", "v": "tyss" }, { "n": "斯诺克", "v": "snk" }, { "n": "蓝球", "v": "lq" }, { "n": "足球", "v": "zq" }, { "n": "游戏竞技", "v": "yxjj" }] }]
  }
}

