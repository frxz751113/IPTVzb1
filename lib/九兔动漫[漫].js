//发布页 https://www.9tdm.com/fby.html
var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'九兔动漫[漫]',
  host:'https://www.9tdm.com',
  url:'/vodshow/fyclassfyfilter.html',
  searchUrl:'/search/page/fypage/wd/{wd}.html',
  searchable:2,
  quickSearch:0,
  filterable:1,
  filter:'H4sIAAAAAAAAA+2Vy04bQRBFf6U1EjsW1UM8D7Z8BmLBwisIu0SKkCWCw2NMhAxCzsuKI0VgEgIRgo2xHH5mHvgvMnY301Xl/ECsWtm373VX60x77rbyAm9Zrapt5W3U35RfveJ2mH098haVt7X+sj5Zyd8nbvH1+uar+vNPtiZ21ulmSX/qIakai1WiOLzNm3tVwkqcyNrH2c2V28NIkmhdpqOuSxhJpvRPssHQTTESJ/LdX0XnpEpYSfZo/S5GP90eRpI9mq1897Pbw0hy0v3T8acf7qRGksT5AT6plWTK23a+03FTjCSJw4/pQ+ISRpIpSR9Tt5IxLc6GmOlEkinXF+mfb26KkTgx7t2lg3aVsBInnh7b5c5VwkpyjnePxdW5O4eR5Ln0rovkwD0XI1VDrdmUvbzZ4D4djtjldYv/uLx7l+OmOxwZ6oP/onKmgrlL2F3iro9dn7sau5q7gF1gro6RWwrmRtiNuBtiN+RugN2AuzXs1riLWWnOSmNWmrPSmJXmrDRmpTkrjVlpzgowK+CsALMCzgowK+CsALMCzgowK+CsALMCzgowK+CsALMCzgowK+CsALMCyiqG6f/ke5XQcQwL/kr5QbFFs8HIBCMaDGeDoQmGNBjMBgMTDGgw/3Kff3CvVh2BidVi+y5Qa6UXSqNJo0mjSaNJo0mjzUWjRdJo0mjSaNJo0mjSaHPRaLE0mjSaNJo0mjSaNNpcNFp5CaTSpNKk0qTSpNKk0v77SlONv66JKEMdIgAA',
  filter_url:'---{{fl.类型}}-----fypage---{{fl.年份}}',
  //实例 https://www.9tdm.com/vodshow/6---奇幻-----2---2021.html
  filter_def:{
    6: {cateId: '6'},
    7: {cateId: '7'},
    8: {cateId: '8'},
    9: {cateId: '9'},
    10: {cateId: '10'}
  },
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.nav li:gt(0):lt(6);a&&Text;a&&href;/(\\d+)\.html',
  cate_exclude:'',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'*',
  一级:'.list-item;h3&&Text;img&&data-src;.line-1&&Text;.media-content&&href',
  二级:{
    title:'h1&&Text;.w-obj li:eq(0)&&Text',
    img:'img&&src',
    desc:'.mb-2:eq(0)&&Text;.mb-2:eq(1)&&Text;.mb-2:eq(2)&&Text',
    content:'.video-content span&&Text',
    tabs:'.form-select option',
    lists:'.hl-plays-list:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'.list-item .border-bottom;h3&&Text;img&&data-src;.w-obj p:eq(0)&&Text;h3 a&&href',
}