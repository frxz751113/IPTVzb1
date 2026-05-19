var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'统一影视',
  host:'https://www.tyys1.com',
  //url:'/index.php/vod/type/id/fyclass/page/fypage.html',//不带筛选
  searchUrl:'/index.php/vod/search/page/fypage/wd/**.html',
  searchable:2,
  quickSearch:0,
  filterable:1,
  url: '/index.php/vod/show/fyfilter.html',//带筛选写法
  filter:'H4sIAAAAAAAAA+2bW08bRxTHv4ufqcwacn3LPeR+vyoPTmKlqJRKQCuhKBLEQDEEDAjsAOamYAwtxnZIaTHYfBnP7vpbdOwZnz17tpLHakqJmEf/f4czM2dnZs9fK976DN/Z5299P4R6fWd9r4I9obbXviZfZ/DHEP/Nhoes3B7//Uuw4+dQNbCTy9b0H3ZqqCLzH/72137D964JECvkEAoAYiPr5v7vCLU4f7W3b0fyCLU6aCnNIimM+GAvKlROuSPY3e3MmE+XLY56ZswG18vhdZnFmVEkZYYHa7mrmfxSq4WY7zet2KQ7RGoww+GcJ4vUYKDxIRb9TAYSGmQZyViF30gWoaEClgoJkkVoEJL8le3ukRCh1ULKC1Pmx6Q7RGqw6OGPpXyELFpoMN3UpGcgqcFcoqv2J1pdoUHI0FR5doOECA3m0j9h9sXIXIQGIem1UnGZhAgNBurfYeEoGUhoeDMFu0JBtPsTWfYhr7qXVlPlWTgTlUR+KUHh12bNvzKuCCk5Fcuau0V3DiFBjqUNNl9w5xASFCOeNBObrggpwaMrjtMcUqpF2KM5GiElGGU7SyOkBBGxLBtZZgsr7iBQYUUbm+ZC0k4elPJz7nVhABUay7L8mrtCQnJmNuOd2QyeGSv+SSOkBDkGovzZseENdxpQnQO5bI4ecNGdDFTIV9wWf0nX6AKQdXCntBdzpxQS3qq9oWAX2qq7X0p7BcWtGmgOtNbSV9L4qwKiLZS2YBqgNICpQamBaTOlzYgaZwjlAqKnKT2N6SlKT2F6ktKTmJ6g9ASmtFYGrpVBa2XgWhm0VgaulUFrZeBaGbRWXMAboCPY+cbZAHYmba/3qd5V8wUeX0tfSeSXEtwRn1dphJTg3MYLbCxOgxwV9v7sVrlvzs4suOIcFd05NJmU0N3nGU5I6O6jEVJC95YnQkjo/vBGzOAIfll4qickz/3hyYQBrDx5YEXTVmTWs34MatGlgwEaJyXIN7liTwz8Uz4M8I2a8BTFUV1bLtTTE8K3TjpuZsYUN905GKCaxX8OyHlCzgO5QMgFIBcJuQjkEiGXgFwm5DKQK4RcAXKVkKtA2ghpA3KNkGtArhNyHcgNQm4AuUnITSC3CLkF5DYht4HcIeQOkLuE3AVyj5B7QO4Tch/IA0IeAHlIyEMgjwh5BOQxIY+BPCHkCZCnhDwF8oyQZ0CavztDWEXBR+Blr7P9zfEplo96tr8Z3ynHv9TyvOz197TzcDi/+byZnUb0+/aebufsZga450K0+9VPXaHKDF40+QLH2KkpWJ9YAg0vQ4TWgFNT8DUKjkTFWIZHzPdzJIvQGrGECgaqvplTMLkqHqu+9+SPzJqmIUKDE7CVZYUZd4jU4AjtL3PFHSK1Bgy3mf5gDy/SFVU1eAD9xfJckTwAoWnXqF3jkXKNvAm0CnEz5t4qjurpNt0PClTtQrUL/XZc6FdxjYoO9Zi7S+0DtQ/UPvAo+MCW4+sDrXDaXukjHbnQGrBEKl/J0tP8YnaHSA2ybO2wfJpkEVojPlDh+9byCpsnA0kNQiYWrU3q4IQGK1L67mfG4h6rWNEa8ccKbrJ/lPtuuuiq9pWMVX1DU9968W6klCddupDUTZGC9apvPeoavPrWS9UeqJqT+nZIGwhtILSB0AZCGwhtILSBOFIGovUYG4jEEi+claIeAmTn2t8u7U6QdlloDRgAeyDHop88wznyoX1HqN8QK7Sqmyne3rpzCAly/JuvFbotxFS3hbot1G2hbgt1W6jbwkNqC4/jv4L85/3XN9rVHNa72MxFPO8bISm/R/UbRL9B9Bvk/3+DvPsbfKZEUk04AAA=',
  filter_url:'{{fl.area}}{{fl.by}}{{fl.class}}{{fl.cateId}}{{fl.lang}}{{fl.letter}}/page/fypage{{fl.year}}',
  //https://www.tyys1.com/index.php/vod/show/area/大陆/by/hits/class/动作/id/2/lang/国语/letter/B/page/2/year/2024.html
  filter_def:{
    1: {cateId: '/id/1'},
    2: {cateId: '/id/2'},
    3: {cateId: '/id/3'},
    4: {cateId: '/id/4'},
    41: {cateId: '/id/41'}
  },
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.head-nav li;a&&Text;a&&href;/(\\d+)\.html',
  cate_exclude:'体育赛事',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'*',
  一级:'.public-list-box;.time-title&&Text;.lazy&&data-src;.public-list-prb&&Text;.time-title&&href',
  二级:{
    title:'h3&&Text;.slide-info-remarks&&Text',
    img:'.detail-pic img&&data-src',
    desc:'.gen-search-form li:eq(6)&&Text;.gen-search-form li:eq(4)&&Text;.gen-search-form li:eq(5)&&Text;.gen-search-form li:eq(2)&&Text;.gen-search-form li:eq(3)&&Text',
    content:'#height_limit&&Text',
    tabs:'.anthology-tab a',
    lists:'ul.anthology-list-play:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'body .box-width .search-box;.thumb-txt&&Text;.lazy&&data-src;.public-list-prb&&Text;.public-list-exp&&href;.thumb-else span:eq(2)&&Text',
}