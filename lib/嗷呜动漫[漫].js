
var rule = {
    title: '嗷呜动漫',
    host: 'https://www.aowu.tv',
    url: '/index.php/ds_api/vod',
    searchUrl: '/search/**----------fypage---/',
    class_name: '当季新番&番剧&剧场',
    class_url: '20&21&22',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {'User-Agent': 'MOBILE_UA'},
    play_parse: true,
    lazy: '',
    limit: 6,
    推荐: '.flex;.public-list-box;a&&title;.lazy&&data-src;.ft2&&Text;a&&href',
    double: true,
    一级: $js.toString(()=>{
        let d = [];
        const data = {'type': MY_CATE, 'by': 'time', 'page': MY_PAGE};
        const options = {method: 'POST', body: data};
        let html = request(input, options);
        let list = JSON.parse(html).list;
        list.forEach(it => 
        d.push({
            title: it.vod_name,
            desc: it.vod_remarks,
            img: it.vod_pic,
            url: rule.host + it.url
        }));
        setResult(d);
    }),
    二级: {
        title: 'h3&&Text',
        img: '.vodlist_thumb&&data-original',
        content: '.switch-box&&Text',
        tabs: '.anthology-tab:eq(#id) a',
        lists: '.anthology-list-play:eq(#id) a'
    },
    搜索: '.row .vod-detail;h3&&Text;img&&data-src;.pic_text&&Text;a&&href'
}
