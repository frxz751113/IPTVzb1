var rule = {
    title: '星之阁[短]',
    host: 'https://api.xingzhige.com',
    homeUrl: '/API/playlet/?keyword=推荐榜&page=1',
    url: '/API/playlet/?keyword=fyclass&page=fypage',
    searchUrl: '/API/playlet/?keyword=**&page=fypage',
    detailUrl:'/API/playlet/?book_id=fyid',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {
        'User-Agent': MOBILE_UA, 
        'Origin': HOST,
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': HOST + '/'
    },
    timeout: 5000,
    class_parse: $js.toString(() => {
        let classes = [
            { type_id: '推荐榜', type_name: '推荐榜' },
            { type_id: '新剧', type_name: '新剧' },
            { type_id: '逆袭', type_name: '逆袭' },
            { type_id: '霸总', type_name: '霸总' },
            { type_id: '现代言情', type_name: '现代言情' },
            { type_id: '打脸虐渣', type_name: '打脸虐渣' },
            { type_id: '豪门恩怨', type_name: '豪门恩怨' },
            { type_id: '神豪', type_name: '神豪' },
            { type_id: '马甲', type_name: '马甲' },
            { type_id: '都市日常', type_name: '都市日常' },
            { type_id: '战神归来', type_name: '战神归来' },
            { type_id: '小人物', type_name: '小人物' },
            { type_id: '女性成长', type_name: '女性成长' },
            { type_id: '大女主', type_name: '大女主' },
            { type_id: '穿越', type_name: '穿越' },
            { type_id: '都市修仙', type_name: '都市修仙' },
            { type_id: '强者回归', type_name: '强者回归' },
            { type_id: '亲情', type_name: '亲情' },
            { type_id: '古装', type_name: '古装' },
            { type_id: '重生', type_name: '重生' },
            { type_id: '闪婚', type_name: '闪婚' },
            { type_id: '赘婿逆袭', type_name: '赘婿逆袭' },
            { type_id: '虐恋', type_name: '虐恋' },
            { type_id: '追妻', type_name: '追妻' },
            { type_id: '天下无敌', type_name: '天下无敌' },
            { type_id: '家庭伦理', type_name: '家庭伦理' },
            { type_id: '萌宝', type_name: '萌宝' },
            { type_id: '古风权谋', type_name: '古风权谋' },
            { type_id: '职场', type_name: '职场' },
            { type_id: '奇幻脑洞', type_name: '奇幻脑洞' },
            { type_id: '异能', type_name: '异能' },
            { type_id: '无敌神医', type_name: '无敌神医' },
            { type_id: '古风言情', type_name: '古风言情' },
            { type_id: '传承觉醒', type_name: '传承觉醒' },
            { type_id: '现言甜宠', type_name: '现言甜宠' },
            { type_id: '奇幻爱情', type_name: '奇幻爱情' },
            { type_id: '乡村', type_name: '乡村' },
            { type_id: '历史古代', type_name: '历史古代' },
            { type_id: '王妃', type_name: '王妃' },
            { type_id: '高手下山', type_name: '高手下山' },
            { type_id: '娱乐圈', type_name: '娱乐圈' },
            { type_id: '强强联合', type_name: '强强联合' },
            { type_id: '破镜重圆', type_name: '破镜重圆' },
            { type_id: '暗恋成真', type_name: '暗恋成真' },
            { type_id: '民国', type_name: '民国' },
            { type_id: '欢喜冤家', type_name: '欢喜冤家' },
            { type_id: '系统', type_name: '系统' },
            { type_id: '真假千金', type_name: '真假千金' },
            { type_id: '龙王', type_name: '龙王' },
            { type_id: '校园', type_name: '校园' },
            { type_id: '穿书', type_name: '穿书' },
            { type_id: '女帝', type_name: '女帝' },
            { type_id: '团宠', type_name: '团宠' },
            { type_id: '年代爱情', type_name: '年代爱情' },
            { type_id: '玄幻仙侠', type_name: '玄幻仙侠' },
            { type_id: '青梅竹马', type_name: '青梅竹马' },
            { type_id: '悬疑推理', type_name: '悬疑推理' },
            { type_id: '皇后', type_name: '皇后' },
            { type_id: '替身', type_name: '替身' },
            { type_id: '大叔', type_name: '大叔' },
            { type_id: '喜剧', type_name: '喜剧' },
            { type_id: '剧情', type_name: '剧情' }
        ];
        input = classes;
    }),
    play_parse: true,    
    double: true,
    推荐: $js.toString(() => {
        let html = request(input);
        let data = JSON.parse(html);
        if (data && data.data) {
            VODS = data.data.map(item => ({
                vod_id: `${item.book_id}@${item.author}`,
                vod_name: item.title,
                vod_pic: item.cover,
                vod_remarks: item.type
            }));
        } else {
            VODS = [];
        }
    }),
    一级: $js.toString(() => {
        let html = request(input);
        let data = JSON.parse(html);
        if (data && data.data) {
            VODS = data.data.map(item => ({
                vod_id: `${item.book_id}@${item.author}`,
                vod_name: item.title,
                vod_pic: item.cover,
                vod_remarks: item.type
            }));
        } else {
            VODS = [];
        }
    }),    
    二级: $js.toString(() => {
        let [kid, kactor] = input.split('@');
        let html = request(kid);
        let kdetail = JSON.parse(html);
        let detail = kdetail.data.detail || {};
        let video_list = kdetail.data.video_list || [];        
        let kurls = video_list.map((it) => {
            return `${it.title}$${it.video_id}`
        }).join('#');
        
        VOD = {
            vod_id: kid,
            vod_name: detail.title || '',
            vod_pic: detail.cover || '',
            type_name: detail.category_schema || '',
            vod_remarks: `共${detail.total || 0}集 · ${detail.duration || ''}`,
            vod_director: detail.record_number || '',
            vod_actor: kactor, 
            vod_content: detail.desc || '',
            vod_play_from: '星之阁专线',
            vod_play_url: kurls
        }
    }),
    搜索: $js.toString(() => {
        let html = request(input);
        let data = JSON.parse(html);
        if (data && data.data) {
            VODS = data.data.map(item => ({
                vod_id: `${item.book_id}@${item.author}`, 
                vod_name: item.title,
                vod_pic: item.cover,
                vod_remarks: item.type
            }));
        } else {
            VODS = [];
        }
    }),    
    /*lazy: $js.toString(() => {
        let video_id = input;
        let qualities = ['1080p', '720p', '480p', '360p'];
        let video_url = '';        
        for (let i = 0; i < qualities.length; i++) {
            let quality = qualities[i];
            let api_url = HOST + '/API/playlet/?video_id=' + video_id + '&quality=' + quality;
            try {
                let html = request(api_url, {
                    headers: {
                        'User-Agent': 'okhttp/3.12.11',
                        'Content-Type': 'application/json; charset=utf-8'
                    }
                });
                let data = JSON.parse(html);
                if (data && data.data && data.data.video && data.data.video.url) {
                    video_url = data.data.video.url;
                    break;
                }
            } catch (e) {
                continue;
            }
        }        
        if (video_url) {
            input = video_url;
        } else {
            input = input;
        }
    })*/
    lazy: $js.toString(() => {
        const video_id = input;
        const QUALITY_MAP = {'1080p': '蓝光','720p': '超清','480p': '高清','360p': '标清'};
        function fetchJson(url) {
            try {
                let headers = {
                    'User-Agent': 'okhttp/3.12.11',
                    'Content-Type': 'application/json; charset=utf-8'
                };
                let html = request(url, { headers: headers });
                return JSON.parse(html);
            } catch (e) {
                return null;
            }
        }
        let urls = [];
        for (let level in QUALITY_MAP) {
            let display = QUALITY_MAP[level];
            let apiUrl = HOST + '/API/playlet/?video_id=' + video_id + '&quality=' + level;
            let data = fetchJson(apiUrl);
            if (data && data.data && data.data.video && data.data.video.url) {
                let videoUrl = data.data.video.url;
                urls.push(`星之阁-${display}`, videoUrl);
            }
        }
        if (urls.length > 0) {
            input = { parse: 0, url: urls };
        } else {
            input = '';
        }
    })
}