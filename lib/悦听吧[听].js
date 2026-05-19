var rule = {
    title: '悦听吧有声小说',
    编码: 'utf-8',
    host: 'http://www.yuetingba.cn',
    url: '/book/2/1', // 历史分类页面的 URL
    searchUrl: '/Search?name=**',
    searchable: 2,
    quickSearch: 0,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
    },
    timeout: 10000,
    class_name: '玄幻&历史&武侠&都市&科幻&名著&女频&社科&儿童',
    class_url: '1&2&3&4&5&6&7&8&9',
    play_parse: true,
    lazy: '',
    limit: 10,
    推荐: '.box-right-item .box-right-title&&Text;.box-right-item a&&href',
    一级: '.book-list-item;div.book-title&&Text;div.book-image img&&src;div.book-intro&&Text;a&&href',
    二级: {
        title: '.box-list-item-text-title&&Text',
        img: 'div.box-list-item-img img&&src',
        desc: '.box-list-item-text-intro&&Text',
        content: '.box-list-item-text-intro&&Text',
        tabs: '.playlist-top&&h2',
        lists: '#playlist ul li',
        playerTitle: '.bottom-play-control iframe&&Text',
        playerTime: '.bottom-play-control iframe .current-time&&Text',
        playerDuration: '.bottom-play-control iframe .duration&&Text',
        playerProgress: 'js:let progressBar=document.querySelector(".bottom-play-control iframe .progress-bar");progressBar.style.width',
    },
    搜索: '/Search?name=**'
}
