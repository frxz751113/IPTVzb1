var rule = {
  title: '饺子影院[盘]',
  host: 'https://www.jiaozi.me',
  url: '/mlist/indexfyclass-fypage.html',
  searchUrl: '/search.php?page=fypage&searchword=**&searchtype=',
  searchable: 2,
  quickSearch: 0,
  headers: {
    'User-Agent': 'PC_UA',
  },
  timeout: 5000,
  class_name: '电影&电视剧&动漫',
  class_url: '1&2&41',
  play_parse: true,
  //推送阿里播放  支持影视壳
  lazy: $js.toString(() => {
    let url = input.startsWith('push://') ? input : 'push://' + input;
    input = { parse: 0, url: url };
  }),
  推荐:'*',
  一级: '.myui-vodlist li;a&&title;a&&data-original;.text-right&&Text;a&&href',
  二级: {
    "title": ".myui-content__thumb&&title;",
    "img": ".myui-content__thumb&&img&&data-original",
    "desc": "",
    "content": ".myui-panel-box&&p:eq(0)&&Text",
    "tabs": "",
    "lists": ".downlist&&p",
    "list_text": "a&&title"
  },
  搜索: '.myui-vodlist__media li;a&&title;a&&data-original;.text-right&&Text;a&&href',
}