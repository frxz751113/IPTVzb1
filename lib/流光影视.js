var rule = {
  title: '流光影视',
  host: 'https://www.lgys.xyz',
  url: '/index.php/vod/showfyfilter.html',
  searchUrl: '/index.php/vod/search.html?wd=**',
  searchable: 2,
  quickSearch: 0,
  filterable: 1,
  headers: {
    'User-Agent': 'MOBILE_UA',
  },
  class_parse: '.menu a:gt(0):lt(8);a&&Text;a&&href;/(\\d+).html',
  play_parse: true,
  filter: {
    "1": [{ "key": "地区", "name": "地区", "value": [{ "n": "全部", "v": "" }, { "n": "中国大陆", "v": "/area/中国大陆" }, { "n": "中国香港", "v": "/area/中国香港" }, { "n": "中国台湾", "v": "/area/中国台湾" }, { "n": "日本", "v": "/area/日本" }, { "n": "韩国", "v": "/area/韩国" }, { "n": "泰国", "v": "/area/泰国" }, { "n": "欧美", "v": "/area/欧美" }, { "n": "印度", "v": "/area/印度" }, { "n": "马来西亚", "v": "/area/马来西亚" }, { "n": "其他", "v": "/area/其他" }] }, { "key": "年份", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "/year/2025" }, { "n": "2024", "v": "/year/2024" }, { "n": "2023", "v": "/year/2023" }, { "n": "2022", "v": "/year/2022" }, { "n": "2021", "v": "/year/2021" }, { "n": "2020", "v": "/year/2020" }, { "n": "2019", "v": "/year/2019" }, { "n": "2018", "v": "/year/2018" }, { "n": "2017", "v": "/year/2017" }, { "n": "2016", "v": "/year/2016" }, { "n": "2015", "v": "/year/2015" }, { "n": "2014", "v": "/year/2014" }, { "n": "2013", "v": "/year/2013" }, { "n": "2012", "v": "/year/2012" }, { "n": "2011", "v": "/year/2011" }, { "n": "2010", "v": "/year/2010" }, { "n": "2009", "v": "/year/2009" }, { "n": "2008", "v": "/year/2008" }, { "n": "2007", "v": "/year/2007" }, { "n": "2006", "v": "/year/2006" }, { "n": "2005", "v": "/year/2005" }, { "n": "2004", "v": "/year/2004" }, { "n": "2003", "v": "/year/2003" }, { "n": "2002", "v": "/year/2002" }, { "n": "2001", "v": "/year/2001" }, { "n": "2000", "v": "/year/2000" }] }, { "key": "剧情", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "喜剧", "v": "/class/喜剧" }, { "n": "爱情", "v": "/class/爱情" }, { "n": "恐怖", "v": "/class/恐怖" }, { "n": "动作", "v": "/class/动作" }, { "n": "科幻", "v": "/class/科幻" }, { "n": "剧情", "v": "/class/剧情" }, { "n": "战争", "v": "/class/战争" }, { "n": "警匪", "v": "/class/警匪" }, { "n": "犯罪", "v": "/class/犯罪" }, { "n": "动画", "v": "/class/动画" }, { "n": "奇幻", "v": "/class/奇幻" }, { "n": "武侠", "v": "/class/武侠" }, { "n": "冒险", "v": "/class/冒险" }, { "n": "枪战", "v": "/class/枪战" }, { "n": "恐怖", "v": "/class/恐怖" }, { "n": "悬疑", "v": "/class/悬疑" }, { "n": "惊悚", "v": "/class/惊悚" }, { "n": "经典", "v": "/class/经典" }, { "n": "青春", "v": "/class/青春" }, { "n": "文艺", "v": "/class/文艺" }, { "n": "微电影", "v": "/class/微电影" }, { "n": "古装", "v": "/class/古装" }, { "n": "历史", "v": "/class/历史" }, { "n": "运动", "v": "/class/运动" }, { "n": "农村", "v": "/class/农村" }, { "n": "儿童", "v": "/class/儿童" }, { "n": "网络电影", "v": "/class/网络电影" }] }, { "key": "语言", "name": "语言", "value": [{ "n": "全部", "v": "" }, { "n": "国语", "v": "/lang/国语" }, { "n": "英语", "v": "/lang/英语" }, { "n": "粤语", "v": "/lang/粤语" }, { "n": "闽南语", "v": "/lang/闽南语" }, { "n": "韩语", "v": "/lang/韩语" }, { "n": "日语", "v": "/lang/日语" }, { "n": "法语", "v": "/lang/法语" }, { "n": "德语", "v": "/lang/德语" }, { "n": "其它", "v": "/lang/其它" }] }, { "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }],
    "2": [{ "key": "地区", "name": "地区", "value": [{ "n": "全部", "v": "" }, { "n": "中国大陆", "v": "/area/中国大陆" }, { "n": "中国香港", "v": "/area/中国香港" }, { "n": "中国台湾", "v": "/area/中国台湾" }, { "n": "日本", "v": "/area/日本" }, { "n": "韩国", "v": "/area/韩国" }, { "n": "泰国", "v": "/area/泰国" }, { "n": "欧美", "v": "/area/欧美" }, { "n": "新加坡", "v": "/area/新加坡" }, { "n": "其他", "v": "/area/其他" }] }, { "key": "年份", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "/year/2025" }, { "n": "2024", "v": "/year/2024" }, { "n": "2023", "v": "/year/2023" }, { "n": "2022", "v": "/year/2022" }, { "n": "2021", "v": "/year/2021" }, { "n": "2020", "v": "/year/2020" }, { "n": "2019", "v": "/year/2019" }, { "n": "2018", "v": "/year/2018" }, { "n": "2017", "v": "/year/2017" }, { "n": "2016", "v": "/year/2016" }, { "n": "2015", "v": "/year/2015" }, { "n": "2014", "v": "/year/2014" }, { "n": "2013", "v": "/year/2013" }, { "n": "2012", "v": "/year/2012" }, { "n": "2011", "v": "/year/2011" }, { "n": "2010", "v": "/year/2010" }, { "n": "2009", "v": "/year/2009" }, { "n": "2008", "v": "/year/2008" }, { "n": "2007", "v": "/year/2007" }, { "n": "2006", "v": "/year/2006" }, { "n": "2005", "v": "/year/2005" }, { "n": "2004", "v": "/year/2004" }, { "n": "2003", "v": "/year/2003" }, { "n": "2002", "v": "/year/2002" }, { "n": "2001", "v": "/year/2001" }, { "n": "2000", "v": "/year/2000" }] }, { "key": "剧情", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "古装", "v": "/class/古装" }, { "n": "战争", "v": "/class/战争" }, { "n": "青春偶像", "v": "/class/青春偶像" }, { "n": "喜剧", "v": "/class/喜剧" }, { "n": "家庭", "v": "/class/家庭" }, { "n": "犯罪", "v": "/class/犯罪" }, { "n": "动作", "v": "/class/动作" }, { "n": "奇幻", "v": "/class/奇幻" }, { "n": "剧情", "v": "/class/剧情" }, { "n": "历史", "v": "/class/历史" }, { "n": "经典", "v": "/class/经典" }, { "n": "乡村", "v": "/class/乡村" }, { "n": "情景", "v": "/class/情景" }, { "n": "商战", "v": "/class/商战" }, { "n": "网剧", "v": "/class/网剧" }, { "n": "其他", "v": "/class/其他" }] }, { "key": "语言", "name": "语言", "value": [{ "n": "全部", "v": "" }, { "n": "国语", "v": "/lang/国语" }, { "n": "英语", "v": "/lang/英语" }, { "n": "粤语", "v": "/lang/粤语" }, { "n": "闽南语", "v": "/lang/闽南语" }, { "n": "韩语", "v": "/lang/韩语" }, { "n": "日语", "v": "/lang/日语" }, { "n": "其它", "v": "/lang/其它" }] }, { "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }],
    "3": [{ "key": "地区", "name": "地区", "value": [{ "n": "全部", "v": "" }, { "n": "内地", "v": "/area/内地" }, { "n": "港台", "v": "/area/港台" }, { "n": "日韩", "v": "/area/日韩" }, { "n": "欧美", "v": "/area/欧美" }] }, { "key": "年份", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "/year/2025" }, { "n": "2024", "v": "/year/2024" }, { "n": "2023", "v": "/year/2023" }, { "n": "2022", "v": "/year/2022" }, { "n": "2021", "v": "/year/2021" }, { "n": "2020", "v": "/year/2020" }, { "n": "2019", "v": "/year/2019" }, { "n": "2018", "v": "/year/2018" }, { "n": "2017", "v": "/year/2017" }, { "n": "2016", "v": "/year/2016" }, { "n": "2015", "v": "/year/2015" }, { "n": "2014", "v": "/year/2014" }, { "n": "2013", "v": "/year/2013" }, { "n": "2012", "v": "/year/2012" }, { "n": "2011", "v": "/year/2011" }, { "n": "2010", "v": "/year/2010" }, { "n": "2009", "v": "/year/2009" }, { "n": "2008", "v": "/year/2008" }, { "n": "2007", "v": "/year/2007" }, { "n": "2006", "v": "/year/2006" }, { "n": "2005", "v": "/year/2005" }, { "n": "2004", "v": "/year/2004" }, { "n": "2003", "v": "/year/2003" }, { "n": "2002", "v": "/year/2002" }, { "n": "2001", "v": "/year/2001" }, { "n": "2000", "v": "/year/2000" }] }, { "key": "剧情", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "教育", "v": "/class/教育" }, { "n": "选秀", "v": "/class/选秀" }, { "n": "情感", "v": "/class/情感" }, { "n": "访谈", "v": "/class/访谈" }, { "n": "播报", "v": "/class/播报" }, { "n": "旅游", "v": "/class/旅游" }, { "n": "音乐", "v": "/class/音乐" }, { "n": "美食", "v": "/class/美食" }, { "n": "纪实", "v": "/class/纪实" }, { "n": "曲艺", "v": "/class/曲艺" }, { "n": "生活", "v": "/class/生活" }, { "n": "游戏互动", "v": "/class/游戏互动" }, { "n": "财经", "v": "/class/财经" }, { "n": "求职", "v": "/class/求职" }, { "n": "记录", "v": "/class/记录" }, { "n": "音乐", "v": "/class/音乐" }] }, { "key": "语言", "name": "语言", "value": [{ "n": "全部", "v": "" }, { "n": "中国大陆", "v": "/lang/中国大陆" }, { "n": "英语", "v": "/lang/英语" }, { "n": "粤语", "v": "/lang/粤语" }, { "n": "闽南语", "v": "/lang/闽南语" }, { "n": "韩语", "v": "/lang/韩语" }, { "n": "日语", "v": "/lang/日语" }, { "n": "其它", "v": "/lang/其它" }] }, { "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }],
    "4": [{ "key": "地区", "name": "地区", "value": [{ "n": "全部", "v": "" }, { "n": "中国大陆", "v": "/area/中国大陆" }, { "n": "日本", "v": "/area/日本" }, { "n": "欧美", "v": "/area/欧美" }, { "n": "其他", "v": "/area/其他" }] }, { "key": "年份", "name": "年份", "value": [{ "n": "全部", "v": "" }, { "n": "2025", "v": "/year/2025" }, { "n": "2024", "v": "/year/2024" }, { "n": "2023", "v": "/year/2023" }, { "n": "2022", "v": "/year/2022" }, { "n": "2021", "v": "/year/2021" }, { "n": "2020", "v": "/year/2020" }, { "n": "2019", "v": "/year/2019" }, { "n": "2018", "v": "/year/2018" }, { "n": "2017", "v": "/year/2017" }, { "n": "2016", "v": "/year/2016" }, { "n": "2015", "v": "/year/2015" }, { "n": "2014", "v": "/year/2014" }, { "n": "2013", "v": "/year/2013" }, { "n": "2012", "v": "/year/2012" }, { "n": "2011", "v": "/year/2011" }, { "n": "2010", "v": "/year/2010" }, { "n": "2009", "v": "/year/2009" }, { "n": "2008", "v": "/year/2008" }, { "n": "2007", "v": "/year/2007" }, { "n": "2006", "v": "/year/2006" }, { "n": "2005", "v": "/year/2005" }, { "n": "2004", "v": "/year/2004" }, { "n": "2003", "v": "/year/2003" }, { "n": "2002", "v": "/year/2002" }, { "n": "2001", "v": "/year/2001" }, { "n": "2000", "v": "/year/2000" }] }, { "key": "剧情", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "情感", "v": "/class/情感" }, { "n": "科幻", "v": "/class/科幻" }, { "n": "热血", "v": "/class/热血" }, { "n": "推理", "v": "/class/推理" }, { "n": "搞笑", "v": "/class/搞笑" }, { "n": "冒险", "v": "/class/冒险" }, { "n": "萝莉", "v": "/class/萝莉" }, { "n": "校园", "v": "/class/校园" }, { "n": "动作", "v": "/class/动作" }, { "n": "机战", "v": "/class/机战" }, { "n": "运动", "v": "/class/运动" }, { "n": "战争", "v": "/class/战争" }, { "n": "少年", "v": "/class/少年" }, { "n": "少女", "v": "/class/少女" }, { "n": "社会", "v": "/class/社会" }, { "n": "原创", "v": "/class/原创" }, { "n": "亲子", "v": "/class/亲子" }, { "n": "益智", "v": "/class/益智" }, { "n": "励志", "v": "/class/励志" }, { "n": "其他", "v": "/class/其他" }] }, { "key": "语言", "name": "语言", "value": [{ "n": "全部", "v": "" }, { "n": "国语", "v": "/lang/国语" }, { "n": "英语", "v": "/lang/英语" }, { "n": "粤语", "v": "/lang/粤语" }, { "n": "闽南语", "v": "/lang/闽南语" }, { "n": "韩语", "v": "/lang/韩语" }, { "n": "日语", "v": "/lang/日语" }, { "n": "其它", "v": "/lang/其它" }] }, { "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }],
    "20": [{ "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }],
    "21": [{ "key": "排序", "name": "排序", "value": [{ "n": "按最新", "v": "/by/time" }, { "n": "按最热", "v": "/by/hits" }, { "n": "按评分", "v": "/by/score" }] }]
  },
  filter_url: '{{fl.地区}}{{fl.排序}}{{fl.剧情}}/id/fyclass{{fl.语言}}/page/fypage{{fl.年份}}',
  lazy: `js:
  let html = request(input);
  let iframe = html.match(/<iframe[^>]*src="(https[^"]+)"/);
  let player = html.match(/var player_\w+\s*=\s*({[\s\S]*?})\s*;</);
  if (iframe) {
    let iframeUrl = iframe[1];
    let clickScript = "document.querySelector('#playleft iframe').contentDocument.querySelector('#start').click()";
    input = { parse: 1, url: iframeUrl, js: clickScript, click: clickScript };
  } 
  else if (player) {
    try {
      let json = JSON5.parse(player[1]);
      let url = json.url;
      if (json.encrypt == '1') url = unescape(url);
      if (json.encrypt == '2') url = unescape(base64Decode(url));
      if (json.from === 'BXD' && url.includes('BX-')) {
        url = 'https://jx.uniuui.com/player/ec.php?code=qw&from=BX&if=1&url=' + url;
      }
      if (/\.(m3u8|mp4)/.test(url)) {
        input = { parse: 0, jx: 0, url: url };
      } else {
        input = { parse: 0, jx: 1, url: url };
      }
    } catch (e) {
      console.log('解析错误:' + e.message);
    }
  }
  else {
    let clickScript = "document.querySelector('#start').click()";
    input = { parse: 1, url: input, js: clickScript, click: clickScript };
  }`,
  limit: 6,
  double: true,
  推荐: '.content;.myui-vodbox-content;.card-info .title&&Text;img&&src;.tag.text-overflow&&Text;a&&href',
  一级: '.show-vod-list .myui-vodbox-content;.card-info .title&&Text;img&&src;.tag.text-overflow&&Text;a&&href',
  二级: {
    title: '.detail-box .title--span&&Text;.tag:eq(1)&&Text',
    img: '.img-box .lazyload&&data-original',
    desc: '.tags&&Text;.other-box .item:eq(2)&&Text;.other-box .item:eq(1)&&Text;.director:eq(1)&&Text;.director:eq(0)&&Text',
    content: '.wrapper_more_text&&Text',
    tabs: '.nav.nav-btn&&li',
    lists: '.lists-box:eq(#id) a',
  },
  搜索: '.show-vod-list .myui-vodbox-content;.card-info .title&&Text;img&&src;.tag.text-overflow&&Text;a&&href',
}