//永久地址https://fantuantv.com
var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'饭团动漫[漫]',
  host:'https://acgfta.com',
  url:'/ft/fyclass/file/recent/page/fypage.html',
  searchUrl:'/search/page/fypage/wd/**.html',
  searchable:2,
  quickSearch:0,
  filterable:0,
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.navbar-nav li;a&&Text;a&&href;.*/(.*?)\.html',
  cate_exclude:'新番归档|榜单',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'*',
  一级:'.col.anime-card;.lozad&&alt;.lozad&&data-src;.semibold.mb-0&&Text;.stretched-link&&href',
  二级:{
    title:'.py-3 h6&&Text;.semibold:eq(4)&&Text',
    img:'.lozad&&data-src',
    desc:';.semibold:eq(3)&&Text;;;',
    content:'.overflow-auto&&Text',
    tabs:'.nav.nav-pills.mb-3 li',
    lists:'.anime-episode:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'*',
}