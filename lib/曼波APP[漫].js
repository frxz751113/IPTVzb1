function Decrypt(word) {
    const key = CryptoJS.enc.Utf8.parse("66dc309cbeeca454");
    const iv = CryptoJS.enc.Utf8.parse("66dc309cbeeca454");
    let decrypt = CryptoJS.AES.decrypt(word, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7,
    });
    let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
    return decryptedStr.toString();
  }
  
  
  function Encrypt(word) {
    const key = CryptoJS.enc.Utf8.parse("66dc309cbeeca454");
    const iv = CryptoJS.enc.Utf8.parse("66dc309cbeeca454");
    let encrypt = CryptoJS.AES.encrypt(word, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7,
    });
    let encryptedStr = encrypt.toString(CryptoJS.enc.base64);
    return encryptedStr.toString();
  }
  
  globalThis.Encrypt = Encrypt
  globalThis.Decrypt = Decrypt
  var rule = {
    title: '曼波APP',
    host: 'https://app.omofun1.top',
    url: '/api.php/getappapi.index/typeFilterVodList?type_id=fyclass&page=fypage&fyfilter',
    searchUrl: '/api.php/getappapi.index/searchList?keywords=**&type_id=0&page=1',
    detailUrl: "/api.php/getappapi.index/vodDetail?vod_id=fyid",
    homeUrl: '/api.php/getappapi.index/typeFilterVodList?type_id=21&page=1&area=全部&year=&sort=最热&lang=全部&class=全部',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    filter_url: 'area=全部&year={{fl._year}}&sort={{fl._sort or "最新"}}&lang=全部&class=全部',
    filter: {
      "20": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "最新" }, { "n": "最热", "v": "最热" }, { "n": "最赞", "v": "最赞" }], "key": "order", "name": "排序" }],
      "21": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "最新" }, { "n": "最热", "v": "最热" }, { "n": "最赞", "v": "最赞" }], "key": "_order", "name": "排序" }],
      "22": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "最新" }, { "n": "最热", "v": "最热" }, { "n": "最赞", "v": "最赞" }], "key": "order", "name": "排序" }],
      "23": [{ "value": [{ "n": "全部", "v": "" }, { "n": "2024", "v": "2024", }, { "n": "2023", "v": "2023" }, { "n": "2022", "v": "2022" }, { "n": "2021", "v": "2021" }, { "n": "2020", "v": "2020" }, { "n": "2019", "v": "2019" }, { "n": "2018", "v": "2018" }, { "n": "2017", "v": "2017" }, { "n": "2016", "v": "2016" }, { "n": "2015", "v": "2015" }, { "n": "2014", "v": "2014" }, { "n": "2013", "v": "2013" }, { "n": "2012", "v": "2012" }, { "n": "2011", "v": "2011" }, { "n": "2010", "v": "2010" }, { "n": "2009", "v": "2009" }, { "n": "2008", "v": "2008" }, { "n": "2007", "v": "2007" }, { "n": "2006", "v": "2006" }, { "n": "2005", "v": "2005" }, { "n": "2004", "v": "2004" }, { "n": "2003", "v": "2003" }, { "n": "2002", "v": "2002" }, { "n": "2001", "v": "2001" }, { "n": "2000", "v": "2000" }], "key": "_year", "name": "年份" }, { "value": [{ "n": "最新", "v": "最新" }, { "n": "最热", "v": "最热" }, { "n": "最赞", "v": "最赞" }], "key": "order", "name": "排序" }]
    },
    class_name: '日本动漫&国产动漫&动漫电影&欧美动漫',
    class_url: '20&21&22&23',
    headers: {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) cyc-desktop/1.0.8 Chrome/128.0.6613.36 Electron/32.0.1 Safari/537.36"
    },
    timeout: 5000,
    play_parse: true,
    lazy: $js.toString(() => {
      var result = {}
      result.parse = 0;
      result.jx = 0;
      if (/mp4|m3u8/.test(input) && !/senhewenhua.com/.test(input)) {
        var url = input
      } else if (input.includes(rule.host)) {
        var html = request(input.split("?")[0], {
          body: input.split("?")[1],
          method: "POST"
        });
        if (JSON.parse(html).code == "1") {
          try {
            var html = Decrypt(JSON.parse(html).data);
            var html2 = JSON.parse(html).json;
            var html3 = JSON.parse(html2);
            if (html3.code != "404") {
              var url = html3.url
            }
          } catch (e) {
            log(e.message);
          }
        }
      } else {
        var jxdata = request(input);
        var url = JSON.parse(jxdata).url;
      }
      result.url = url
      input = result
    }),
    推荐: $js.toString(() => {
      var M = input.split("?")
      var html = request(M[0], {
        body: M[1],
        method: "POST"
      });
      var html1 = Decrypt(JSON.parse(html).data);
      var d = []
      var list = JSON.parse(html1).recommend_list;
      list.forEach(item => {
        d.push({
          title: item.vod_name,
          desc: item.vod_remarks,
          pic_url: item.vod_pic,
          url: item.vod_id,
        })
      })
      setResult(d)
    }),
    一级: $js.toString(() => {
      var M = input.split("?")
      var html = request(M[0], {
        body: M[1],
        method: "POST"
      });
      var html1 = Decrypt(JSON.parse(html).data);
      var d = []
      var list = JSON.parse(html1).recommend_list;
      list.forEach(item => {
  
        d.push({
          title: item.vod_name,
          desc: item.vod_remarks,
          pic_url: item.vod_pic,
          url: item.vod_id,
        })
      })
      setResult(d)
    }),
    二级: $js.toString(() => {
      VOD = {};
      var M = input.split("?")
      var html = request(M[0], {
        body: M[1],
        method: "POST"
      });
      var html1 = Decrypt(JSON.parse(html).data);
      var data = JSON.parse(html1);
      var items = data.vod;
      VOD = data.vod;
      var arts = data.vod_play_list;
      var tabs = [];
      var parses = [];
      var lists = [];
      arts.forEach(item => {
        tabs.push(item.player_info.show);
        parses.push(item.player_info.parse);
        lists.push(item.urls);
      });
      var result = [];
      try {
        for (var i in lists) {
          var playlist = [];
          var list = lists[i]
          for (let item of list) {
            let title = item.name;
            let url = item.url;
            let parse = parses[i]
            if (/m3u8|mp4/.test(url)) {
              if (/senhewenhua/.test(url)) {
                playlist.push(title + '$https://json.xn--pxt92gb0ku1kjqwf9h3sm.cn/zijian/tt.php?url=' + url.replace("11451", "8080"))
              } else {
                playlist.push(title + '$' + url)
              }
            } else if (/http/.test(parse)) {
              playlist.push(title + '$' + parse + url)
            } else {
  
              playlist.push(title + '$' + rule.host + `/api.php/getappapi.index/vodParse?parse_api=${parse}&url=${Encrypt(url)}&token=${item.token}`);
            }
          }
          let vod_play_url = playlist.join("#")
          result.push(vod_play_url)
        }
        VOD.vod_play_url = result.join("$$$");
        VOD.vod_play_from = tabs.join("$$$")
      } catch (e) {
        log("解析片名海报等基础信息发生错误:" + e.message)
      }
    }),
    搜索: $js.toString(() => {
      var M = input.split("?")
      var html = request(M[0], {
        body: M[1],
        method: "POST"
      });
      var html1 = Decrypt(JSON.parse(html).data);
      var d = []
      var list = JSON.parse(html1).search_list;
      list.forEach(item => {
        d.push({
          title: item.vod_name,
          desc: item.vod_remarks,
          pic_url: item.vod_pic,
          url: item.vod_id,
        })
      })
      setResult(d)
    }),
  }