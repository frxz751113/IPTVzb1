var rule = {
    title: '爱电影',
    host: 'https://kuhh4jo.com/',
    url: '/api/mw-movie/anonymous/video/list?pageNum=fypage&pageSize=30&sort=1&sortBy=1&type1=fyclass',
    searchUrl: '/api/mw-movie/anonymous/video/searchByWordPageable?keyword=**&pageNum=fypage&pageSize=12&type=false',
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'Referer': 'https://kuhh4jo.com/',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    },
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    class_name: '电影&电视剧&综艺&动漫',
    class_url: '1&2&3&4',
    limit: 6,
    double: false,
    play_parse: true,
    lazy: $js.toString(() => {
        var t = new Date().getTime().toString();
        // 解析URL获取参数
        var urlObj = new URL(input);
        var params = new URLSearchParams(urlObj.search);
        var signkey = `clientType=1&id=${params.get('id')}&nid=${params.get('nid')}&key=cb808529bae6b6be45ecfab29a4889bc&t=${t}`;
        
        eval(getCryptoJS());
        var key = CryptoJS.SHA1(CryptoJS.MD5(signkey).toString()).toString();
        
        let json_data = JSON.parse(request(input, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'deviceId': '7211cb82-f86a-4efa-8912-beeea7321600',
                'sign': key,
                't': t,
                'client-type': '1',
                'authorization': '',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Accept': 'application/json, text/plain, */*',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://kuhh4jo.com/vod/play/' + params.get('id') + '/sid/' + params.get('nid'),
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
        }));
        
        let link = json_data.data.list[0].url;
        input = {
            url: link,
            header: rule.headers
        };
    }),
    推荐: $js.toString(() => {
        let kdata = fetch(input).split('data\\\":')[3].split(',\\\"newestShort')[0] + '}';
        kdata = kdata.replace(/\\/g, '');
        let kjson = JSON.parse(kdata);
        VODS = [];
        Object.keys(kjson).forEach((key) => {
            kjson[key].list.map((it) => {
                VODS.push({
                    vod_name: it.vodName,
                    vod_pic: it.vodPic,
                    vod_remarks: it.vodRemarks + '_' + it.vodDoubanScore,
                    vod_id: it.vodId
                })
            })
        })
    }),
    一级: $js.toString(() => {
        let d = [];
        const t = new Date().getTime();
        eval(getCryptoJS());
        const signkey = 'pageNum=' + MY_PAGE + '&pageSize=30&sort=1&sortBy=1&type1=' + MY_CATE + '&key=cb808529bae6b6be45ecfab29a4889bc&t=' + t;
        const key = CryptoJS.SHA1(CryptoJS.MD5(signkey).toString()).toString();
        const list = JSON.parse(request(input, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'deviceId': '7211cb82-f86a-4efa-8912-beeea7321600',
                'sign': key,
                't': t,
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': rule.host
            }
        })).data.list;
        list.forEach((it) => {
            d.push({
                title: it.vodName,
                desc: it.vodRemarks || it.vodVersion,
                img: it.vodPic,
                url: rule.host.replace(/\/$/, '') + '/detail/' + it.vodId
            });
        });
        setResult(d);
    }),
    二级: $js.toString(() => {
        let parts = input.split('/');
        let id = parts[parts.length - 1];
        const t = new Date().getTime();
        eval(getCryptoJS());
        const signkey = 'id=' + id + '&key=cb808529bae6b6be45ecfab29a4889bc&t=' + t;
        const key = CryptoJS.SHA1(CryptoJS.MD5(signkey).toString()).toString();
        const apiUrl = rule.host.replace(/\/$/, '') + '/api/mw-movie/anonymous/video/detail?id=' + id;
        let html = JSON.parse(request(apiUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'deviceId': '7211cb82-f86a-4efa-8912-beeea7321600',
                'sign': key,
                't': t,
                'Accept': 'application/json, text/plain, */*',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': rule.host + 'detail/' + id
            }
        })).data;
        // 完善VOD信息
        VOD = {
            vod_id: input,
            vod_name: html.vodName,
            vod_pic: html.vodPic,
            vod_content: html.vodBlurb || html.vodContent,
            vod_director: html.vodDirector || '',
            vod_actor: html.vodActor || '',
            vod_area: html.vodArea || '',
            vod_lang: html.vodLang || '',
            vod_year: html.vodYear || '',
            vod_type: html.vodClass || html.typeName || '',
            vod_remarks: html.vodRemarks || (html.vodSerial ? `更新至${html.vodSerial}集` : '') + (html.vodTotal ? `|共${html.vodTotal}集` : ''),
            vod_score: html.vodDoubanScore || html.vodScore || '',
            vod_play_from: '爱电影'
        };
        // 生成播放链接
        let playUrls = [];
        if(html.episodeList && html.episodeList.length > 0) {
            html.episodeList.forEach((it) => {
                const playLink = rule.host.replace(/\/$/, '') + '/api/mw-movie/anonymous/v2/video/episode/url?clientType=1&id=' + id + '&nid=' + it.nid;
                playUrls.push(it.name + '$' + playLink);
            });
            VOD.vod_play_url = playUrls.join('#');
        }
    }),
    搜索: $js.toString(() => {
        const t = new Date().getTime();
        eval(getCryptoJS());
        let pg = MY_PAGE;
        let signkey = 'keyword=' + KEY + '&pageNum=' + pg + '&pageSize=12&type=false&key=cb808529bae6b6be45ecfab29a4889bc&t=' + t;
        const key = CryptoJS.SHA1(CryptoJS.MD5(signkey).toString()).toString();
        let data = JSON.parse(request(input, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'deviceId': '7211cb82-f86a-4efa-8912-beeea7321600',
                'sign': key,
                't': t,
                'Accept': 'application/json, text/plain, */*',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': rule.host
            }
        })).data.list;
        let d = [];
        data.forEach(it => {
            d.push({
                title: it.vodName,
                desc: it.vodRemarks || it.vodVersion,
                img: it.vodPic,
                url: rule.host.replace(/\/$/, '') + '/detail/' + it.vodId
            });
        });
        setResult(d);
    }),
};
