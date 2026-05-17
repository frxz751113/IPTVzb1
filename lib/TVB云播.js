var rule = {
    title: 'TVB云播',
    //模板:'mxpro',
    host: 'http://www.tvyb09.com', //http://www.hktvyb.vip/发布页
    url: 'vod/show/id/fyfilter.html',
    filterable: 1, //是否启用分类筛选,
    filter_url: '{{fl.cateId}}{{fl.area}}{{fl.by}}{{fl.class}}{{fl.lang}}{{fl.letter}}/page/fypage{{fl.year}}',
    class_name: '电影&电视剧&综艺&动漫&日韩剧&国产剧&欧美剧&港台剧',
    class_url: '1&2&3&4&16&13&15&14',
    filter: 'H4sIAAAAAAAAA+2Z7VIiRxSG74XfVjGDrh97B7mG1P5gN1SyFWOq1KTK2rJKRRDUCFouLgt+ZUXQiIIao0OQm5nuGe4iA92cPn3GWsbSpDYJP33O6+nutxv6ZeZdyAy9/Ppd6PvYXOhl6E10NvbVN6Gh0FT0h5j3t1NvsL017++fo5M/xbrCKQ+zRKUdr3Sw94cZmh+SeLViN4tOekVWRlUlV2TpsqqMQcVJ1Xk8oSrjqlLeZHcNVZmACl/M8oWcqpiGGihd1tqZanY89cG20qgUCc2/6hTl0iejMzNq5aLR51dOlidpuNspLJm+Tl0imb4sXSKZ7jAZSDDdNjKQYLpJpItgullkLoL1JG71mK2f6hLJYC6rF06TSCRDK3K2G74VdRhISiu+FUkG060e2/cHZLqCQZfkVjt/QroIBl32Tr01ki6CgWTpzMltEolgIImv8qWPRCIY+NLIsMQt8UWwnqS9u8U/lHSJZDBQbsVNW2QgwWDR9+fO9u+sWSfrBgzCzJH7iR4JwUCykWSZSyIRDI5EK+vtHTkSgqltKPLdTboNXQaS5ZbzG1m6ZGBgc9NpFB9amlbBn+/odCyKPt7FGlu3gn68j8rtfLI3TqdRWCLYreM8v73QFBIpg2v87l7vIRCs6X6DFZqaQiLY8Kv3VCERbMBanSokgh47JV4803sIBGvZP6E9JFKn6g+qkEjNtOafaU3r8UuNWcd6D4Ggx3LGc5mlTvQ2QGHNpZaTqTrpvL5soOqb5oCvtbx/1gcFCrrEjd3I6SKB8HGajE59q46Te1F1KwtBj1Oh6el7A3QahSVC20gVEsFhuTyiConQNlKFROgoUIVE6MD5FAKho+Bbi0DITnYe1xUCYTvnYtFp9Om8u7YbzYB2RozISK99p024C1B1mFaHcTVCqxFcNWnVxFWDVg1UNSdI1ZzA1XFaHcfVMVodw9VRWh3F1Re0+gJXqVcm9sqkXpnYK5N6ZWKvTOqVib0yqVcm9sqgXhnYK4N6ZWCvDOqVgb0yqFcG9sqgXhnYK4N65QF8aF/PqSPLN7aYlQl4ZPnOTXvnutf89Vx49q3XpFe1LYvXtlH1u7ezM+q74WKZpZKoOvPmx+lYZ16vhkKRJ2b5CP6Ssq2ySrXoIHjXmnd1odII/krp3BWqpOzkZ+XOdaZKo88Xv/uHlwBxii3esHiGdBHsETmfnd8wq0okgj0uFffL+QFScYCcHyDUBQir9t2hL9RJplJxgucvdIlkMJf3SV/8lgzlPt8GSPbw9S27+O/vp8TBZMLT6wFBoOAR6jkCY/8oFyRS9gtqASJlrualKLZ7qLcB+rhgNUgCgyTwr0sC/4tfA8GS/JcXioZxKHpCzGgvpJ3yAskQguFbbnnff8t5DKZ63nJrKV0iGXTZqvJVElYkU2Yl+C25lCVTW35l32XJdAVD90P7E5muZCCxTtn5HpEIBnMpXPqfQwkGXbb3+TV9KCmYSpW3PJWxrS3fEyStAjZe/+qFEGKjYNCxvuQurpNegv1jSUBkZf1iFEiPzPQW7yA9OesKgQZfQYOHCYMI8d+IEF/evTnyTPdmgEsxwEsrJ151D8ntKxkMtFFxskkykGAgye45Z/T9jWDqS73viyI3u+tukLdjksFAB4esQJ4DSPaIH/m8aPnfSAkGc+n/ziXAyzxW88y+JnMRDEtKV36Jx2CPju7tP8mrL8nUA4d9liqQLoKpI3vJqiS4SAYDFVZ5nkQOyZS7ddbaoe522cO3yd/yqKD7FE0PCAIF/xH/mev/UT+sBwFhEBAGAWEQEJ4rIMz/BZ2B9n47JAAA',
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
        13: {
            cateId: '13'
        },
        14: {
            cateId: '14'
        },
        15: {
            cateId: '15'
        },
        16: {
            cateId: '16'
        }
    },
    searchUrl: '/vod/search/wd/**.html',//http://www.tvyb09.com/vod/search/wd/%E5%AD%A4%E8%88%9F%E4%B9%8B%E5%9F%8E1994.html
    searchable: 2, //是否启用全局搜索,
    quickSearch: 0, //是否启用快速搜索,
    play_parse: true,
    sniffer: 1,//https://c.weimobwmc.com/ol-6NoTV/05cf1687dfa143ea921db83f9cc8a762.mp4
    isVideo:'.m3u8',
    lazy: $js.toString(() => {
        let html = request(input);
        let hconf = html.match(/r player_.*?=(.*?)</)[1];
        let json = JSON.parse(hconf);
        let url = json.url;
        if (json.encrypt == '1') {
            url = unescape(url);
        } else if (json.encrypt == '2') {
            url = unescape(base64Decode(url));
        }
        if (/\.(m3u8|mp4|m4a|mp3)/.test(url)) {
            input = {
                parse: 0,
                jx: 0,
                url: url,
            };
        } else {
            let js = 'document.querySelector(".up-file").click()';//contentWindow.document.querySelector
            input = {
                parse: 1,
                url: 'https://jx.nnxv.cn/tv.php?url=' + url,
                click: js,
                js: js,
            };
        }
    }),

    limit: 6,
    tab_exclude: '热门资讯',
    推荐: 'ul.myui-vodlist;li;*;*;*;*',
    double: true, // 推荐内容是否双层定位
    一级: '.myui-vodlist__box;a&&title;.lazyload&&data-original;.tag&&Text;a&&href',
    二级: {
        "title": "h1&&Text;.data:eq(0) a:eq(0)&&Text",
        "img": ".lazyload&&data-original",
        "desc": ";.data:eq(0) a:eq(2)&&Text;.data:eq(0) a:eq(1)&&Text;.data:eq(2)&&Text;.data:eq(3)&&Text",
        "content": ".text-collapse span&&Text",
        "tabs": ".myui-panel__head h3",
        "lists": ".myui-content__list:eq(#id) li"
    },
    搜索: 'ul.myui-vodlist__media li;*;*;*;*',
}