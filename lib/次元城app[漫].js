var rule = {
    title: '次元城',
    host: 'https://pc.cycback.org',
    url: '/video/query?page=fypage&limit=20&tid=fyclass&fyfilter',
    searchUrl: '/video/search?text=**&pg=1&limit=30',
    homeUrl: '/video/query?page=1&limit=20&tid=20&class=&year=&order=time',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    filter_url: 'class={{fl._class}}&year={{fl._year}}&order=time',
    filter: {
      "20": [{ "value": [{ "n": "全部", "v": "" }, { "n": "原创", "v": "原创" }, { "n": "漫画改", "v": "漫画改" }, { "n": "小说改", "v": "小说改" }, { "n": "游戏改", "v": "游戏改" }, { "n": "特摄", "v": "特摄" }, { "n": "热血", "v": "热血" }, { "n": "穿越", "v": "穿越" }, { "n": "奇幻", "v": "奇幻" }, { "n": "战斗", "v": "战斗" }, { "n": "搞笑", "v": "搞笑" }, { "n": "日常", "v": "日常" }, { "n": "科幻", "v": "科幻" }, { "n": "治愈", "v": "治愈" }, { "n": "校园", "v": "校园" }, { "n": "泡面", "v": "泡面" }, { "n": "恋爱", "v": "恋爱" }, { "n": "少女", "v": "少女" }, { "n": "魔法", "v": "魔法" }, { "n": "冒险", "v": "冒险" }, { "n": "历史", "v": "历史" }, { "n": "架空", "v": "架空" }, { "n": "机战", "v": "机战" }, { "n": "运动", "v": "运动" }, { "n": "励志", "v": "励志" }, { "n": "音乐", "v": "音乐" }, { "n": "推理", "v": "推理" }, { "n": "社团", "v": "社团" }, { "n": "智斗", "v": "智斗" }, { "n": "催泪", "v": "催泪" }, { "n": "美食", "v": "美食" }, { "n": "偶像", "v": "偶像" }, { "n": "乙女", "v": "乙女" }, { "n": "职场", "v": "职场" }], "key": "_class", "name": "类型" }, { "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "time" }, { "n": "最热", "v": "hits" }, { "n": "好评", "v": "score" }], "key": "order", "name": "排序" }],
      "21": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "time" }, { "n": "最热", "v": "hits" }, { "n": "好评", "v": "score" }], "key": "_order", "name": "排序" }]
    },
    class_name: 'TV动画&剧场版',
    class_url: '20&21',
    headers: {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) cyc-desktop/1.0.8 Chrome/128.0.6613.36 Electron/32.0.1 Safari/537.36"
    },
    timeout: 5000,
    play_parse: true,
    lazy: `js:
      var html=request(input);
      var result={};
      result.parse= 0;
      result.jx=0;
      result.url=JSON.parse(html).url+"#.mp4#isVideo=true#";
      input = result`,
    推荐: 'json:data;name;pic;score;vod_id',
    一级: 'json:data;name;pic;score;vod_id',
    二级: $js.toString(() => {
      VOD = {};
      let vod_id = input.replace("https://pc.cycback.org/video/", "");
      let detailUrl = 'https://pc.cycback.org/video/info/' + vod_id;
      let html = request(detailUrl);
      let items = JSON.parse(html).data;
      VOD = {
        type_name: items.vod_class,
        vod_actor: items.vod_actor,
        vod_director: items.vod_director,
        vod_area: "",
        vod_content: items.vod_blurb,
        vod_name: items.vod_name,
        vod_remarks: items.vod_remarks,
        vod_pic: items.vod_pic,
        vod_year: items.vod_year,
      }
      let result = [];
      let from = []
      try {
        for (var i in items.vod_play_from) {
          from.push(items.vod_play_from[0].name);
          let playlist = [];
          let res = request('https://pc.cycback.org/video/play_url?id=' + vod_id + '&from=' + items.vod_play_from[i].code);
          let data = JSON.parse(res).data;
          for (let item of data) {
            let title = item.name;
            let url = item.url;
            playlist.push(title + '$' + url);
          }
          let vod_play_url = playlist.join("#")
          result.push(vod_play_url)
        }
  
        VOD.vod_play_url = result.join("$$$");
        VOD.vod_play_from = from.join("$$$")
      } catch (e) {
        log("解析片名海报等基础信息发生错误:" + e.message)
      }
    }),
    搜索: 'json:data;name;pic;year;vod_id',
  }