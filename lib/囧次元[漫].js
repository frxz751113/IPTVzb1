
function Headers() {
    let d = [];
    var timestamp = new Date().getTime() / 1000;
    var t = timestamp.toString().split('.')[0];
  
    const characterSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    //随机生成10位字符串
    const randomString = Array.from({
      length: 10
    }, () => characterSet[Math.floor(Math.random() * characterSet.length)]).join('');
    //反转10位字符串用于s参数.后边拼接的字符串
    const reversedString = randomString.split('').reverse().join('');
  
    var s = md5('jocy' + '&' + t + '&' + randomString) + '.' + reversedString
  
    return {
      "User-Agent": "Mozilla/5.0 (Linux; Android 15; 2407FRK8EC Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36",
      "Accept": "application/json, text/plain, */*",
      "s": s,
      "t": t,
      "x-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMmJkOTYzMjMtMjc2My00Y2U2LWIxZDgtNjY0ODhlMWU0ZjdmIiwiQnVmZmVyVGltZSI6ODY0MDAwMDAwMDAwMDAsImV4cCI6MTc0NTMwNjgwMywibmJmIjoxNzQ0NzAyMDAzfQ.UKjp-l_6rjVWpWP-w0fw4H549nrZhFkbTkRj-5EZekY"
    };
  
  
  }
  globalThis.Headers = Headers
  var rule = {
    title: '囧次元',
    host: 'https://jocy-api.6b7.xyz',
    url: '/app/video/list?area=&channel=fyclass&enablePagination=true&limit=18&page=fypage&fyfilter',
  
    searchUrl: '/app/video/search?key=**&limit=6&page=fypage',
    detailUrl: '/app/video/detail?id=fyid',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    filter_url: 'sort={{fl._order or "addtime"}}&type=&year={{fl._year}}',
    filter: {
      "2": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "addtime" }, { "n": "最热", "v": "hits" }, { "n": "好评", "v": "gold" }], "key": "_order", "name": "排序" }],
      "1": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "addtime" }, { "n": "最热", "v": "hits" }, { "n": "好评", "v": "gold" }], "key": "_order", "name": "排序" }],
      "26": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "addtime" }, { "n": "最热", "v": "hits" }, { "n": "好评", "v": "gold" }], "key": "_order", "name": "排序" }]
    },
    class_name: '国漫&日漫&动漫电影',
    class_url: '2&1&26',
    headers: {
      "User-Agent": "Mozilla/5.0 (Linux; Android 15; V2338A Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.71 Mobile Safari/537.36"
    },
    timeout: 5000,
    play_parse: true,
    lazy: `js:   
      var result={};
      result.parse= 0;
      result.jx=0;
       var play = JSON.parse(request(input,{headers:Headers()}))
                  if (play.type == 'multi') {
                      result.url = play.url.multi[0].url + "#isVideo=true#"
                  } else {
                      result.url= play.url.single + "#isVideo=true#"
                  }
      input = result`,
    一级: $js.toString(() => {
      let html = request(input, { headers: Headers() });
      let data = JSON.parse(html).data.items;
      data.forEach(it => {
        d.push({
          url: it.id,
          title: it.name,
          img: it.pic,
          desc: it.continu,
        });
      });
      setResult(d);
    }),
    二级: $js.toString(() => {
      VOD = {};
      let d = [];
      let html = request(input, { headers: Headers() });
      let data = JSON.parse(html).data;
      VOD = {
        type_name: data.type,
        vod_actor: data.actor,
        vod_director: data.director,
        vod_area: data.area,
        vod_content: data.content,
        vod_name: data.name,
        vod_remarks: data.continu,
        vod_pic: data.pic,
        vod_year: data.year,
      }
      try {
        var parts = data.parts;
        var part = parts[0].part
        var lists = [];
        part.forEach(it => {
          lists.push(it + "$https://jocy-api.6b7.xyz/app/video/play?id=" + data.id + "&part=" + it + "&play=" + parts[0].play);
        });
        VOD.vod_play_url = lists.join("#");
        VOD.vod_play_from = parts[0].play_zh
      } catch (e) {
        log("解析片名海报等基础信息发生错误:" + e.message)
      }
    }),
    搜索: $js.toString(() => {
      let d = [];
      let html = request(input, { headers: Headers() });
      let data = JSON.parse(html).data.items;
      data.forEach(it => {
        d.push({
          url: it.id,
          title: it.name,
          img: it.pic,
          desc: it.continu,
        });
      });
      setResult(d);
    })
  }