var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'鬼片之家',
  host:'https://www.guipian360.com',
  url:'/list/fyclass-fypage.html',
  searchUrl:'/vodsearch/**----------fypage---.html',
  searchable:2,
  quickSearch:0,
  filterable:0,
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.nav li;a&&Text;a&&href;/(\\d+)\.html',
  cate_exclude:'',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'*',
  一级:'.m-movies .u-movie;a&&title;img&&src;.zhuangtai&&Text;a&&href',
  二级:{
    title:'h1&&Text;.movielabel&&Text',
    img:'img&&data-original||src',
    desc:'.media .fr&&Text;.media strong:eq(0)&&Text;;.media li:eq(1)&&Text;.media li:eq(0)&&Text',
    content:'.jianjie&&Text',
    tabs:'dl li',
    lists:'.list:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'*',
}