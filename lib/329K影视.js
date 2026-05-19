var rule = {
  title: '329K影视',
  host: 'https://www.329k.com/',
  class_name: '电影&电视剧&综艺&动漫&短剧',
  class_url: '1&2&3&4&5',
  searchUrl: '/search/**----------fypage---.html',
  searchable: 2,
  quickSearch: 0,
  headers: {
    'User-Agent': 'PC_UA',
    'Referer': 'https://www.329k.com',
  },
  url: '/index.php/api/vod#type=fyclass&page=fypage',
  filterable: 0,
  detailUrl: '/detail/fyid.html',
  play_parse: true,
  
  // 智能播放解析逻辑
  lazy: `js:
  let html = request(input);
  let url = '';
  
  // 1. 优先解析 player_aaaa (这是MacCMS最标准的数据源，最稳)
  let pat = /var player_aaaa=({[\s\S]*?});/;
  let match = html.match(pat);
  
  if (match) {
    try {
      let json = JSON.parse(match[1]);
      url = json.url;
      // 某些源 url_next 才是实际播放地址，这里优先取 url
    } catch (e) {
      log('JSON解析错误: ' + e);
    }
  }

  // 2. 兜底逻辑：如果 player_aaaa 没取到，尝试从 iframe 提取
  if (!url) {
    let ifr = html.match(/<iframe[^>]*src=["']([^"']+)["']/i);
    if (ifr) {
      let src = ifr[1];
      // 你的源码中 iframe 包含 &url=...，处理这种情况
      if (src.indexOf('url=') > -1) {
        // 提取 url= 后面的内容
        let parts = src.split('url=');
        url = parts[parts.length - 1].split('&')[0];
      } else {
        url = src;
      }
    }
  }

  // 3. 最终输出处理
  if (url) {
    // 解码 (源码中的 url 是 decode 过的，但 iframe 里的可能是 encode 的，统一解码保险)
    url = decodeURIComponent(url);
    
    // 补全协议
    if (url.startsWith('//')) {
      url = 'https:' + url;
    }

    // 智能判断：如果是 m3u8/mp4 直接播，否则走解析
    // 你的源码里是 .m3u8，会命中 parse:0 (直连)，速度最快
    if (/\.(m3u8|mp4)/i.test(url)) {
      input = { jx: 0, parse: 0, url: url };
    } else {
      input = { jx: 0, parse: 1, url: url };
    }
  } else {
    input;
  }
`,
  推荐: '.flex.wrap .public-list-box;a&&title;.public-list-div img&&data-src;.public-list-subtitle&&Text;a&&href',
  
  // 一级分类页：处理加密API请求
  一级: 'js:let body=input.split("#")[1];let t=Math.round(new Date/1e3).toString();let key=md5("DS"+t+"DCC147D11943AF75");let url=input.split("#")[0];body=body+"&time="+t+"&key="+key;fetch_params.body=body;fetch_params.method="POST";let html=post(url,fetch_params);let data=JSON.parse(html);VODS=data.list.map(function(it){return {vod_name:it.vod_name,vod_pic:it.vod_pic.startsWith("http")?it.vod_pic:"https://www.329k.com/"+it.vod_pic,vod_id:it.vod_id,vod_remarks:it.vod_remarks};});',

  // 二级详情页：精准匹配选集和列表
  二级: {
    title: '.slide-info-title&&Text',
    img: '.detail-pic img&&data-src',
    desc: '.slide-info&&Text;.slide-info-remarks:eq(0)&&Text;.slide-info-remarks:eq(1)&&Text;.slide-info:eq(3)&&Text;.slide-info:eq(2)&&Text;',
    content: '#height_limit&&Text',
    tabs: '.anthology-tab .swiper-wrapper a',
    tab_text: 'body&&Text',
    lists: '.anthology-list-play:eq(#id) li a',
    list_text: 'body&&Text',
    list_url: 'a&&href',
  },
  
  搜索: '.row-right .public-list-box;.thumb-txt&&Text;.lazy&&data-src;;a&&href',
}
