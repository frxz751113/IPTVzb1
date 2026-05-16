/*
@header({
  searchable: 2,
  filterable: 0,
  quickSearch: 0,
  title: '米兔音乐',
  '类型': '影视',
  lang: 'dr2'
})
*/

var rule = {
  title: '米兔音乐',
  host: 'https://www.qqmp3.vip',

  url: '/api/fyclass',
  searchUrl: '/api/songs.php?type=search&keyword=**',

  class_name: '热门歌曲&新歌曲&随机歌曲',
  class_url: 'songs.php&songs.php?type=new&songs.php?type=rand',

  searchable: 2,
  quickSearch: 0,
  filterable: 0,

  headers: {
    'User-Agent': 'MOBILE_UA',
  },

  play_parse: true,
  limit: 6,
  double: true,
  推荐: '*',
  // 列表页
  一级: 'json:data;name;pic;artist;rid',
  二级:  '*',
  搜索: 'json:data;name;pic;artist;rid',

  /**
   * 播放直链解析
   */
  lazy: $js.toString(() => {
    let rid = input.match(/api\/([^/?]+)/)[1];
    // 真实解析接口
    let api = 'https://www.qqmp3.vip/api/kw.php?rid=' + rid;

    let json = request(api);
    let data = JSON.parse(json);
    if (data.code === 200 && data.data && data.data.url) {
        const lrc = data.data.lrc || '';
        const srt = lrcToSrt(lrc);
        const danmu = srtToDanmu(srt);
        input = {
            parse: 0,              // 关闭嗅探
            url: data.data.url,    // MP3直链
            header: {
                'User-Agent': 'MOBILE_UA',
                'Referer': 'https://www.qqmp3.vip/'
            },
            danmaku: danmu,
            subs: [
                {
                    'format': 'application/x-subrip',
                    'name': MD5(data.data.url) + '.srt',
                    'data': srt,
                    'selected': true
                }
            ]
        };
    }
  }),
};