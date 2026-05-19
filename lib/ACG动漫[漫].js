//地址发布页https://www.omoo.app
var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title: 'ACG动漫[漫]',
  host: 'https://www.acgbibi.com',
  url: '/type/fyclass-fypage.html',
  searchUrl: '/search/**----------fypage---.html',
  searchable:2,
  quickSearch:0,
  filterable:0,
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.snui-header-menu-nav li:gt(0):lt(7);a&&Text;a&&href;/(\\d+)\.html',
  cate_exclude:'宅文化',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'.Ibga_ACacIHE li;body;.lazyload&&title;.lazyload&&data-original;.Iec_GGIe&&Text;.lazyload&&href;.text-right&&Text',
  一级:'.Ibga_ACacIHE li;.lazyload&&title;.lazyload&&data-original;.Iec_GGIe&&Text;.lazyload&&href;.text-right&&Text',
  二级:{
    title:'h1.title&&Text;.data:eq(1)&&Text',
    img:'.lazyload&&data-original||src',
    desc:'.data:eq(0)&&Text;.data:eq(4)&&Text;.data:eq(2)&&Text;.data:eq(6)&&Text;.data:eq(5)&&Text',
    content:'.detail-content&&Text',
    tabs:'.channel-tab li',
    lists:'.play-list-content:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
  },
  搜索:'*',
  搜索验证标识:'系统安全验证',
}