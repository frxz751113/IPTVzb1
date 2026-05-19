var rule = {
    title: '天龙电影网',
    host: 'https://www.tlyy8.com',
    url: '/tlpb/fyfilter.html',
    searchUrl: '/tlso**/page/fypage.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {
        'User-Agent': 'UC_UA',
    },
    class_parse: '.stui-header__menu li:gt(0):lt(5);a&&Text;a&&href;.*/(.*?).html',
    play_parse: true,
    lazy: $js.toString(() => {
        let html = JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);
        let url = html.url;
        if (html.encrypt == '1') {
            url = unescape(url)
        } else if (html.encrypt == '2') {
            url = unescape(base64Decode(url))
        }
        if (/\.m3u8|\.mp4/.test(url)) {
            input = {
                jx: 0,
                url: url,
                parse: 0
            }
        } else {
            input
        }
    }),
    limit: 6,
    推荐: 'ul.stui-vodlist.clearfix;li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href',
    double: true,
    一级: '.stui-vodlist li;a&&title;a&&data-original;.pic-text&&Text;a&&href',
    二级: {
        title: '.stui-content__detail .title&&Text;.stui-content__detail p:eq(-2)&&Text',
        img: '.stui-content__thumb .lazyload&&data-original',
        desc: '.stui-content__detail p:eq(0)&&Text;.stui-content__detail p:eq(1)&&Text;.stui-content__detail p:eq(2)&&Text',
        content: '.detail&&Text',
        tabs: '.stui-pannel__head li',
        lists: '.stui-content__playlist:eq(#id) li',
    },
    搜索: 'ul.stui-vodlist__media:eq(0),ul.stui-vodlist:eq(0),#searchList li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
    搜索1: 'ul.stui-vodlist&&li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
    搜索2: 'ul.stui-vodlist__media&&li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
    filter: {
        "dianying": [{ key: '分类', name: '分类', value: [{ n: '全部', v: 'dianying', }, { n: '动作片', v: 'dzp', }, { n: '科幻片', v: 'khp', }, { n: '战争片', v: 'zzp', }, { n: '恐怖片', v: 'kbp', }, { n: '喜剧片', v: 'xjp', }, { n: '爱情片', v: 'aqp', }, { n: '剧情片', v: 'jqp', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '中国', v: '/area/中国', }, { n: '大陆', v: '/area/大陆', }, { n: '内地', v: '/area/内地', }, { n: '香港', v: '/area/香港', }, { n: '台湾', v: '/area/台湾', }, { n: '日本', v: '/area/日本', }, { n: '韩国', v: '/area/韩国', }, { n: '俄罗斯', v: '/area/俄罗斯', }, { n: '澳大利亚', v: '/area/澳大利亚', }, { n: '泰国', v: '/area/泰国', }, { n: '新加坡', v: '/area/新加坡', }, { n: '马来西亚', v: '/area/马来西亚', }, { n: '越南', v: '/area/越南', }, { n: '印度', v: '/area/印度', }, { n: '巴基斯坦', v: '/area/巴基斯坦', }, { n: '伊朗', v: '/area/伊朗', }, { n: '菲律宾', v: '/area/菲律宾', }, { n: '美国', v: '/area/美国', }, { n: '英国', v: '/area/英国', }, { n: '德国', v: '/area/德国', }, { n: '丹麦', v: '/area/丹麦', }, { n: '巴西', v: '/area/巴西', }, { n: '西班牙', v: '/area/西班牙', }, { n: '加拿大', v: '/area/加拿大', }, { n: '法国', v: '/area/法国', }, { n: '意大利', v: '/area/意大利', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021', v: '/year/2021', }, { n: '2020', v: '/year/2020', }, { n: '2019', v: '/year/2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', },], },],
        "dianshiju": [{ key: '分类', name: '分类', value: [{ n: '全部', v: 'dianshiju', }, { n: '国产剧', v: 'gcj', }, { n: '热门短剧', v: 'rmdj', }, { n: '港台剧', v: 'gtj', }, { n: '日韩剧', v: 'rhj', }, { n: '海外剧', v: 'hwj', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '中国', v: '/area/中国', }, { n: '大陆', v: '/area/大陆', }, { n: '内地', v: '/area/内地', }, { n: '香港', v: '/area/香港', }, { n: '台湾', v: '/area/台湾', }, { n: '日本', v: '/area/日本', }, { n: '韩国', v: '/area/韩国', }, { n: '俄罗斯', v: '/area/俄罗斯', }, { n: '澳大利亚', v: '/area/澳大利亚', }, { n: '泰国', v: '/area/泰国', }, { n: '新加坡', v: '/area/新加坡', }, { n: '马来西亚', v: '/area/马来西亚', }, { n: '越南', v: '/area/越南', }, { n: '印度', v: '/area/印度', }, { n: '巴基斯坦', v: '/area/巴基斯坦', }, { n: '伊朗', v: '/area/伊朗', }, { n: '菲律宾', v: '/area/菲律宾', }, { n: '美国', v: '/area/美国', }, { n: '英国', v: '/area/英国', }, { n: '德国', v: '/area/德国', }, { n: '丹麦', v: '/area/丹麦', }, { n: '巴西', v: '/area/巴西', }, { n: '西班牙', v: '/area/西班牙', }, { n: '加拿大', v: '/area/加拿大', }, { n: '法国', v: '/area/法国', }, { n: '意大利', v: '/area/意大利', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021', v: '/year/2021', }, { n: '2020', v: '/year/2020', }, { n: '2019', v: '/year/2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', },], },],
        "dongmna": [{ key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '中国', v: '/area/中国', }, { n: '大陆', v: '/area/大陆', }, { n: '内地', v: '/area/内地', }, { n: '香港', v: '/area/香港', }, { n: '台湾', v: '/area/台湾', }, { n: '日本', v: '/area/日本', }, { n: '韩国', v: '/area/韩国', }, { n: '俄罗斯', v: '/area/俄罗斯', }, { n: '澳大利亚', v: '/area/澳大利亚', }, { n: '泰国', v: '/area/泰国', }, { n: '新加坡', v: '/area/新加坡', }, { n: '马来西亚', v: '/area/马来西亚', }, { n: '越南', v: '/area/越南', }, { n: '印度', v: '/area/印度', }, { n: '巴基斯坦', v: '/area/巴基斯坦', }, { n: '伊朗', v: '/area/伊朗', }, { n: '菲律宾', v: '/area/菲律宾', }, { n: '美国', v: '/area/美国', }, { n: '英国', v: '/area/英国', }, { n: '德国', v: '/area/德国', }, { n: '丹麦', v: '/area/丹麦', }, { n: '巴西', v: '/area/巴西', }, { n: '西班牙', v: '/area/西班牙', }, { n: '加拿大', v: '/area/加拿大', }, { n: '法国', v: '/area/法国', }, { n: '意大利', v: '/area/意大利', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021', v: '/year/2021', }, { n: '2020', v: '/year/2020', }, { n: '2019', v: '/year/2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', },], },],
        "zongyi": [{ key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '中国', v: '/area/中国', }, { n: '大陆', v: '/area/大陆', }, { n: '内地', v: '/area/内地', }, { n: '香港', v: '/area/香港', }, { n: '台湾', v: '/area/台湾', }, { n: '日本', v: '/area/日本', }, { n: '韩国', v: '/area/韩国', }, { n: '俄罗斯', v: '/area/俄罗斯', }, { n: '澳大利亚', v: '/area/澳大利亚', }, { n: '泰国', v: '/area/泰国', }, { n: '新加坡', v: '/area/新加坡', }, { n: '马来西亚', v: '/area/马来西亚', }, { n: '越南', v: '/area/越南', }, { n: '印度', v: '/area/印度', }, { n: '巴基斯坦', v: '/area/巴基斯坦', }, { n: '伊朗', v: '/area/伊朗', }, { n: '菲律宾', v: '/area/菲律宾', }, { n: '美国', v: '/area/美国', }, { n: '英国', v: '/area/英国', }, { n: '德国', v: '/area/德国', }, { n: '丹麦', v: '/area/丹麦', }, { n: '巴西', v: '/area/巴西', }, { n: '西班牙', v: '/area/西班牙', }, { n: '加拿大', v: '/area/加拿大', }, { n: '法国', v: '/area/法国', }, { n: '意大利', v: '/area/意大利', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2025', v: '/year/2025', }, { n: '2024', v: '/year/2024', }, { n: '2023', v: '/year/2023', }, { n: '2022', v: '/year/2022', }, { n: '2021', v: '/year/2021', }, { n: '2020', v: '/year/2020', }, { n: '2019', v: '/year/2019', }, { n: '2018', v: '/year/2018', }, { n: '2017', v: '/year/2017', }, { n: '2016', v: '/year/2016', }, { n: '2015', v: '/year/2015', }, { n: '2014', v: '/year/2014', }, { n: '2013', v: '/year/2013', }, { n: '2012', v: '/year/2012', }, { n: '2011', v: '/year/2011', }, { n: '2010', v: '/year/2010', }, { n: '2009', v: '/year/2009', }, { n: '2008', v: '/year/2008', }, { n: '2007', v: '/year/2007', }, { n: '2006', v: '/year/2006', }, { n: '2005', v: '/year/2005', }, { n: '2004', v: '/year/2004', }, { n: '2003', v: '/year/2003', }, { n: '2002', v: '/year/2002', }, { n: '2001', v: '/year/2001', }, { n: '2000', v: '/year/2000', },], },],
    },
    filter_url: '{{fl.分类}}{{fl.地区}}/page/2{{fl.年份}}',
    filter_def: { dianying: { 分类: 'dianying' }, dianshiju: { 分类: 'dianshiju' }, dongmna: { 分类: 'dongmna' }, zongyi: { 分类: 'zongyi' } },
}