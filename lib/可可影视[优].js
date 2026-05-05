var rule = {
    title: '可可影视[优]',
    host: 'https://www.kkys01.com',
    //host: 'https://www.kkys01.com',
    url: '/show/fyclass-fyfilter-fypage.html',
    filter_url: '{{fl.class}}-{{fl.area}}-{{fl.lang}}-{{fl.year}}-{{fl.by}}',
    searchUrl: '/search?k=**&page=fypage&t=',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {
        'User-Agent': 'MOBILE_UA',
        'Referer': HOST + '/',
        'X-Forwarded-For': `119.${Math.floor(Math.random()*254)+1}.${Math.floor(Math.random()*254)+1}.${Math.floor(Math.random()*254)+1}`
    
    },
    class_parse: '#nav-swiper&&.nav-swiper-slide;a&&Text;a&&href;/(\\w+).html',
    cate_exclude: 'Netflix|今日更新|专题列表|排行榜',
    tab_exclude: '可可影视提供',
    tab_remove: ['4K(高峰不卡)','4K(高峰不卡)1'],
    play_parse: true,
    limit: 9,
    lazy: $js.toString(() => {
        let kurl = input;
        let khtml = request(kurl);
        if (/dujia/.test(khtml)) {
            kurl = khtml.split("PPPP = '")[1].split("';")[0];
            const key = CryptoJS.enc.Utf8.parse('Isu7fOAvI6!&IKpAbVdhf&^F');
            const dataObj = {
                ciphertext: CryptoJS.enc.Base64.parse(kurl)
            };
            const decrypted = CryptoJS.AES.decrypt(dataObj, key, {
                mode: CryptoJS.mode.ECB,
                padding: CryptoJS.pad.Pkcs7
            });
            kurl = decrypted.toString(CryptoJS.enc.Utf8);
        } else {
            kurl = khtml.split('src: "')[1].split('",')[0];
        }
        input = {
            jx: 0,
            parse: 0,
            url: kurl,
            header: rule.headers
        };
    }),    
    预处理: $js.toString(() => {
        let hash = request(rule.host,{headers: rule.headers})?.match(/a0_0x2a54\s*=\s*\['([^']+)'/)?.[1]?.trim() ?? '';
        if (hash && hash !== getItem('myhash')) {
            setItem('mycookie', '');
            setItem('myhash', '');
            let idx = parseInt('0x' + hash[0], 16);
            for (let i = 0; i < 1000000; i++) {
                let input = hash + i;
                let sha1 = CryptoJS.SHA1(input).toString(CryptoJS.enc.Latin1);
                if (sha1.charCodeAt(idx) === 0xb0 && sha1.charCodeAt(idx + 1) === 0x0b) {
                    let cookie = `cdndefend_js_cookie=${input}`;
                    setItem('myhash', hash);
                    setItem('mycookie', cookie);
                    rule.headers['cookie'] = cookie;
                    break;
                }
            }
        } else if (getItem('mycookie')) {
            rule.headers['cookie'] = getItem('mycookie');
        }
        let khtml = fetch(rule.host, {headers: rule.headers});
        let tValue = khtml.match(/<input[^>]*name="t"[^>]*value="([^"]*)"/i);
        if (tValue && tValue[1]) {
            rule.searchUrl = rule.searchUrl + encodeURIComponent(tValue[1]);
        }
        let scripts = pdfa(khtml, 'script');
        let img_script = scripts.find((it) => pdfh(it, 'script&&src').includes('rdul.js'));
        if (img_script) {
            let img_url = img_script.match(/src="(.*?)"/)[1];
            let img_html = fetch(img_url);
            rule.img_host = img_html.match(/'(.*?)'/)[1];
            rule.图片替换 = rule.host + '=>' + rule.img_host;
        }
    }),
    推荐: '*',
    一级: '.module-item;.v-item-title:eq(1)&&Text;img:eq(-1)&&data-original;span:eq(-1)&&Text;a&&href',
    搜索:'.search-result-item;img&&alt;img&&data-original;.search-result-item-header&&Text;a&&href',    
    二级: {
        title: '.detail-title&&strong:eq(1)&&Text;.detail-tags&&Text',
        img: '.detail-pic&&img&&data-original',
        desc: '.detail-info-row-main:eq(-2)&&Text;.detail-tags-item:eq(0)&&Text;.detail-tags-item:eq(1)&&Text;.detail-info-row-main:eq(1)&&Text;.detail-info-row-main:eq(0)&&Text',
        content: '.detail-desc&&Text',
        tabs: '.source-item',
        tab_text: 'span:eq(-1)&&Text',
        lists: '.episode-list:eq(#id)&&a',
        list_text: 'body&&Text',
        list_url: 'a&&href',
    },    
    filter: 'H4sIAAAAAAAAA+2Zz08bVxDH7/4rKp852EBSnFsPrVSpyqU9VIqiyK3cKip1pdBWRQjJYBuMIdggx8SxC6RgMAn+AUGOWWP7n9m3u/4v+sy8mbdOqskqoTm0e0F85vt+7XvzdmbWC4FgOHjnk3uBheBPsfngneD3s9G5ueBEMB79OSbRPuuK3XXJv0dnf5OGewvBuDSLdG2YrI3MEoKLE2C9G/v1h9mHfyjz3c+/+eKrL78lVawdW8m0EhWQVqxIC2oApGVrZq+CGgBqduZMj6kANWspbyWKSlNAWjJrLT9DDYDGzDbt3gscE4C04y1x2UUNgMZcPrWLWzgmAD1DdVX3U0DayvawdIIaAI2ZeWoaazgmAPXbXBG5c+wHQFru0DmgvQYgrdEWRh01ANTMq32n0VKaAlpL/cjs7+NaALS24WR2SbsG2rO9ur22insG4Dpbu9DVZzsC0lID+2UVNQDUnKUNUTGUpmDx/uIEuXH0USyqvVhUWmLD8OjF4vB4WFrBPejURbmnTNhieFSyOs2xFsqk979lXfbHxwAT7Up/UxpxVwBoN3eqVuUUdxOA5t470f0U0K6sn2lNAY356onWFNBq+6+1poC0xy1hHKEGoMdsucdsufuZncsh9VNAz761K9IdfHYAmu/1hVMd4HwA2lv2rfWBPAxyGGSadZCyeztWkQ6HmNacyskOIoMXTjO1aBYkWjttbEHseuuIVkGk8aJoppOoDuyc9PQSHgYxzdJ/BfOaBr2H3CZ65nTb7OJbTMGYp89G4z9qT3eadaeW8Orp5Z5sj2MD0DOeH2pNgcvPtKbA5btaU+DyXa0pcPmnqx+A5z2Yj0UfuW775YXZ7Xncg8nQ5G1lu/7XZb+l7bfc9mltn3bbp7R9ym2f1PZJtz2s7WG3PaTtIbKHQ9ePdUBaOPRA/olQg9CbDUKjBiHdIDLeIByJhB7IP7rBzJsNZkYNZnQDq3xh7eDFGWmfRsbP4bt5fQrW5rYwcm+dgt29EvkMTqGHriSsIt6nSbfZTqJX6E11mimRwVf09GgNgfsTAdnvX8pkFHnJZLiMhMtyuKyDzSy4SM9kTlwWwGVHXCYzCmP0fAq8ZE5cJsNlQKPwR/Mp8JKtyDekPiMFXrJGLlMbJnuis4xrAbjhbIXMwRvOVric4n3zFC7f4PIUNhd5Z1bFZSRcJuNHWT/K+lHWW5SdvrEoaxsvRO8Jej8AaZU90zDs4wTKxLS8Rkv3VkBa6kzkDnRvzZ6+RnCVNRPDuerZLnfEARUMALTa7LJdbuBSAbxU1lw8cgZ5GfFxTADUvo5F536JK02BlzyEq+St/K59SjkKAGmlZ+YV5RMAfrXuxxw/5vgxx1vMmfpYlV22ZiWWrKuXY18ltclT9OC+aXLfuZm3OVvJcRUZV3Ux31e5tzlb4TJVJRc9pCs4zynUA+jImbVKWPco8FIZ292c6ysjAPXbfy7K9E4CQO2z+EPpViDB/15iqmmci3oeYwgAvR3/3Lae4k4r0PXmutxDXAmAlxr2H2v0G4qpXER7d7z9sGj6YdWq/wXc/wLu50l+nvR/zZNuv0eepM1urxgmVpy/yFMB6GYUKqKBcUkBLayUl1EMbwYA9TsZOO0s9gOg+VYf24U9nA/AS7bF/iLPxE82i2GyLfYXeS6DS7dFI6lv8Aj+czf4o96EkcsHFv8GMgdHLMEiAAA=',
}