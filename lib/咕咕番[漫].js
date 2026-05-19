//咕咕番发布页：gugu01.cc
var rule = {
    title: '咕咕番[漫]',
    host: "https://www.gugu3.com",
    class_name: "连载日漫&完结日漫&剧场&特摄",
    class_url: "6&7&21&23",
    //class_parse: '.head-nav li;a&&Text;a&&href;/(\\d+)\.html',
    searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
    searchable: 2,
    quickSearch: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    url: '/index.php/api/vod#type=fyclassfyfilter&page=fypage',
    filterable: 1,
    filter:'H4sIAAAAAAAAA+2X3U4TQRiG72WPOZhtpSC3YjhYyUaJFROKJoSQgAUsbYOLESqhFtA0FGmltcS0NMDNdPbnLpxl5vtJPOmZmMzZPu+7/Xbe2Zn5umtOzpl7tua88ledOWch7xUKzpSz5L32FUa9kWxUFL/z8m/9h/uWlCy3W0mxlcoKnPUprUbn+3I4MqoB8GR3Xzb7xjMAXhg0ova+8Qygt9eKgh3wNODz7vaS7yfwPA34u1pTDgbwOw3gJZ3PYf/AeAawZqkXFrehpgas+WsUbpWgpgasedIfDwOoqQGz73xKji4guwas2anGpQbU1IBjuWyE5Q0YiwbwxsMjNYUygGkjhjvi+0CW4R0ZwMrFTnyGlTXgaHfPaQYMoNf8QG/YACYZDMLSR0iiAb3TM3ncAU8DeqUv4WENPA3obVbUOwBPA46l3JP38DsD6AV78ucleBqw5vt2dIirTQN6/bPk67fo4AfYyDhzzYZaMTBzGtA7upMBrA8D+DY2q7J+A29DA5uB8c0uzUAK6/Opq/ekt+x7tCVlvSurNxNuSbXyw3qbtkEKbPvI41vaPinQcr4gzwAf0qrvLbMhDa/Ho9sJh5QRmSdGe7hkepb0LNczpGe47pLucl2QLpjuPkVdXTJ9lvRZrs+QPsP1HOk5rk+TPs11yuvyvC7ldXlel/K6PK9LeV2e16W8Ls8rKK/geQXlFTyvoLyC5xWUV/C8gvIKnldQXsHzCsoreF5BeQXPKyiv4HkF5VWXfFnmvaUXtCzjq07c2ph8p6j7aaekgJu30iPPANsp5BngQ3q+SgMKa7+T2vVfAwqru2F9Izzsmiori+puHNeDqc5oY75cXClwM77akiVokIWFN8t++vj5KWfGdnXb1W1Xd2xXn7ir2+OTjk/1j8Ken/b8tOenPT/tV5H9KoJL+1X0H7TurG3dtnXb1u081tZt+6Ttk4+wT/6jhrX+B8eBrnOCGwAA',
    filter_url: "&class={{fl.class}}&area={{fl.area}}&year={{fl.year}}&lang={{fl.lang}}&by={{fl.by}}",
    filter_def: "",
    filter_def: {},
    detailUrl: '/index.php/vod/detail/id/fyid.html',
    play_parse: true,
    sniffer: 1,
    is_video: 'obj/tos|bd.xhscdn|/ugc/',
    lazy: $js.toString(() => {
        input = {
            parse: 1,
            url: input,
            //js:'try{let urls=Array.from(document.querySelectorAll("iframe")).filter(x=>x.src.includes("?url="));if(urls){location.href=urls[0].src}}catch{}document.querySelector("button").click()',
            js: 'try{location.href=document.querySelector("#playleft iframe").src}catch{}document.querySelector("button.swal-button--confirm").click()',
            parse_extra: '&is_pc=1&custom_regex=' + rule.is_video,
        }
    }),
    limit: 6,
    推荐: '.border-box.public-r .public-list-box:gt(4);a&&title;img&&data-src;.public-list-prb&&Text;a&&href',
    一级: $js.toString(() => {
        let body = input.split("#")[1];
        let t = Math.round(new Date / 1e3).toString();
        let key = md5("DS" + t + "DCC147D11943AF75");
        let url = input.split("#")[0];
        body = body + "&time=" + t + "&key=" + key;
        print(body);
        fetch_params.body = body;
        let html = post(url, fetch_params);
        let data = JSON.parse(html);
        VODS = data.list.map(function (it) {
            it.vod_pic = urljoin2(input.split("/i")[0], it.vod_pic);
            return it
        });
    }),
    二级: {
        title: '.slide-info-title&&Text;.slide-info:eq(3)--strong&&Text',
        img: '.lazy&&data-src',
        desc: '.fraction&&Text;.slide-info-remarks:eq(1)&&Text;.slide-info-remarks:eq(2)&&Text;.slide-info:eq(2)--strong&&Text;.slide-info:eq(1)--strong&&Text',
        content: '#height_limit&&Text',
        tabs: '.anthology.wow.fadeInUp.animated&&.swiper-wrapper&&a',
        tab_text: '.swiper-slide&&Text',
        lists: '.anthology-list-box:eq(#id) li',
    },
    //搜索: 'json:list;name;pic;;id',
    搜索: $js.toString(() => {
        let html = fetch(input);
        let list = pdfa(html, ".public-list-box");
        VODS = list.map(x => {
            return {
                vod_name: pdfh(x, ".thumb-txt&&Text"),
                vod_pic: pdfh(x, ".lazy&&data-src"),
                vod_remarks: pdfh(x, ".public-list-prb&&Text"),
                vod_content: pdfh(x, ".thumb-blurb&&Text"),
                vod_id: pdfh(x, "a&&href")
            }
        });
    }),
    图片替换: '&amp;=>&',
}