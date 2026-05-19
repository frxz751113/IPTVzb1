var rule = {
    author: '小可乐/2504/第一版',
    title: '武德影院',
    类型: '影视',
    host: 'https://www.thshic.com',
    hostJs: '',
    headers: {
        'User-Agent': MOBILE_UA
    },
    编码: 'utf-8',
    timeout: 5000,

    homeUrl: '/',
    url: '/thssw/fyfilter.html',
    filter_url: '{{fl.cateId}}-{{fl.area}}-{{fl.by}}-{{fl.class}}-{{fl.lang}}-{{fl.letter}}---fypage---{{fl.year}}',
    searchUrl: '/thssc/**----------fypage---.html',
    detailUrl: '',

    limit: 9,
    double: false,
    class_name: '电影&剧集&综艺&动漫&短剧',
    class_url: '1&2&3&4&5',
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
        },
        5: {
            cateId: '5'
        }
    },

    推荐: '*',
    一级: '.col8;img&&alt;img&&data-original;p&&Text;a&&href',
    搜索: '*',
    二级: $js.toString(() => {
        let khtml = fetch(input);
        let jinput = pd(khtml, '.playbtn&&a&&href', HOST);
        let ptabs = pdfa(fetch(jinput), '.wrap&&a');
        let ktabs = ptabs.map((it) => {
            return '👶' + pdfh(it, 'body&&Text')
        });
        let plists = ptabs.map((it) => {
            let jurl = pd(it, 'a&&href', HOST);
            let plist = pdfh(fetch(jurl), '.sort-list:eq(0)&&Html');
            return plist
        });
        let kurls = plists.map((item) => {
            let kurl = pdfa(item, 'a:not([rel])').map((it) => {
                return pdfh(it, 'body&&Text') + '$' + pd(it, 'a&&href', HOST)
            });
            return kurl.join('#')
        });
        VOD = {
            vod_id: input,
            vod_name: pdfh(khtml, 'h1&&Text'),
            vod_pic: pdfh(khtml, '.shadow&&img&&data-original'),
            type_name: pdfh(khtml, '.tag&&Text'),
            vod_remarks: pdfh(khtml, '.data:eq(-1)&&Text'),
            vod_year: pdfh(khtml, '.tag&&a:eq(-3)&&Text'),
            vod_area: pdfh(khtml, '.tag&&a:eq(-2)&&Text'),
            vod_lang: pdfh(khtml, '.tag&&a:eq(-1)&&Text'),
            vod_director: pdfh(khtml, '.data:eq(1)--span&&Text'),
            vod_actor: pdfh(khtml, '.data:eq(0)--span&&Text'),
            vod_content: pdfh(khtml, 'meta[name*=description]&&content').split('讲述了:')[1],
            vod_play_from: ktabs.join('$$$'),
            vod_play_url: kurls.join('$$$')
        }
    }),

    play_parse: true,
    lazy: $js.toString(() => {
        let kcode = JSON.parse(fetch(input).split('aaaa=')[1].split('<')[0]);
        let kurl = kcode.url;
        if (/\.(m3u8|mp4)/.test(kurl)) {
            input = {
                jx: 0,
                parse: 0,
                url: kurl,
                header: rule.headers
            }
        } else {
            input = {
                jx: 0,
                parse: 1,
                url: input
            }
        }
    }),

    filter: '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'
}