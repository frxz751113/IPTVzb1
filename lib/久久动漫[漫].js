var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'久久动漫[漫]',
  host:'http://www.995dm.com',
  //url:'/type/fyclass-fypage.html',//不带筛选写法
  searchUrl:'/search-pg-fypage-wd-**.html',
  url: '/vod-list-id-fyclass-pg-fypage-fyfilter.html',//带筛选写法
  filter:'H4sIAAAAAAAAA+2Z20obURSGX2XIdYW9kzn2VYoXUQKVWgtqC0EEU62NhyZRbFSqQWnTWjTFQymaUPsy2TPJWzQRG7L+tQJTwbu5C5lv9uHfe+b/154FK6VTT61n1oKVepHL936mJqezc3OpJ1ZqJvsy1/8j3FyLLlqmttH/8012+nXu3x0z/ctmdbu7//3u2uD2MZ2yFp8MkGi50TleAiRNEFN/b25agGQIEhY2ouIFIDZFjo7NpwYgDu2oUjI/TgFxaSuVWnS2BYhHkO7hdrhXB8Snk96/NZUiIAFFvm3xSWuYUukkqqwiQ5XpNnbCq4/IUIGjeq2HIUPXKbxshSs4ZK1oO6e1cB3X0qHzCt+eRVUU0KXthMW9dnMNGTrmTuWwU2IMmzvX0LWxr7C6iwzdF2Fjs1Os4XLRJTWlVVO+RIbO3axfmD/Yl1bQUOGXWS6zxaBQp7BpDppsVftLZo3fg/fPbD6XnR1+ZM3Nz3br94jn9d1Jd/lk0CzpMq3SmcGVfqNjd/8AkmZIGhHNEI2IYogCRAeI6AARnyE+Ih5DPERchriIOAxxELEZYiPC1NWormbqalRXM3U1qquZuhrVVUxdheoqpq5CdRVTV6G6iqmrUF3F1FWormLqKlRXMXUVqquYugrVVUxdheoqpq5SwlM5kSc2Wto2zbL8TIYHS2H1fNDoRH5sfqp313Cv7WYzPN8ZRp5Pzc+hVXQ+VIaRuclXs7n7kVnjvQv2Y5i9Aw4hub0DTtP42r49QiZGJHDoikalFYGhG0N2LLq/RBdx6DYV3dqhu13MKE4MF/Eg60iO5YGriTGFzkt0fc/FvrgTB3Repvyl+7nEDIsuqjnfMvUrBsXwdA2vQTmIYDLarZvrawbFsHUNr3fZjsGPRtgxHXi7tc/3tU47iWcnnp14duLZD/HszGN4dga8TfLsDHiAWKLTzSX6XwaqQ6lIt+lWF6t0GzKE5H823RqikdiQISSPtOlGFStsG7xWKvhtF5ebV/M21VnMGTYcLkiZxo5ThcfwfhfqULEKD1AfPmaPVfxCpqFrKp6reJALpfykFXQm+j68FcJCJVyqMoguvez78MYcUfXD0YBc9QdJOEjCQRIOknDwkHDQ29ePkA48cCQpHXhQ1UrpwANHktKBDy9uKR34UGhK6cAH55fSgQ9nx+IpPpweSK7uQ5EppQwfEpaUMnz4qiClDN/HPcEThB/ju0IQ4xw/AH+UEkQAOounB1RnMUEELGEJY3awL54gAqjl5XQAg5bTAX5vEtMBHdKIdABjEtMBvMBHpAMvRndpO4kQSYRIIkQSIf47QliLfwGeToG8AyAAAA==',
  filter_url:'-{{fl.by}}-{{fl.class}}-{{fl.year}}-',
  //https://www.995dm.com/vod-list-id-3-pg-2-order--by-score-class-40-year-2023-letter--area--lang-.html
  filter_def:{
    1: {cateId: '1'},
    3: {cateId: '3'},
    4: {cateId: '4'},
    16: {cateId: '16'}
  },
  searchable:2,
  quickSearch:0,
  filterable:1,
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.nav-pc li b;a&&Text;a&&href;.*/(\\d+)',
  tab_exclude:'线路空',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'*',
  一级:'.index-tj li;p.name&&Text;img&&data-original;.bz&&Text;.li-hv&&href',
  二级:{
    title:'.h2 a:eq(2)&&Text;.info dd:eq(0)&&Text',
    img:'img&&src',
    desc:';.info dd:eq(3)&&Text;.info dd:eq(2)&&Text;.info dd:eq(4)&&Text;.info dd:eq(1)&&Text',
    content:'.des2&&Text',
    tabs:'.pfrom.tab1.clearfix li',
    lists:'.urlli:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'*',
}