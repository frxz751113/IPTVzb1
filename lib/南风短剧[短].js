var rule = {
    author: '嗷呜',
    title: '南风短剧',
    host: 'https://www.nanf.cc',
    url: '/djshow/fyclassfyfilter',
    filter_url: '--{{fl.排序}}------fypage---.html',
    searchable: 2,
    quickSearch: 1,
    filterable: 0,
    class_parse: '.item&&li;a&&Text;a&&href;.*/(.*?).html',
    play_parse: true,
    filter: 'H4sIAAAAAAAAA6vmUgACJUMlK4VoMBMEquEssGR2aiVQWulZ36Snu/qVdFAl8xJzU3HLliXmlKaimI3dDoRxYLOmb3s5fQtWExEmgxSWZAItx5CvxdSCz7Ynu3Y92zCFCNsyMkuKKbbtxfqWpx1tRNhWnJxfhM1zKCKxXKjisRATlYxG43NYxafxaHwOq/g0GY3PYRWfpqPxOazi02w0PodVfJqPxuewik+L0fgcHvHJVQsAg4rcm4IOAAA=',
    cate_exclude: '最新短剧|热播榜',
    lazy: $js.toString(() => {
        input = "push://" + input;
    }),
    limit: 6,
    推荐: '*',
    double: true,
    一级: '.shoutu-vodlist .col8;img&&alt;.lazyload&&data-original;;h4&&a&&href',
    二级: {
        title: 'h1&&Text;.tag-link&&Text',
        img: '.lazyload&&data-original',
        desc: '.tag a:eq(0)&&Text;.tag a:eq(1)&&Text;.tag a:eq(2)&&Text;.tag a:eq(3)&&Text',
        content: '.panel-bd:eq(-2)&&Text',
        tabs: $js.toString(() => {
            TABS = ['夸克网盘']
        }),
        lists: $js.toString(() => {
            LISTS = []
            let kk = []
            let kku = jsp.pdfh(html, '.wp_play .btn-main1&&href')
            kk.push("跳转夸克$" + kku)
            LISTS.push(kk)
        }),
    },
    searchUrl: '/djsearch/**----------fypage---.html',
    搜索: '*',
}