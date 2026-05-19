var rule = {
    title: '嘟嘟短剧[短]',
    host: 'https://api-v2.cenguigui.cn',
    homeUrl: '/api/duanju/baidu/?name=热播&page=1',
    url: '/api/duanju/baidu/?name=fyclass&page=fypage',
    searchUrl: '/api/duanju/baidu/?name=**&page=fypage',
    detailUrl: '/api/duanju/baidu/?id=fyid',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    },
    play_parse: true,
    class_parse: $js.toString(() => {
    let classes = [
    { type_id: '热播', type_name: '🎬热播' },
    { type_id: '新剧', type_name: '🎬新剧' },
    { type_id: '都市', type_name: '🎬都市' },
    { type_id: '穿越', type_name: '🎬穿越' },
    { type_id: '重生', type_name: '🎬重生' },
    { type_id: '赘婿', type_name: '🎬赘婿' },
    { type_id: '逆袭', type_name: '🎬逆袭' },
    { type_id: '霸总', type_name: '🎬霸总' },
    { type_id: '职场', type_name: '🎬职场' },
    { type_id: '异能', type_name: '🎬异能' },
    { type_id: '神医', type_name: '🎬神医' },
    { type_id: '系统', type_name: '🎬系统' },
    { type_id: '总裁', type_name: '🎬总裁' },
    { type_id: '豪门', type_name: '🎬豪门' },
    { type_id: '神豪', type_name: '🎬神豪' },
    { type_id: '校园', type_name: '🎬校园' },
    { type_id: '青春', type_name: '🎬青春' },
    { type_id: '马甲', type_name: '🎬马甲' },
    { type_id: '年代', type_name: '🎬年代' },
    { type_id: '闪婚', type_name: '🎬闪婚' },
    { type_id: '战神', type_name: '🎬战神' },
    { type_id: '女主', type_name: '🎬女主' },        
    { type_id: '修仙', type_name: '🎬修仙' },
    { type_id: '亲情', type_name: '🎬亲情' },       
    { type_id: '虐恋', type_name: '🎬虐恋' },
    { type_id: '追妻', type_name: '🎬追妻' },
    { type_id: '萌宝', type_name: '🎬萌宝' },        
    { type_id: '古风', type_name: '🎬古风' },
    { type_id: '传承', type_name: '🎬传承' },
    { type_id: '甜宠', type_name: '🎬甜宠' },
    { type_id: '奇幻', type_name: '🎬奇幻' },
    { type_id: '爱情', type_name: '🎬爱情' },
    { type_id: '乡村', type_name: '🎬乡村' },
    { type_id: '历史', type_name: '🎬历史' },
    { type_id: '王妃', type_name: '🎬王妃' },
    { type_id: '高手', type_name: '🎬高手' },
    { type_id: '娱乐', type_name: '🎬娱乐' },
    { type_id: '联合', type_name: '🎬联合' },
    { type_id: '破镜', type_name: '🎬破镜' },
    { type_id: '暗恋', type_name: '🎬暗恋' },
    { type_id: '民国', type_name: '🎬民国' },
    { type_id: '冤家', type_name: '🎬冤家' },    
    { type_id: '真假', type_name: '🎬真假' },
    { type_id: '龙王', type_name: '🎬龙王' },    
    { type_id: '穿书', type_name: '🎬穿书' },
    { type_id: '女帝', type_name: '🎬女帝' },
    { type_id: '团宠', type_name: '🎬团宠' },    
    { type_id: '玄幻', type_name: '🎬玄幻' },
    { type_id: '仙侠', type_name: '🎬仙侠' },
    { type_id: '青梅', type_name: '🎬青梅' },
    { type_id: '悬疑', type_name: '🎬悬疑' },
    { type_id: '推理', type_name: '🎬推理' },
    { type_id: '皇后', type_name: '🎬皇后' },
    { type_id: '替身', type_name: '🎬替身' },
    { type_id: '大叔', type_name: '🎬大叔' },
    { type_id: '喜剧', type_name: '🎬喜剧' },
    { type_id: '剧情', type_name: '🎬剧情' }
        ];
    input = classes;
    }),
    lazy: $js.toString(() => {
        let item = JSON.parse(fetch(`${HOST}/api/duanju/baidu/?video_id=${input}`));
        let qualities = item.data.qualities || [];
        const priority = { '1080p': 3, 'sc': 2, 'sd': 1 };
        qualities.sort((a, b) => (priority[b.quality] || 0) - (priority[a.quality] || 0));
        let urls = [];
        qualities.forEach(q => {
            urls.push(q.title);
            urls.push(q.download_url);
        });
        input = {
            parse: 0,
            url: urls
        };
    }),
    推荐: 'json:data;title;cover;totalChapterNum;id',
    一级: 'json:data;title;cover;totalChapterNum;id',
    二级: $js.toString(() => {
        let item = JSON.parse(fetch(input));
        VOD = {
            vod_name: item.title,
            vod_pic: item.data[0].cover,
            vod_year: item.time.split('-')[0],
            vod_area: '中国',
            vod_remarks: '更新至' + item.total + '集',
        };
        let playUrls = item.data.map(item => `${item.title}$${item.video_id}`);
        VOD.vod_play_from = '嘟嘟短剧';
        VOD.vod_play_url = playUrls.join("#");
    }),            
    搜索: 'json:data;title;cover;totalChapterNum;id',
}