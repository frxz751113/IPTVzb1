var rule = {
    模板:'首图2',
  title: '剧集屋',
  host: 'http://jjwu.org',
  url: '/index.php/vod/show/fyfilter.html',
  searchUrl: '/index.php/vod/search.html?wd=**&submit=',
  filterable: 1,
  filter: {
    "1":[{key:'类型',name:'类型',value:[{n:'全部',v:'',},{n:'动作片',v:'/id/6',},{n:'科幻片',v:'/id/7',},{n:'喜剧片',v:'/id/8',},{n:'剧情片',v:'/id/9',},{n:'爱情片',v:'/id/10',},{n:'恐怖片',v:'/id/11',},{n:'战争片',v:'/id/12',},{n:'动画片',v:'/id/26',},],},{key:'排序',name:'排序',value:[{n:'按时间',v:'/by/time',},{n:'按人气',v:'/by/hits',},{n:'按评分',v:'/by/score',},],},],
    "2":[{key:'类型',name:'类型',value:[{n:'全部',v:'',},{n:'国产剧',v:'/id/21',},{n:'TVB港剧',v:'/id/22',},{n:'美剧',v:'/id/23',},{n:'韩剧',v:'/id/24',},],},{key:'排序',name:'排序',value:[{n:'按时间',v:'/by/time',},{n:'按人气',v:'/by/hits',},{n:'按评分',v:'/by/score',},],},],
    },
    filter_url: '{{fl.类型}}{{fl.排序}}/page/fypage',
    filter_def: { 1: { 类型: '/id/1' }, 2: { 类型: '/id/2' } },
}