//网址发布页https://v.auete.com/ 
var rule = {
  类型: '影视',//影视|听书|漫画|小说
  title: 'Auete影视',
  host: 'https://www.auete.cc',//https://www.auete.com
  searchUrl: '/auete4so.php?page=fypage&searchword=**&searchtype=',
  searchable: 2,
  quickSearch: 0,
  filterable: 1,
  url: '/fyclassfyfilter/indexfypage.html[/fyclassfyfilter/index.html]',
  filter_url: '{{fl.class}}',
  filter: {
    "Movie": [{ "key": "class", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "喜剧片", "v": "/xjp" }, { "n": "动作片", "v": "/dzp" }, { "n": "爱情片", "v": "/aqp" }, { "n": "科幻片", "v": "/khp" }, { "n": "恐怖片", "v": "/kbp" }, { "n": "惊悚片", "v": "/jsp" }, { "n": "战争片", "v": "/zzp" }, { "n": "剧情片", "v": "/jqp" }] }],
    "Tv": [{ "key": "class", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "美剧", "v": "/oumei" }, { "n": "韩剧", "v": "/hanju" }, { "n": "日剧", "v": "/riju" }, { "n": "泰剧", "v": "/yataiju" }, { "n": "网剧", "v": "/wangju" }, { "n": "台剧", "v": "/taiju" }, { "n": "国产", "v": "/neidi" }, { "n": "港剧", "v": "/tvbgj" }, { "n": "英剧", "v": "/yingju" }] }],
    "Zy": [{ "key": "class", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "国综", "v": "/guozong" }, { "n": "韩综", "v": "/hanzong" }, { "n": "美综", "v": "/meizong" }] }],
    "Dm": [{ "key": "class", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "动画", "v": "/donghua" }, { "n": "日漫", "v": "/riman" }, { "n": "国漫", "v": "/guoman" }, { "n": "美漫", "v": "/meiman" }] }],
    "qita": [{ "key": "class", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "记录片", "v": "/Jlp" }, { "n": "经典片", "v": "/Jdp" }, { "n": "经典剧", "v": "/Jdj" }, { "n": "网大电影", "v": "/wlp" }, { "n": "国产老电影", "v": "/laodianying" }] }]
  },
  headers: {
    'User-Agent': 'PC_UA','Cookie': 'ssea2_search=ok'
  },
  timeout: 5000,
  class_parse: '.navbar-nav li;a&&Text;a&&href;.*/(.*?)/',
  cate_exclude: '新站|网址发布页|搜索',
  play_parse: true,
  lazy: $js.toString(() => {
    input = { parse: 1, url: input, js: '' };
  }),
  double: true,
  推荐: '*',
  一级: '.picture_list_container li;h2 a&&title;.pic img&&src;.hdtag&&Text;h2 a&&href',
  二级: {
    title: 'meta:eq(5)&&content;.message p:eq(5)&&Text',
    img: 'meta:eq(16)&&content',
    desc: 'meta:eq(11)&&content;.message p:eq(9)&&Text;meta:eq(6)&&content;meta:eq(10)&&content;.message p:eq(3)&&Text',
    content: 'meta:eq(17)&&content',
    tabs: '#player_list h2',
    lists: '#player_list:eq(#id)&&a',
    tab_text: 'body&&Text',
    list_text: 'body&&Text',
    list_url: 'a&&href',
    list_url_prefix: '',
  },
  //搜索:'*',
}