var rule = {
    author: '小可乐/2502/第一版',
    title: 'BT天堂',
    类型: '影视',
    host: 'https://www.kundihulan.com',
    hostJs: '',
    headers: {
        'User-Agent': 'MOBILE_UA'
    },
    编码: 'utf-8',
    timeout: 5000,

    homeUrl: '/',
    url: '/vodshow/fyfilter.html',
    filter_url: '{{fl.cateId}}-{{fl.area}}-{{fl.by}}-{{fl.class}}-{{fl.lang}}-{{fl.letter}}---fypage---{{fl.year}}',
    detailUrl: '/video/fyid.html',
    searchUrl: '/index.php/ajax/suggest?mid=1&wd=**&page=fypage&limit=30',
    searchable: 1,
    quickSearch: 1,
    filterable: 1,

    limit: 9,
    double: false,
    class_name: '电影&剧集&综艺&动漫',
    class_url: '1&2&3&4',
    filter_def: {
        1: {
            cateId: '1'
        },
        2: {
            cateId: '2'
        },
        3: {
            cateId: '3'
        },
        4: {
            cateId: '4'
        }
    },

    play_parse: true,
    lazy: `js:
let kcode = JSON.parse(request(input).match(/var player_.*?=(.*?)</)[1]);
let kurl = kcode.url;
if (/\\.(m3u8|mp4)/.test(kurl)) {
    input = { jx: 0, parse: 0, url: kurl }
} else {
    input = { jx: 0, parse: 1, url: input }
}`,

    推荐: '*',
    一级: '.col8;a&&title;img&&data-original;.text&&Text;a&&href',
    二级: `js:
let khtml = request(input);
let jinput = pd(khtml, '.playbtn&&a&&href',input);
let jhtml = request(jinput);
let tab_arr = pdfa(jhtml, '.col-flex&&a');
let htmls = tab_arr.map((it) => { return request(pd(it, 'a&&href', input) ) });
let ktabs = [];
tab_arr.map((it) => { ktabs.push('👶' + pdfh(it, 'a&&Text')) });
let kplists = [];
htmls.forEach((ht) => {
    if (ht) {
        let plist = pdfa(ht, '.tzt-playlist.sort-list&&a:not(:contains(美女直播))').map((it) => { return pdfh(it, 'a&&Text') + '$' + pd(it, 'a&&href', input) });
        plist = plist.join('#');
        kplists.push(plist)
    } else {
        kplists.push('')
    }
});

VOD = {
vod_id: input,
vod_name: pdfh(khtml, 'h1&&Text'),
vod_pic: pdfh(khtml, '.shadow&&img&&data-original'),
type_name: pdfh(khtml, '.tag&&a:eq(0)&&Text'),
vod_remarks: pdfh(khtml, '.data:eq(-1)&&Text'),
vod_year: pdfh(khtml, '.tag&&a:eq(2)&&Text'),
vod_area: pdfh(khtml, '.tag&&a:eq(3)&&Text'),
vod_lang: pdfh(khtml, '.tag&&a:eq(4)&&Text'),
vod_director: pdfh(khtml, '.data--span:eq(1)&&Text'),
vod_actor: pdfh(khtml, '.data--span:eq(0)&&Text'),
vod_content: '👶' + pdfh(khtml, 'meta[name*=description]&&content'),
vod_play_from: ktabs.join('$$$'),
vod_play_url: kplists.join('$$$')
}
`,
    搜索: 'json:list;name;pic;en;id',

    filter: 'H4sIAAAAAAAAA+2YW08TQRTH3/sx9rkm3RYo8Mb9fr9DeKi4iUTEBKoJISQaKLYgVI20EustAVoUwhIVZMvly3S38C2cZc6cMxulaaDxad96fv8dZmZnz/+/y7xHUZXqMc+88kibU6qViVBYa3mgeJXp0GON1fnDrPlpldXPQlNPGRibV6YZNiOZq8WMjVmhKgtewCuZ3FkqH3sJSgUpiZQZS5MSRCUfPbQWI6RUkpJ+Y55kSalCxXrx2nqeIEX1kRR9nzNikiStLpZ2zKT6aSrjm3m2QVKASeMLXrwtoRktRDfFTOnmK6PwTaFZt9JXm8tAoRDa1c6m9fsANChwXFy3Ts7FOF7gcs/XzQ9noEGBN+DHBmlQCO1y9ZA0KHBccttK7YlxvMB1ft6lcVDgOs+PSYOC1qLLa9Ed49Z009gR43iB45bi7E6Z0V0xFGvcyfZFPr6fj22KzWBNz+IXa/WCDRNTYI1XRI5y2YSQeeE49TktNEOnbiWPrpI/izx1v89fBuz6p8QDxAMy9xP3y1wlrsrcR9wncbUKuVol80rilTIPEg/KvIJ4hczLiZfLnParyvtVab+qvF+V9qvK+1Vpv3bvyucxpYXDmnQi5n7SOlgr8kRqANQgqQVSi6QOSB2SeiD1SBqANCBpBNKIpAlIE5JmIM1IWoC0IGkF0oqkDUgbknYg7Ug6gHQg6QTSiaQLSBeSbiDdSHqA9CDpBdKLpA9IH5J+IP1IBoAMIBkEMohkCMgQkmEgw0hGgIwgGQUyisR3Tzzs9i/Hs3J/Turc9bemEf/rOaGGZkV4kl0q/m7OMCz9HSgPJ8Oz5DsHS2ZUuPnsxJMZzZ7WM+71KP675ih1gfXr2NxKsLwSCjWOtZe2DZ8kKfquDVaSyC64n0sSzcWG5Iw0SVKT8kSSJOprHkiSVH7jXLZ7lCpLlyPseuHYvCgmo26bs4UysXAG35x7BTM4obOYMj9+FUOxdjPLzSw3s9zMKnFmBe6aWdQd/NMmnz29jBmiG6in7ByJ607VERnMsZ0q9S+PPKca/C+ZwlctzJgXzjVTNtiFc8VC44Xr0q5Luy7tuvQtXLrsri4tvbfzt/2VjHX6XXQD9Sy3Macq/deNf3rIakD6+uDfLA5VLZ1LX69buDQvinlL/6cTu+/Srku7Lu26dAld2rPwB+GxdvVKGQAA'
}