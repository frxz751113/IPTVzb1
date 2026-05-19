var rule = {
  title: '172MV',
  host: 'https://m.172mixdj.com',
  url: '/categories/fyfilter',
  searchUrl: '/searches?s=**',
  searchable: 2,
  quickSearch: 2,
  filterable: 1,
  filter: 'H4sIAAAAAAAAA6tWqirPLVOyiq5Wyk6tVLJSer5x99N53Uo6SnmJuanI/LLEnNJUsMI8oPDT1hUvm1eAhIEcsBG1OhAZn8Rsj/zS4lSoXE5idgaYC5MPKMpPR1ZQAOSjqnArzcuuRFaSBhJAVeOak5pcUpSPrCoVIoSqziUxLzlV3zmnNAmqKgUkkAzi18aCFEF8/axv0tNd/Qhfw/movn65e8aLdUugJunnpZbD7XnevPbldFh46BfkJFbCpZ71rXjROwEmlZaZh3Dd02lznq1ZBJPKycxGSD3Z0f1i716YVEp+eR7IwbE6SpWUx1cl/viCS4Vl5iUiy5UB+XjjkUAUEhF7QzVWqsqTi5FiZci4vBYA9zmgRwEEAAA=',
  filter_url: '{{fl.类型}}{{fl.排序}}',
  filter_def: {zwmv:{类型:"zwmv"},ywmv:{类型:"ywmv"},zwcs:{类型:"zwcs"},},
  headers: {'User-Agent': 'PC_UA',},
  timeout: 5000,
  class_name: '中文MV舞曲&英文MV舞曲&中文MV串烧',
  class_url: 'zwmv&ywmv&zwcs',
  play_parse: true,
  double: true,
  lazy: `js:
    let html = request(input);
    let hconf = html.match(/r player_.*?=(.*?)</)[1];
    let json = JSON5.parse(hconf);
    let url = json.url;
    if (json.encrypt == '1') {
      url = unescape(url);
    } else if (json.encrypt == '2') {
     url = unescape(base64Decode(url));
    }
    if (/\\.(m3u8|mp4|m4a|mp3)/.test(url)) {
      input = {
        parse: 0,
        jx: 0,
       url: url,
      };
    } else {
      input;
    }`,
  推荐: '.js-slick;.post-item;a.post-permalink&&title;img&&data-src;.video-length&&Text;a&&href;.d-flex&&Text',
  一级: 'body&&.infinite-item;a&&title;img&&data-src;.video-length&&Text;a&&href',
  二级: '*',
  tab_rename: {'道长在线': '在线播放',},
  搜索: '*',
}
