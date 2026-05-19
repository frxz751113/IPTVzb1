var rule = {
  title: 'KimiVod',
  host: 'https://kimivod.com',
  url: '/vod/showfyfilter.html',
  searchUrl: '/search.php?page=fypage&searchword=**&searchtype=',
  searchable: 2, quickSearch: 0, filterable: 1,
  headers: { 'User-Agent': 'MOBILE_UA'},
  /*class_name: '电影&剧集&综艺&动漫&短剧&国产剧&韩剧&美剧&日剧&台剧&港剧&海外剧&纪录片&泰剧&战争片&动画电影&悬疑片&奇幻片&爱情片&恐怖片&剧情片&动作片&科幻片&喜剧片&国产动漫&日本动漫&韩国动漫&欧美动漫&港台动漫&台港综艺&欧美综艺&韩日综艺&国产综艺',
  class_url: '2&1&4&3&39&6&7&8&9&10&11&12&26&32&22&23&24&25&21&20&13&14&15&16&28&27&29&30&31&36&33&34&38',*/
  class_name: '电视剧&电影&动漫&综艺&短剧',
  class_url: '1&2&3&4&39',
  filter: {
    "1": [{ "key": "类型", "name": "类型", "value": [{ "n": "陆剧", "v": "/id/6" }, { "n": "韩剧", "v": "/id/7" }, { "n": "美剧", "v": "/id/8" }, { "n": "日剧", "v": "/id/9" }, { "n": "台剧", "v": "/id/10" }, { "n": "港剧", "v": "/id/11" }, { "n": "海外剧", "v": "/id/12" }, { "n": "纪录片", "v": "/id/26" }, { "n": "泰剧", "v": "/id/32" }] }],
    "2": [{ "key": "类型", "name": "类型", "value": [{ "n": "战争片", "v": "/id/22" }, { "n": "动画电影", "v": "/id/23" }, { "n": "悬疑片", "v": "/id/24" }, { "n": "奇幻片", "v": "/id/25" }, { "n": "爱情片", "v": "/id/21" }, { "n": "恐怖片", "v": "/id/20" }, { "n": "剧情片", "v": "/id/13" }, { "n": "动作片", "v": "/id/14" }, { "n": "科幻片", "v": "/id/15" }, { "n": "喜剧片", "v": "/id/16" }] }],
    "3": [{ "key": "类型", "name": "类型", "value": [{ "n": "大陆动漫", "v": "/id/28" }, { "n": "日本动漫", "v": "/id/27" }, { "n": "欧美动漫", "v": "/id/30" }, { "n": "港台动漫", "v": "/id/31" }, { "n": "韩国动漫", "v": "/id/29" }] }],
    "4": [{ "key": "类型", "name": "类型", "value": [{ "n": "台湾香港综艺", "v": "/id/36" }, { "n": "欧美综艺", "v": "/id/33" }, { "n": "韩国日本综艺", "v": "/id/34" }, { "n": "大陆综艺", "v": "/id/38" }] }],
    "39": [{ "key": "类型", "name": "类型", "value": [{ "n": "短剧", "v": "/id/39" }] }]
  },
  filter_url: '{{fl.类型}}/page/fypage',
  filter_def: { '1': { 类型: '/id/1' }, '2': { 类型: '/id/2' }, '3': { 类型: '/id/3' }, '4': { 类型: '/id/4' }, '39': { 类型: '/id/39' } },
  play_parse: true, limit: 6, double: true,
  lazy: `js:
  let html=request(input);
  input=html.match(/vid\s*=\s*["'](.*?)["']/)[1];
  `,
  推荐: '.row article;body;.transparent a&&title;.lazyload&&data-src||src;.small-text&&Text;.transparent a&&href',
  一级: '.grid.container_list .s6;a&&title;img&&data-src;.white-text.small-text&&Text;a&&href',
  二级: {
    title: 'h1&&Text;.scroll.no-margin a:eq(0)&&Text',
    img: '.lazyload&&data-src||src',
    desc: '.medium-line p:eq(2)&&Text;.scroll.no-margin a:eq(2)&&Text;.scroll.no-margin a:eq(1)&&Text;.medium-line p:eq(0)&&Text;.medium-line p:eq(1)&&Text',
    content: '.right-align&&Text',
    tabs: '.tabs span',
    lists: '.playno:eq(#id) a'
  },
  搜索: '.thumb;a&&title;.myui-vodlist__thumb&&data-original;.text-right&&Text;.myui-vodlist__thumb&&href;.pic-tag-top&&Text',
}
