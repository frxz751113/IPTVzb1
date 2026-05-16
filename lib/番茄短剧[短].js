//搜索结果为书籍
var rule = {
    title: '番茄短剧',
    host: 'http://fqgo.52dns.cc',
    url: '/catalog?book_id=fyclass',
    searchUrl: '/search?query=**&tab_type=12&offset=fypage',
    detailUrl:'/catalog?book_id=fyid',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
        'X-SS-REQ-TICKET': Date.now().toString()
    },
    timeout: 5000,
    class_name: '热剧&新剧&逆袭&总裁&现言&打脸&马甲&豪门&都市&神豪',
    class_url: 'videoseries_hot&firstonlinetime_new&cate_739&cate_29&cate_3&cate_1051&cate_266&cate_1053&cate_261&cate_20',
    play_parse: true,
    double: true,
    lazy: $js.toString(() => {
        let id = MY_URL;
        let api_url = rule.host + '/video?item_ids=' + id;
        let html = request(api_url, { headers: rule.headers });
        let data = JSON.parse(html);        
        let videoModel = JSON.parse(data.data[id].video_model);
        let videoUrl = atob(videoModel.video_list.video_1.main_url);        
        input = {
            parse: 0,
            url: videoUrl,
            js: ''
        };
    }),    
    推荐: $js.toString(() => {
        let url = 'https://reading.snssdk.com/reading/bookapi/bookmall/cell/change/v?change_type=0&selected_items=videoseries_hot&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a';
        let html = request(url, {headers: rule.headers});
        let data = JSON.parse(html);        
        let items = [];
        if (data.data?.cell_view?.cell_data) {
            items = data.data.cell_view.cell_data;
        } else if (data.search_tabs) {
            for (const tab of data.search_tabs) {
                if (tab.title === '短剧' && tab.data) {
                    items = tab.data;
                    break;
                }
            }
        } else if (Array.isArray(data.data)) {
            items = data.data;
        } else {
            items = [data];
        }        
        VODS = items.map(item => {
            return {
                vod_id: item.series_id || item.book_id || item.id || (item.video_data?.[0]?.series_id) || '',
                vod_name: item.title || (item.video_data?.[0]?.title) || (item.data?.[0]?.title) || '未知短剧',
                vod_pic: item.cover || (item.video_data?.[0]?.cover) || (item.data?.[0]?.cover) || '',
                vod_remarks: (item.video_data?.[0]?.sub_title) || (item.video_data?.[0]?.rec_text) || (item.data?.[0]?.score) || '',
                vod_content: item.video_desc || (item.video_data?.[0]?.video_desc) || (item.data?.[0]?.video_desc) || ''
            };
        });
    }),    
    一级: $js.toString(() => {
        let classList = rule.class_url.split('&');
        let cateId = classList[MY_CATE.class_index] || classList[0];        
        let now = new Date();
        let sessionId = now.getUTCFullYear().toString() +
                        String(now.getUTCMonth() + 1).padStart(2, '0') +
                        String(now.getUTCDate()).padStart(2, '0') +
                        String(now.getUTCHours()).padStart(2, '0') +
                        String(now.getUTCMinutes()).padStart(2, '0');        
        let baseUrl = `https://reading.snssdk.com/reading/bookapi/bookmall/cell/change/v?change_type=0&selected_items=${cateId}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${sessionId}`;        
        let page = MY_PAGE || 1;
        if (page > 1) {
            let offset = (page - 1) * 12;
            baseUrl += `&offset=${offset}`;
        }       
        let html = request(baseUrl, {headers: rule.headers});
        let data = JSON.parse(html);        
        let items = [];        
        if (data.data?.cell_view?.cell_data) {
            items = data.data.cell_view.cell_data;
        } else if (data.search_tabs) {
            for (const tab of data.search_tabs) {
                if (tab.title === '短剧' && tab.data) {
                    items = tab.data;
                    break;
                }
            }
        } else if (Array.isArray(data.data)) {
            items = data.data;
        } else {
            items = [data];
        }        
        VODS = items.map(item => {
            let videoData = item.video_data?.[0] || {};
            return {
                vod_id: item.series_id || item.book_id || item.id || videoData.series_id || '',
                vod_name: item.title || videoData.title || '未知短剧',
                vod_pic: item.cover || videoData.cover || '',
                vod_remarks: videoData.sub_title || videoData.rec_text || ''
            };
        });
    }),    
    二级: $js.toString(() => {
        let html = request(input);
        let data = JSON.parse(html).data;
        let bookInfo = data.book_info;        
        let playList = data.item_data_list.map(item => {
            return `${item.title}$${item.item_id}`;
        }).join('#');        
        VOD = {
            vod_id: bookInfo.book_id,
            vod_name: bookInfo.book_name,
            vod_type: bookInfo.tags,
            vod_year: bookInfo.create_time,
            vod_pic: bookInfo.thumb_url || bookInfo.audio_thumb_uri,
            vod_content: bookInfo.abstract || bookInfo.book_abstract_v2,
            vod_remarks: bookInfo.sub_info || `更新至${data.item_data_list.length}集`,
            vod_play_from: '番茄短剧',
            vod_play_url: playList
        };
    }),    
    搜索: $js.toString(() => {
    let KEY = input;
    let page = MY_PAGE;
    let offset = (page - 1) * 12;
    let searchUrl = rule.host + '/search?query=' + KEY + '&tab_type=12&offset=' + offset;    
    let html = request(searchUrl, {headers: rule.headers});
    let data = JSON.parse(html);    
    let items = [];
    if (data.search_tabs && data.search_tabs.length > 0) {
        for (const tab of data.search_tabs) {
            if (tab.title === '短剧' && tab.data) {
                items = tab.data;
                break;
            }
            if (tab.tab_type === 1 && tab.data) {
                items = tab.data;
            }
        }
    }
    VODS = items.map(item => {
        let bookData = item.book_data && item.book_data.length > 0 
            ? item.book_data[0] 
            : {};        
        let title = bookData.book_name || '';
        if (item.search_high_light?.title?.rich_text) {
            title = item.search_high_light.title.rich_text
                .replace(/<em>/g, '')
                .replace(/<\/em>/g, '');
        }        
        return {
            vod_id: bookData.book_id || item.book_id || '',
            vod_name: title || '未知短剧',
            vod_pic: bookData.thumb_url || '',
            vod_remarks: bookData.sub_info || bookData.read_cnt_text || ''
        };
    });
    }),  
}