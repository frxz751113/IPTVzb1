var rule = {
    类型: '影视',
    title: '甜圈短剧[短]',
    host: 'https://mov.cenguigui.cn',
    //homeUrl: '/duanju/api.php?classname=推荐榜&offset=0',
    //url: '/duanju/api.php?classname=fyclass&offset=fypage',
    homeUrl: '/duanju/api.php?name=推荐榜&offset=0',
    url: '/duanju/api.php?name=fyclass&offset=fypage',
    detailUrl: '/duanju/api.php?book_id=fyid',
    searchUrl: '/duanju/api.php?name=**&page=fypage',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    //search_match: true, //精准搜索
    headers: {
        'User-Agent': 'MOBILE_UA',
        'Referer': HOST + '/'
    },
    timeout: 5000,
    class_name: '🔥 推荐榜&🎬 新剧&🎬 逆袭&🎬 霸总&🎬 现代言情&🎬 打脸虐渣&🎬 豪门恩怨&🎬 神豪&🎬 马甲&🎬 都市日常&🎬 战神归来&🎬 小人物&🎬 女性成长&🎬 大女主&🎬 穿越&🎬 都市修仙&🎬 强者回归&🎬 亲情&🎬 古装&🎬 重生&🎬 闪婚&🎬 赘婿逆袭&🎬 虐恋&🎬 追妻&🎬 天下无敌&🎬 家庭伦理&🎬 萌宝&🎬 古风权谋&🎬 职场&🎬 奇幻脑洞&🎬 异能&🎬 无敌神医&🎬 古风言情&🎬 传承觉醒&🎬 现言甜宠&🎬 奇幻爱情&🎬 乡村&🎬 历史古代&🎬 王妃&🎬 高手下山&🎬 娱乐圈&🎬 强强联合&🎬 破镜重圆&🎬 暗恋成真&🎬 民国&🎬 欢喜冤家&🎬 系统&🎬 真假千金&🎬 龙王&🎬 校园&🎬 穿书&🎬 女帝&🎬 团宠&🎬 年代爱情&🎬 玄幻仙侠&🎬 青梅竹马&🎬 悬疑推理&🎬 皇后&🎬 替身&🎬 大叔&🎬 喜剧&🎬 剧情',
    class_url: '推荐榜&新剧&逆袭&霸总&现代言情&打脸虐渣&豪门恩怨&神豪&马甲&都市日常&战神归来&小人物&女性成长&大女主&穿越&都市修仙&强者回归&亲情&古装&重生&闪婚&赘婿逆袭&虐恋&追妻&天下无敌&家庭伦理&萌宝&古风权谋&职场&奇幻脑洞&异能&无敌神医&古风言情&传承觉醒&现言甜宠&奇幻爱情&乡村&历史古代&王妃&高手下山&娱乐圈&强强联合&破镜重圆&暗恋成真&民国&欢喜冤家&系统&真假千金&龙王&校园&穿书&女帝&团宠&年代爱情&玄幻仙侠&青梅竹马&悬疑推理&皇后&替身&大叔&喜剧&剧情',
    play_parse: true,
    double: true,
    /*lazy: $js.toString(() => {
        const qualities = [
            {display: "蓝光",level: "1080p"},
            {display: "超清",level: "720p"},
            {display: "高清",level: "480p"},
            {display: "标清",level: "360p"},
            {display: "默认",level: null}    // null表示不使用level参数
        ];
        let urls = [];
        qualities.forEach(quality => {
            let baseUrl = `${HOST}/duanju/api.php?video_id=${input}&type=mp4`;
            let url = quality.level ? `${baseUrl}&level=${quality.level}` : baseUrl;
            urls.push(quality.display, url);
        });        
        input = {
            parse: 0,
            url: urls
        };
    }),*/
    lazy: $js.toString(() => {
        const video_id = input;
        const QUALITY_MAP = {'1080p': '蓝光','720p': '超清','480p': '高清','360p': '标清'};
        function fetchJson(url, headers) {
            try {
                const response = request(url, {
                    headers
                });
                return JSON.parse(response);
            } catch (error) {
                return null;
            }
        }
        const starSource = {
            name: '星之阁',
            qualities: Object.keys(QUALITY_MAP).map(level => ({
                display: QUALITY_MAP[level],
                level: level
            })),
            getUrl: function(video_id, quality) {
                const apiUrl = `https://api.xingzhige.com/API/playlet/?video_id=${video_id}&quality=${quality.level}`;
                const headers = {
                    'User-Agent': 'okhttp/3.12.11',
                    'Content-Type': 'application/json; charset=utf-8'
                };
                const data = fetchJson(apiUrl, headers);
                return data && data.data && data.data.video && data.data.video.url;
            }
        };
        const donutQualities = Object.keys(QUALITY_MAP).map(level => ({
            display: QUALITY_MAP[level],
            level: level
        }));
        const donutSource = {
            name: '甜圈',
            qualities: donutQualities,
            getUrl: function(video_id, quality) {
                const baseUrl = `${HOST}/duanju/api.php?video_id=${video_id}&type=mp4`;
                return `${baseUrl}&level=${quality.level}`;
            }
        };
        const sources = [starSource, donutSource];
        const urls = [];
        const seenUrls = new Set(); 
        for (const source of sources) {
            for (const quality of source.qualities) {
                const videoUrl = source.getUrl(video_id, quality);
                if (videoUrl && !seenUrls.has(videoUrl)) {
                    seenUrls.add(videoUrl);
                    urls.push(`${source.name}-${quality.display}`, videoUrl);
                }
            }
        }        
        input = { parse: 0, url: urls };
    }),
    推荐: $js.toString(() => {
        let res = request(input, {
            headers: rule.headers
        });
        let data = JSON.parse(res).data;
        VODS = [];
        data.forEach(item => {
            VODS.push({
                vod_id: item.book_id,
                vod_name: item.title,
                vod_pic: item.cover,
                vod_remarks: `${item.type}|${item.episode_cnt}集`
            });
        });
    }),
    一级: $js.toString(() => {
        let res = request(input, {
            headers: rule.headers
        });
        let data = JSON.parse(res).data;
        VODS = [];
        data.forEach(item => {
            VODS.push({
                vod_id: item.book_id,
                vod_name: item.title,
                vod_pic: item.cover,
                //vod_remarks: `${item.score}分|${item.episode_cnt}集`
                vod_remarks: (item.score !== undefined && item.score !== null ? item.score + '分' : item.type) + '|' + item.episode_cnt + '集'
            });
        });
    }),
    二级: $js.toString(() => {
        let res = request(input, {
            headers: rule.headers
        });
        let item = JSON.parse(res);
        let playUrls = [];
        if (item.data && Array.isArray(item.data)) {
            playUrls = item.data.map(ep => `${ep.title}$${ep.video_id}`);
        }
        VOD = {
            vod_id: item.book_id || '',
            vod_name: item.book_name || item.title || '',
            //type_name: item.category || '',
            vod_pic: item.book_pic || item.cover || '',
            vod_content: item.desc || '',
            vod_remarks: `${item.duration}•共${item.total}集  类型：${item.category}`,
            vod_director: item.author,
            vod_year: item.time || '',
            vod_play_from: '甜圈短剧',
            vod_play_url: playUrls.join("#")
        };
    }),
    搜索: $js.toString(() => {
        let d = [];
        let html = request(input, {
            headers: rule.headers
        });
        let data = JSON.parse(html).data;
        if (rule.search_match) {
            data = data.filter(item =>
                item.title &&
                new RegExp(KEY, "i").test(item.title)
            );
        }
        data.forEach((it) => {
            d.push({
                title: it.title,
                img: it.cover,
                year: it.author,
                desc: it.type,
                url: it.book_id
            });
        });
        setResult(d);
    }),
}