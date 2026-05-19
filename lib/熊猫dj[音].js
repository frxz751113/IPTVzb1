var rule = {
    title: '熊猫dj[音]',
    homeUrl: 'https://m.djcscs.com/index.php?ac=music_index',
    host: 'https://m.djcscs.com',
    url: 'https://m.djcscs.com/index.php?ac=ajax_fyclassAjaxPage&classid=0&size=0&page=fypage',
    searchUrl: '',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    filter: '',
    filter_url: '',
    filter_def: {},
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 5000,

    lazy: `js:
            let kurl = request(input).match(/mp3: \\"(.*?)\\"/)[1];          
             
            input = { jx: 0, parse: 0, url: kurl };
            
            `,
    // class_parse:'.index-tab&&a;a&&Text;a&&href;ac=(.*?)_index',
    class_name: "曲库&电台&歌单&U盘音乐&视频&音乐人", //静态分类
    class_url: "music&radio&topic&upan&video&dj", //静态分类
    cate_exclude: '曲库|电台|视频', //需要排除的分类
    play_parse: true,
    double: true, //推荐页双层显示
    //推荐:列表1;列表2;标题;图片;描述;链接;详情
    推荐: ';;;;;;',
    //一级: '列表;标题;图片;描述;链接;详情',
    一级: 'a:has(img[src*=uploadfiles]);a&&Text;img&&src;;a&&href;',
    二级: {
        title: 'a&&Text;vod_type',
        img: 'src',
        desc: '主要信息;年代;地区;演员;导演',
        content: '简介',
        tabs: '', //线路数组
        lists: '.pad15:has(img[src*=uploadfiles])&&a:has(img[width=23])', //集数组
        tab_text: '', //线路名
        list_text: '', //集名
        list_url: 'a&&href' //集链接
    }, //'*',没有二级直接嗅探播放详情页地址
    //搜索: '列表;标题;图片;描述;链接;详情',
    搜索: ';;;;;',
}