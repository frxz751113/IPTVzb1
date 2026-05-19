var rule = {
  title: '音乐磁场',
  host: 'https://hifini.net/',
  url: '/forum-fyclass-fypage.htm?orderby=lastpid&follow=0',
  searchUrl: '/search-**-1-0-fypage.htm',
  class_parse: '.navbar-nav li;a&&Text;a&&href;forum-(.*/?).htm',
  searchable: 2,
  quickSearch: 0,
  filterable: 0,
  headers: {
    'User-Agent': 'MOBILE_UA',
  },
  play_parse: true,
  lazy: `
let html = request(input);

// 1️⃣ 直链
let m = html.match(/url:\\s*"(https?:[^"]+)"/);
let playUrl = m ? m[1] : input;

// 2️⃣ 歌词
let lyric = [];
let ps = html.match(/<p>(.*?)<\\/p>/g) || [];
for(let p of ps){
  let t = p.replace(/<[^>]+>/g,'').trim();
  if(!t) continue;
  if(/下载链接|提取码|隐藏内容/.test(t)) break;
  lyric.push(t);
}

input = {
  parse: 0,
  url: playUrl,
  lyric: lyric.join('\\n')
};
`,
  limit: 6,
  double: true,
  推荐: '.cbox_list;*;*;*;*;*',
  一级: 'ul.list-unstyled li:gt(2);.subject&&Text;img&&src;.media-body&&Text;.subject a&&href',
  二级: '*',
  搜索: '*',
}
