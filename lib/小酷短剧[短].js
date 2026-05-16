var rule = {
    title: '小酷短剧[短]',
    host: 'http://wapi.kuwo.cn',
    url: '/openapi/v1/shortplay/moduleMore?currentPage=fypage&moduleId=fyclass&rn=12',    
    detailUrl: '',
    searchUrl: '',
    searchable: 2,
    quickSearch: 1,
    filterable: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
        'Referer': 'http://www.kuwo.cn/',
        'Origin': 'http://www.kuwo.cn'
    },
    timeout: 15000,
    class_name: '土味爱情&更多精彩&霸道总裁的人生&赘婿当道&漫漫追妻路&家庭情感&逆袭重生&动画&日常&其他',
    class_url: '11&12&13&14&15&16&17&19&20&24',
    play_parse: true,
    double: true,    
    推荐: $js.toString(() => {
        let url = rule.host + '/openapi/v1/shortplay/moduleMore?currentPage=1&moduleId=10&rn=12';
        let res = request(url, {headers: rule.headers});
        let json = JSON.parse(res);
        if (json.data && json.data.list) {
            VODS = json.data.list.map(item => ({
                vod_id: item.url + '||' + encodeURIComponent(item.subTitle || ''),
                vod_name: item.title,
                vod_pic: item.img,
                vod_remarks: item.currrentDesc || ''
            }));
        } else {
            VODS = [];
        }
    }),    
    一级: $js.toString(() => {        
        let res = request(url, {headers: rule.headers});
        let json = JSON.parse(res);        
        if (json.data && json.data.list) {
            VODS = json.data.list.map(item => ({
                vod_id: item.url + '||' + encodeURIComponent(item.subTitle || ''),
                vod_name: item.title,
                vod_pic: item.img,
                vod_remarks: item.currrentDesc || ''
            }));
        } else {
            VODS = [];
        }
    }),    
    二级: $js.toString(() => {
        let parts = vod_id.split('||');
        let albumId = parts[0];
        let subTitle = parts[1] ? decodeURIComponent(parts[1]) : '';

        let res = request(rule.host + '/openapi/v1/shortplay/videoList?albumId=' + albumId, {headers: rule.headers});
        let json = JSON.parse(res);        
        if (json.data && json.data.list) {
            let sortedList = json.data.list.sort((a, b) => a.location - b.location);            
            let playList = [];
            sortedList.forEach((item, index) => {
                let episodeName = "第" + (index + 1) + "集";
                let playUrl = "http://nmobi.kuwo.cn/mobi.s?f=web&type=get_url_by_vid&vid=" + item.mvpayinfo.vid;
                
                playList.push({
                    name: episodeName,
                    url: playUrl
                });
            });            
            let playFrom = ['小酷短剧'];
            let playUrl = [playList.map(item => item.name + '$' + item.url).join('#')];            
            VOD = {
                vod_id: json.data.shortinfo.id,          // 保持为纯ID（与 albumId 相同）
                vod_name: json.data.shortinfo.title,
                vod_pic: json.data.shortinfo.cover,
                vod_content: subTitle || json.data.shortinfo.title,  // 优先使用传入的简介
                vod_remarks: `共${json.data.shortinfo.total}集`,
                vod_play_from: playFrom.join('$$$'),
                vod_play_url: playUrl.join('$$$')
            };
        }
    }),      
    lazy: `js:
        let inputUrl = input;
        
        if (inputUrl.includes('nmobi.kuwo.cn/mobi.s') && inputUrl.includes('get_url_by_vid')) {
            let res = request(inputUrl, {headers: rule.headers});
            
            if (res) {
                let urlMatch = res.match(/url=(\\S+)/);
                if (urlMatch && urlMatch[1]) {
                    let videoUrl = urlMatch[1].trim();
                    
                    if (videoUrl.includes('\\n') || videoUrl.includes('\\r')) {
                        videoUrl = videoUrl.split(/\\s/)[0];
                    }
                    
                    input = videoUrl;
                } else {
                    let lines = res.split('\\n');
                    for (let line of lines) {
                        if (line.startsWith('url=')) {
                            let videoUrl = line.substring(4).trim();
                            input = videoUrl;
                            break;
                        }
                    }
                }
            }
        }
        
        input;
    `
}