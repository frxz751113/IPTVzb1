var rule = {
    title: '91看电视测试',
    author: '亮亮先森UX&蓝莓果酱UX',
    version: '20251019',
    host: 'http://sj.91kds.cn',
    url: 'http://sj.91kds.cn/api/get_channel.php?id=fyclass',
    searchUrl: 'http://sj.91kds.cn/api/get_search.php?id=**&deviceId=ffffffff-da12-5a9f-0000-00002bc63564&imei=483248965895528&key=.js:getVar(\'kdskey\')&tm=.js:getVar(\'kdstime\')&desc=广东省广州市移动&mac=&version=2.1.3&isHaveFile=no&userToken=&netType=wifi&app=91ktv&channel=umeng',
    homeUrl: 'http://sj.91kds.cn',
    detailUrl: '',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    class_name: '央视&卫视&高清&4K&影视&体育&动漫&财经&综艺&教育&新闻&纪录&国际&网络&购物&虎牙&安徽&北京&重庆&福建&甘肃&湖北&湖南&吉林&江苏&江西&辽宁&内蒙古&宁夏&青海&山东&山西&陕西&上海&贵州&海南&河北&河南&黑龙江&天津&新疆&西藏&云南&浙江&广西&广东&四川',
    class_url: '央视&卫视&高清&4K&影视&体育&动漫&财经&综艺&教育&新闻&纪录&国际&网络&购物&虎牙&安徽&北京&重庆&福建&甘肃&湖北&湖南&吉林&江苏&江西&辽宁&内蒙古&宁夏&青海&山东&山西&陕西&上海&贵州&海南&河北&河南&黑龙江&天津&新疆&西藏&云南&浙江&广西&广东&四川',
    headers: {
        'User-Agent': 'pc'
    },
    编码: 'utf-8',
    timeout: 5000,
    limit: 20,
    double: false,
    play_parse: true,
    filter: {},
    filter_url: '',
    一级: $js.toString(() => {
        var res = {};
        var items = [];
        eval(getCryptoJS());
        var nwtime = parseInt(new Date().getTime() / 1000) + '';
        var html = request(input);
        if (/ename/.test(html)) {
            var list = JSON.parse(html);
            for (var i = 0; i < list.length; i++) {
                var title = list[i].name;
                var enamee = list[i].ename;
                var srcKey = enamee + "com.jiaoxiang.fangnaleahkajfkahlajjaflfakhfakfbuyaozaigaolefuquqikangbuzhu2.3.4fu:ck:92:92:ff" + nwtime + "20240918";
                var sign = CryptoJS.MD5(srcKey).toString(CryptoJS.enc.Hex);
                var url = "http://sjapi1.91kds.cn/api/get_source.php?ename=" + enamee + "&app=com.jiaoxiang.fangnale" +
                    "&version=2.3.4" +
                    "&mac=fu:ck:92:92:ff" +
                    "&nwtime=" + nwtime +
                    "&sign=" + sign +
                    "&ev=20240918";
                items.push({
                    title: title,
                  //  url: url,
                    url: url + '@' + title,
                    img: list[i].icon,
                    desc: ""
                });
            }
        }
        setResult(items);
    }),
    二级: $js.toString(() => {
        let purl = input.split('@')[0];
        let html = request(purl);
        let data = JSON.parse(html);
        
        // 获取频道名称
        let vod_name = "未知频道";
        if (input.includes('@')) {
            vod_name = input.split('@')[1];
        } else {
            vod_name = data.name || data.title || "直播频道";
        }
        
        VOD = {
            vod_id: purl,
            vod_name: vod_name,
            vod_pic: data.icon || "",
            vod_remarks: "直播",
            vod_content: data.desc || "暂无简介"
        };
    
        let list = data.liveSource || [];
        let names = data.liveSourceName || [];
        let playFrom = [];
        let playUrl = [];
        eval(getCryptoJS());
        let seen = new Set();
        let lineCounter = 1;
    
        list.forEach((item, j) => {
            let rawInput = item;
            let inputUrl = rawInput.replace(/^kdsvod:\/\//, '');
            let urlName = names[j] || '线路' + lineCounter;
            
            if (inputUrl.includes('pwd=jsdecode') && inputUrl.includes('id=')) {
                let parts = inputUrl.split('?');
                let baseUrl = parts[0];
                let queryStr = parts[1] || '';
                let queryObj = {};
                queryStr.split('&').forEach(kv => {
                    let t = kv.split('=');
                    if (t[0]) queryObj[t[0]] = decodeURIComponent(t[1] || '');
                });
                let id = queryObj['id'];
                let bt = queryObj['bt'] || null;
                let coreKey = (bt || '') + '_' + id;
                
                // 去重检查
                if (seen.has(coreKey)) return;
                seen.add(coreKey);
                
                let params = {
                    app: 'com.jiaoxiang.fangnale',
                    version: '2.3.4',
                    mac: 'fu:ck:92:92:ff',
                    utk: '',
                    nwtime: Math.floor(Date.now() / 1000),
                    ev: '20250113'
                };
                let appendStr = 'ahkajfkahlajjaflfakhfakfbuyaozaigaolefuquqikangbuzhu';
                let signStr = id;
                Object.keys(params).forEach(key => {
                    if (key === 'tmk') return;
                    if (key === 'app') signStr += params[key] + appendStr;
                    else signStr += params[key];
                });
                
                params.sign = CryptoJS.MD5(signStr).toString(CryptoJS.enc.Hex);
                let finalQuery = [];
                if (bt !== null) finalQuery.push('bt=' + bt);
                finalQuery.push('id=' + id);
                Object.keys(params).forEach(k => {
                    finalQuery.push(k + '=' + encodeURIComponent(params[k]));
                });
                
                let finalUrl = baseUrl + '?' + finalQuery.join('&');
                let lineName = '线路' + lineCounter;
                playFrom.push(lineName);
                playUrl.push(urlName + '$' + finalUrl);
                lineCounter++;
                
            } else {
                let videoUrl;
                if (inputUrl.startsWith('htmlplay://')) {
                    videoUrl = inputUrl.replace('htmlplay://', '').split('#')[0];
                } else {
                    videoUrl = inputUrl;
                }
                
                // 普通URL的去重检查
                let urlKey = videoUrl.split('?')[0];
                if (seen.has(urlKey)) return;
                seen.add(urlKey);
                
                let referer = '';
                if (inputUrl.includes('@@referer=')) {
                    let tmp = inputUrl.split('@@referer=');
                    videoUrl = tmp[0];
                    referer = tmp[1] || '';
                }
                
                let lineName = '线路' + lineCounter;
                
                if (referer) {
                    let playObj = JSON.stringify({
                        url: videoUrl,
                        header: {
                            Referer: referer
                        }
                    });
                    playFrom.push(lineName);
                    playUrl.push(urlName + '$' + playObj);
                } else {
                    playFrom.push(lineName);
                    playUrl.push(urlName + '$' + videoUrl);
                }
                lineCounter++;
            }
        });
        
        VOD.vod_play_from = playFrom.join("$$$");
        VOD.vod_play_url = playUrl.join("$$$");
    }),
    lazy: $js.toString(() => {
        let url = input;
        
        // 如果是 JSON 格式的播放对象
        if (url.startsWith('{')) {
            try {
                let playObj = JSON.parse(url);
                if (playObj.url) {
                    input = {
                        parse: 0,
                        jx: 0,
                        url: playObj.url,
                        header: playObj.header || {}
                    };
                    return;
                }
            } catch (e) {
                // 如果不是有效的 JSON，继续处理
            }
        }
        
        // 处理普通 URL
        if (url.includes('pwd=jsdecode') && url.includes('id=')) {
            // 已经是处理过的 URL，直接使用
            input = {
                parse: 0,
                jx: 0,
                url: url
            };
        } else if (url.startsWith('http')) {
            // 普通 HTTP URL
            input = {
                parse: 0,
                jx: 0,
                url: url
            };
        } else if (url.startsWith('video://')) {
            // video协议
            input = {
                parse: 0,
                jx: 0,
                url: url.replace('video://', '')
            };
        } else {
            // 其他情况
            input = {
                parse: 0,
                jx: 0,
                url: url
            };
        }
    }),
    搜索: $js.toString(() => {
    }),
    cate_exclude: "",
    tab_exclude: "",
    类型: "直播",
    二级访问前: "",
    search_encoding: "",
    图片来源: "",
    图片替换: "",
    play_json: [],
    pagecount: {},
    proxy_rule: "",
    sniffer: false,
    isVideo: "",
    tab_remove: [],
    tab_order: [],
    tab_rename: {}
}
