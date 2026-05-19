var rule = {
    title: '追剧迷',
    模板: 'vfed',
    host: 'https://www.zhuijumi.cc',
    url: '/tvtype/fyfilter.html',
    searchUrl: '/vodsearch/**-fypage.html',
    class_parse: '.fed-navs-left a;a&&Text;a&&href;.*/(.*?).html',
    filter: {
        'film': [{ key: '分类', name: '分类', value: [{ n: '动作片', v: 'dongzuo', }, { n: '喜剧片', v: 'xiju', }, { n: '爱情片', v: 'aiqing', }, { n: '科幻片', v: 'kehuan', }, { n: '恐怖片', v: 'kongbu', }, { n: '剧情片', v: 'juqing', }, { n: '战争片', v: 'zhanzheng', }, { n: '记录片', v: 'jilu', }, { n: '犯罪片', v: 'fanzui', }, { n: '悬疑片', v: 'xuanyi', }, { n: '灾难片', v: 'zainan', }, { n: '奇幻片', v: 'qihuan', }, { n: '动画片', v: 'donghua', },], },],
        'dianshiju': [{ key: '分类', name: '分类', value: [{ n: '香港剧', v: 'xianggang', }, { n: '国产剧', v: 'guochan', }, { n: '欧美剧', v: 'oumeiju', }, { n: '日剧', v: 'riju', }, { n: '韩剧', v: 'hanju', }, { n: '海外剧', v: 'haiwaiju', }, { n: '微短剧', v: 'weiduanju', },], },],
        'dongman': [{ key: '分类', name: '分类', value: [{ n: '国产动漫', v: 'guochandongman', }, { n: '日本动漫', v: 'ribendongman', }, { n: '欧美动漫', v: 'oumeidongman', },], },],
        'zongyi': [{ key: '分类', name: '分类', value: [{ n: '大陆综艺', v: 'daluzongyi', }, { n: '港台综艺', v: 'gangtaizongyi', }, { n: '日韩综艺', v: 'rihanzongyi', }, { n: '欧美综艺', v: 'oumeizongyi', },], },],
    },
    filter_url: '{{fl.分类}}-fypage',
    filter_def: { 'film': { 分类: 'film' }, 'dianshiju': { 分类: 'dianshiju' }, 'dongman': { 分类: 'dongman' }, 'zongyi': { 分类: 'zongyi' } },
    filterable: 1,
    cate_exclude: '更多|申请|演员',
    lazy: `js:
        var html = JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);
        var url = html.url;
        if (html.encrypt == '1') {
            url = unescape(url)
        } else if (html.encrypt == '2') {
            url = unescape(base64Decode(url))
        }
        if (/\\.m3u8|\\.mp4/.test(url)) {
            input = {
                jx: 0,
                url: url,
                parse: 0
            }
        } else {
            input
        }
    `,
    二级: {
        "title": "h1&&Text;.fed-col-xs6--span:eq(0)&&Text",
        "img": ".fed-list-info&&a&&data-original",
        "desc": ".fed-col-xs12.fed-part-eone:eq(3)&&Text;;;.fed-col-xs12.fed-part-eone--span:eq(0)&&Text;.fed-col-xs12.fed-part-eone--span:eq(1)&&Text",
        "content": ".fed-conv-text:eq(0)&&Text",
        "tabs": "ul.fed-padding&&li",
        "lists": ".fed-tabs-btm:eq(#id) li"
    },
    搜索: '.fed-list-deta;h1&&Text;.fed-lazy&&data-original;.fed-list-remarks&&Text;a&&href;.fed-col-xs12.fed-part-eone:eq(2)&&Text',
}