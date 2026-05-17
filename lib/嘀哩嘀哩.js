Object.assign(muban.mxpro.二级, {
   tab_text: 'div--small&&Text',
});
var rule = {
   模板: 'mxpro',
   title: '嘀哩嘀哩',
   host: 'http://www.dilidili23.com',
   url: '/index.php/vod/show/id/fyclass/fyfilter.html',
   searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
   class_parse: '.navbar-items li:gt(0):lt(8);a&&Text;a&&href;/(\\d+).html',
   lazy: $js.toString(() => {
      let html = JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);
      let url = html.url;
      if (html.encrypt == '1') {
         url = unescape(url)
      } else if (html.encrypt == '2') {
         url = unescape(base64Decode(url))
      }
      if (/\.m3u8/.test(url)) {
         let body = request(url);
         let lines = body.split('\n');
         let m3u8Url = null;
         for (let line of lines) {
            line = line.trim();
            if (line.endsWith('.m3u8')) {
               m3u8Url = urljoin(url, line);
               console.log(m3u8Url);
               break;
            }
         }
         input = {
            jx: 0,
            url: m3u8Url || url,
            parse: 0
         };
      } else {
         input = {
            jx: tellIsJx(url),
            url: url,
            parse: 0
         };
      }
   }),
   filter: {
      '1': [{ key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '日本动漫', v: '/class/日本动漫', }, { n: '日本', v: '/class/日本', }, { n: '国产动漫', v: '/class/国产动漫', }, { n: '中国动漫', v: '/class/中国动漫', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '日语', v: '/lang/日语', }, { n: '国语', v: '/lang/国语', }, { n: '英语', v: '/lang/英语', }, { n: '中文', v: '/lang/中文', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021.2019', v: '/year/2021.2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', }, { n: '1999', v: '/year/1999', }, { n: '1998', v: '/year/1998', },], }, { key: '排序', name: '排序', value: [{ n: '时间排序', v: '/by/time', }, { n: '人气排序', v: '/by/hits', }, { n: '评分排序', v: '/by/score', },], },],
      '2': [{ key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021.2019', v: '/year/2021.2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', }, { n: '1999', v: '/year/1999', }, { n: '1998', v: '/year/1998', },], }, { key: '排序', name: '排序', value: [{ n: '时间排序', v: '/by/time', }, { n: '人气排序', v: '/by/hits', }, { n: '评分排序', v: '/by/score', },], },],
      '3': [{ key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021.2019', v: '/year/2021.2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', }, { n: '1999', v: '/year/1999', }, { n: '1998', v: '/year/1998', },], }, { key: '排序', name: '排序', value: [{ n: '时间排序', v: '/by/time', }, { n: '人气排序', v: '/by/hits', }, { n: '评分排序', v: '/by/score', },], },],
      '4': [{ key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021.2019', v: '/year/2021.2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', }, { n: '1999', v: '/year/1999', }, { n: '1998', v: '/year/1998', },], }, { key: '排序', name: '排序', value: [{ n: '时间排序', v: '/by/time', }, { n: '人气排序', v: '/by/hits', }, { n: '评分排序', v: '/by/score', },], },],
      '5': [{ key: '排序', name: '排序', value: [{ n: '时间排序', v: '/by/time', }, { n: '人气排序', v: '/by/hits', }, { n: '评分排序', v: '/by/score', },], },],
   },
   filter_url: '{{fl.排序}}{{fl.剧情}}{{fl.语言}}/page/2{{fl.年份}}',
   filterable: 1,
}
