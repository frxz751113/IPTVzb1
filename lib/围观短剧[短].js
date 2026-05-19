globalThis.h_ost = 'https://api.drama.9ddm.com';

var rule = {
    title: '围观短剧[短]',
    host: h_ost,
    url: '/drama/home/search',
    homeUrl: '/drama/home/shortVideoTags',
    detailUrl: '/drama/home/shortVideoDetail?oneId=fyid&page=1&pageSize=1000',
    searchUrl: '/drama/home/search',
    headers: {
        'User-Agent': 'okhttp/3.12.11',
        'Content-Type': 'application/json;charset=utf-8'
    },
    timeout: 5000,
    filterable: 1,
    limit: 20,
    multi: 1,
    searchable: 1,
    play_parse: true,
    search_match: true, 
    
    // 分类数据
    class_parse: $js.toString(() => {
        let html = request(input);
        let data = JSON.parse(html);
        let classes = [];
        let filterObj = {};
        
        data.audiences.forEach((audience) => {
            classes.push({
                type_name: audience,
                type_id: audience,
            });
            
            let filters = [
                {
                    key: "tag",
                    name: "标签",
                    value: [
                        { n: "全部", v: "" }
                    ]
                }
            ];
            
            data.tags.forEach((tag) => {
                filters[0].value.push({
                    n: tag,
                    v: tag
                });
            });
            
            filterObj[audience] = filters;
        });
        
        input = classes;
        homeObj.filter = filterObj;
    }),

    lazy: $js.toString(() => {
        let playSetting = JSON.parse(input);
        let videoUrl = playSetting.high || playSetting.normal || playSetting.super;
        input = {
            parse: 0,
            url: videoUrl
        };
    }),
    
    一级: $js.toString(() => {
        let d = [];
        let tag = MY_FL.tag || '';
        const postData = JSON.stringify({
            "audience": MY_CATE,
            "page": MY_PAGE,
            "pageSize": 30,
            "searchWord": "",
            "subject": tag
        });

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'User-Agent': 'okhttp/3.12.11'
            },
            body: postData
        };
        
        let html = request(input, options);
        let response = JSON.parse(html);
        let data = response.data;
        
        data.forEach((it) => {
            d.push({
                title: it.title,
                img: it.vertPoster,
                year: it.publishDate ? it.publishDate.toString() : '',
                desc: `集数:${it.episodeCount} 播放:${it.viewCount}`,
                remarks: it.description,
                url: it.oneId
            });
        });
        setResult(d);
    }),
    
    二级: $js.toString(() => {
        let response = JSON.parse(request(input));
        let data = response.data;
        let firstEpisode = data[0];
        
        VOD = {
            vod_name: firstEpisode.title,
            vod_pic: firstEpisode.vertPoster,
            vod_remarks: `共${data.length}集`,
            vod_content: `播放量:${firstEpisode.collectionCount} 评论:${firstEpisode.commentCount}`
        };
        
        let playUrls = data.map(episode => {
            let playSetting = JSON.parse(episode.playSetting);
            let videoUrl = playSetting.high || playSetting.normal || playSetting.super;
            return `${episode.title}第${episode.playOrder}集$${JSON.stringify(playSetting)}`;
        });
        
        VOD.vod_play_from = '围观短剧';
        VOD.vod_play_url = playUrls.join("#");
    }),
    搜索: $js.toString(() => {
        let d = [];
        const postData = JSON.stringify({
            "audience": "",
            "page": 1,
            "pageSize": 9999,
            "searchWord": KEY,
            "subject": ""
        });

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'User-Agent': 'okhttp/3.12.11'
            },
            body: postData
        };
        
        let html = request(input, options);
        let response = JSON.parse(html);
        let data = response.data;
        data.forEach((it) => {
        /*
            if (rule.search_match && !it.title.includes(KEY)) {
                return; 
            }*/
            d.push({
                title: it.title,
                img: it.vertPoster,
                year: it.publishDate ? it.publishDate.toString() : '',
                desc: `集数:${it.episodeCount} 播放:${it.viewCount}`,
                remarks: it.description,
                url: it.oneId
            });
        });
        setResult(d);
    }),
}
