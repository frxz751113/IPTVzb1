function verifyLogin(url) {
    let cnt = 0;
    let cookie = '';
    let r = Math.random();
    let yzm_url = getHome(url) + '/index.php/verify/index.html';
    log(`验证码链接:${yzm_url}`);
    let submit_url = getHome(url) + '/index.php/ajax/verify_check';
    log(`post登录链接:${submit_url}`);
    while (cnt < OCR_RETRY) {
        try {
            let { cookie, html } = reqCookie(yzm_url + '?r=' + r, { toBase64: true });
            let code = OcrApi.classification(html);
            log(`第${cnt + 1}次验证码识别结果:${code}`);
            html = post(submit_url, {
                headers: { Cookie: cookie },
                body: 'type=search&verify=' + code,
            });
            html = JSON.parse(html);
            if (html.code === 1) {
                log(`第${cnt + 1}次验证码提交成功`);
                log(cookie);
                return cookie // 需要返回cookie
            } else if (html.code !== 1 && cnt + 1 >= OCR_RETRY) {
                cookie = ''; // 需要清空返回cookie
            }
        } catch (e) {
            log(`第${cnt + 1}次验证码提交失败:${e.message}`);
            if (cnt + 1 >= OCR_RETRY) {
                cookie = '';
            }
        }
        cnt += 1
    }
    return cookie
}

globalThis.verifyLogin = verifyLogin;

var rule = {
    类型: '影视',//影视|听书|漫画|小说
    title: '面包网',
    host: 'https://v.aiwule.com',
    url: '/vodshow/fyfilter.html',
    searchUrl: '/vodsearch/**----------fypage---.html',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 5000,
    class_parse: '.nav a;a&&Text;a&&href;/(\\d+)\.html',
    filter: {
        '20': [{ key: '分类', name: '分类', value: [{ n: '全部', v: '20', }, { n: '动作', v: '24', }, { n: '喜剧', v: '25', }, { n: '爱情', v: '26', }, { n: '科幻', v: '27', }, { n: '恐怖', v: '28', }, { n: '剧情', v: '29', }, { n: '战争', v: '30', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '大陆', v: '大陆', }, { n: '香港', v: '香港', }, { n: '台湾', v: '台湾', }, { n: '美国', v: '美国', }, { n: '韩国', v: '韩国', }, { n: '日本', v: '日本', }, { n: '泰国', v: '泰国', }, { n: '新加坡', v: '新加坡', }, { n: '马来西亚', v: '马来西亚', }, { n: '印度', v: '印度', }, { n: '英国', v: '英国', }, { n: '法国', v: '法国', }, { n: '加拿大', v: '加拿大', }, { n: '西班牙', v: '西班牙', }, { n: '俄罗斯', v: '俄罗斯', }, { n: '其它', v: '其它', },], }, { key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '爱情', v: '爱情', }, { n: '动作', v: '动作', }, { n: '喜剧', v: '喜剧', }, { n: '战争', v: '战争', }, { n: '科幻', v: '科幻', }, { n: '剧情', v: '剧情', }, { n: '武侠', v: '武侠', }, { n: '冒险', v: '冒险', }, { n: '枪战', v: '枪战', }, { n: '恐怖', v: '恐怖', }, { n: '微电影', v: '微电影', }, { n: '其它', v: '其它', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '国语', v: '国语', }, { n: '英语', v: '英语', }, { n: '粤语', v: '粤语', }, { n: '闽南语', v: '闽南语', }, { n: '韩语', v: '韩语', }, { n: '日语', v: '日语', }, { n: '法语', v: '法语', }, { n: '德语', v: '德语', }, { n: '其它', v: '其它', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2024', v: '2024', }, { n: '2023', v: '2023', }, { n: '2022', v: '2022', }, { n: '2021', v: '2021', }, { n: '2020', v: '2020', }, { n: '2019', v: '2019', }, { n: '2018', v: '2018', },], }, { key: '字母', name: '字母', value: [{ n: '全部', v: '', }, { n: 'A', v: 'A', }, { n: 'B', v: 'B', }, { n: 'C', v: 'C', }, { n: 'D', v: 'D', }, { n: 'E', v: 'E', }, { n: 'F', v: 'F', }, { n: 'G', v: 'G', }, { n: 'H', v: 'H', }, { n: 'I', v: 'I', }, { n: 'J', v: 'J', }, { n: 'K', v: 'K', }, { n: 'L', v: 'L', }, { n: 'M', v: 'M', }, { n: 'N', v: 'N', }, { n: 'O', v: 'O', }, { n: 'P', v: 'P', }, { n: 'Q', v: 'Q', }, { n: 'R', v: 'R', }, { n: 'S', v: 'S', }, { n: 'T', v: 'T', }, { n: 'U', v: 'U', }, { n: 'V', v: 'V', }, { n: 'W', v: 'W', }, { n: 'X', v: 'X', }, { n: 'Y', v: 'Y', }, { n: 'Z', v: 'Z', },], }, { key: '排序', name: '排序', value: [{ n: '最近更新', v: 'time', }, { n: '最多播放', v: 'hits', }, { n: '最好评', v: 'score', },], },],
        '21': [{ key: '分类', name: '分类', value: [{ n: '全部', v: '21', }, { n: '国产', v: '31', }, { n: '香港', v: '32', }, { n: '韩国', v: '33', }, { n: '欧美', v: '34', }, { n: '台湾', v: '36', }, { n: '日本', v: '37', }, { n: '泰国', v: '38', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '大陆', v: '大陆', }, { n: '香港', v: '香港', }, { n: '台湾', v: '台湾', }, { n: '美国', v: '美国', }, { n: '韩国', v: '韩国', }, { n: '日本', v: '日本', }, { n: '泰国', v: '泰国', }, { n: '新加坡', v: '新加坡', }, { n: '马来西亚', v: '马来西亚', }, { n: '印度', v: '印度', }, { n: '英国', v: '英国', }, { n: '法国', v: '法国', }, { n: '加拿大', v: '加拿大', }, { n: '西班牙', v: '西班牙', }, { n: '俄罗斯', v: '俄罗斯', }, { n: '其它', v: '其它', },], }, { key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '爱情', v: '爱情', }, { n: '动作', v: '动作', }, { n: '喜剧', v: '喜剧', }, { n: '战争', v: '战争', }, { n: '科幻', v: '科幻', }, { n: '剧情', v: '剧情', }, { n: '武侠', v: '武侠', }, { n: '冒险', v: '冒险', }, { n: '枪战', v: '枪战', }, { n: '恐怖', v: '恐怖', }, { n: '微电影', v: '微电影', }, { n: '其它', v: '其它', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '国语', v: '国语', }, { n: '英语', v: '英语', }, { n: '粤语', v: '粤语', }, { n: '闽南语', v: '闽南语', }, { n: '韩语', v: '韩语', }, { n: '日语', v: '日语', }, { n: '法语', v: '法语', }, { n: '德语', v: '德语', }, { n: '其它', v: '其它', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2024', v: '2024', }, { n: '2023', v: '2023', }, { n: '2022', v: '2022', }, { n: '2021', v: '2021', }, { n: '2020', v: '2020', }, { n: '2019', v: '2019', }, { n: '2018', v: '2018', },], }, { key: '字母', name: '字母', value: [{ n: '全部', v: '', }, { n: 'A', v: 'A', }, { n: 'B', v: 'B', }, { n: 'C', v: 'C', }, { n: 'D', v: 'D', }, { n: 'E', v: 'E', }, { n: 'F', v: 'F', }, { n: 'G', v: 'G', }, { n: 'H', v: 'H', }, { n: 'I', v: 'I', }, { n: 'J', v: 'J', }, { n: 'K', v: 'K', }, { n: 'L', v: 'L', }, { n: 'M', v: 'M', }, { n: 'N', v: 'N', }, { n: 'O', v: 'O', }, { n: 'P', v: 'P', }, { n: 'Q', v: 'Q', }, { n: 'R', v: 'R', }, { n: 'S', v: 'S', }, { n: 'T', v: 'T', }, { n: 'U', v: 'U', }, { n: 'V', v: 'V', }, { n: 'W', v: 'W', }, { n: 'X', v: 'X', }, { n: 'Y', v: 'Y', }, { n: 'Z', v: 'Z', },], }, { key: '排序', name: '排序', value: [{ n: '最近更新', v: 'time', }, { n: '最多播放', v: 'hits', }, { n: '最好评', v: 'score', },], },],
        '22': [{ key: '分类', name: '分类', value: [{ n: '全部', v: '22', }, { n: '大陆', v: '39', }, { n: '港台', v: '40', }, { n: '日韩', v: '41', }, { n: '欧美', v: '42', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '大陆', v: '大陆', }, { n: '香港', v: '香港', }, { n: '台湾', v: '台湾', }, { n: '美国', v: '美国', }, { n: '韩国', v: '韩国', }, { n: '日本', v: '日本', }, { n: '泰国', v: '泰国', }, { n: '新加坡', v: '新加坡', }, { n: '马来西亚', v: '马来西亚', }, { n: '印度', v: '印度', }, { n: '英国', v: '英国', }, { n: '法国', v: '法国', }, { n: '加拿大', v: '加拿大', }, { n: '西班牙', v: '西班牙', }, { n: '俄罗斯', v: '俄罗斯', }, { n: '其它', v: '其它', },], }, { key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '爱情', v: '爱情', }, { n: '动作', v: '动作', }, { n: '喜剧', v: '喜剧', }, { n: '战争', v: '战争', }, { n: '科幻', v: '科幻', }, { n: '剧情', v: '剧情', }, { n: '武侠', v: '武侠', }, { n: '冒险', v: '冒险', }, { n: '枪战', v: '枪战', }, { n: '恐怖', v: '恐怖', }, { n: '微电影', v: '微电影', }, { n: '其它', v: '其它', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '国语', v: '国语', }, { n: '英语', v: '英语', }, { n: '粤语', v: '粤语', }, { n: '闽南语', v: '闽南语', }, { n: '韩语', v: '韩语', }, { n: '日语', v: '日语', }, { n: '法语', v: '法语', }, { n: '德语', v: '德语', }, { n: '其它', v: '其它', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2024', v: '2024', }, { n: '2023', v: '2023', }, { n: '2022', v: '2022', }, { n: '2021', v: '2021', }, { n: '2020', v: '2020', }, { n: '2019', v: '2019', }, { n: '2018', v: '2018', },], }, { key: '字母', name: '字母', value: [{ n: '全部', v: '', }, { n: 'A', v: 'A', }, { n: 'B', v: 'B', }, { n: 'C', v: 'C', }, { n: 'D', v: 'D', }, { n: 'E', v: 'E', }, { n: 'F', v: 'F', }, { n: 'G', v: 'G', }, { n: 'H', v: 'H', }, { n: 'I', v: 'I', }, { n: 'J', v: 'J', }, { n: 'K', v: 'K', }, { n: 'L', v: 'L', }, { n: 'M', v: 'M', }, { n: 'N', v: 'N', }, { n: 'O', v: 'O', }, { n: 'P', v: 'P', }, { n: 'Q', v: 'Q', }, { n: 'R', v: 'R', }, { n: 'S', v: 'S', }, { n: 'T', v: 'T', }, { n: 'U', v: 'U', }, { n: 'V', v: 'V', }, { n: 'W', v: 'W', }, { n: 'X', v: 'X', }, { n: 'Y', v: 'Y', }, { n: 'Z', v: 'Z', },], }, { key: '排序', name: '排序', value: [{ n: '最近更新', v: 'time', }, { n: '最多播放', v: 'hits', }, { n: '最好评', v: 'score', },], },],
        '23': [{ key: '分类', name: '分类', value: [{ n: '全部', v: '23', }, { n: '国产', v: '43', }, { n: '日韩', v: '44', },], }, { key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '大陆', v: '大陆', }, { n: '香港', v: '香港', }, { n: '台湾', v: '台湾', }, { n: '美国', v: '美国', }, { n: '韩国', v: '韩国', }, { n: '日本', v: '日本', }, { n: '泰国', v: '泰国', }, { n: '新加坡', v: '新加坡', }, { n: '马来西亚', v: '马来西亚', }, { n: '印度', v: '印度', }, { n: '英国', v: '英国', }, { n: '法国', v: '法国', }, { n: '加拿大', v: '加拿大', }, { n: '西班牙', v: '西班牙', }, { n: '俄罗斯', v: '俄罗斯', }, { n: '其它', v: '其它', },], }, { key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '爱情', v: '爱情', }, { n: '动作', v: '动作', }, { n: '喜剧', v: '喜剧', }, { n: '战争', v: '战争', }, { n: '科幻', v: '科幻', }, { n: '剧情', v: '剧情', }, { n: '武侠', v: '武侠', }, { n: '冒险', v: '冒险', }, { n: '枪战', v: '枪战', }, { n: '恐怖', v: '恐怖', }, { n: '微电影', v: '微电影', }, { n: '其它', v: '其它', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '国语', v: '国语', }, { n: '英语', v: '英语', }, { n: '粤语', v: '粤语', }, { n: '闽南语', v: '闽南语', }, { n: '韩语', v: '韩语', }, { n: '日语', v: '日语', }, { n: '法语', v: '法语', }, { n: '德语', v: '德语', }, { n: '其它', v: '其它', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2024', v: '2024', }, { n: '2023', v: '2023', }, { n: '2022', v: '2022', }, { n: '2021', v: '2021', }, { n: '2020', v: '2020', }, { n: '2019', v: '2019', }, { n: '2018', v: '2018', },], }, { key: '字母', name: '字母', value: [{ n: '全部', v: '', }, { n: 'A', v: 'A', }, { n: 'B', v: 'B', }, { n: 'C', v: 'C', }, { n: 'D', v: 'D', }, { n: 'E', v: 'E', }, { n: 'F', v: 'F', }, { n: 'G', v: 'G', }, { n: 'H', v: 'H', }, { n: 'I', v: 'I', }, { n: 'J', v: 'J', }, { n: 'K', v: 'K', }, { n: 'L', v: 'L', }, { n: 'M', v: 'M', }, { n: 'N', v: 'N', }, { n: 'O', v: 'O', }, { n: 'P', v: 'P', }, { n: 'Q', v: 'Q', }, { n: 'R', v: 'R', }, { n: 'S', v: 'S', }, { n: 'T', v: 'T', }, { n: 'U', v: 'U', }, { n: 'V', v: 'V', }, { n: 'W', v: 'W', }, { n: 'X', v: 'X', }, { n: 'Y', v: 'Y', }, { n: 'Z', v: 'Z', },], }, { key: '排序', name: '排序', value: [{ n: '最近更新', v: 'time', }, { n: '最多播放', v: 'hits', }, { n: '最好评', v: 'score', },], },],
        '47': [{ key: '地区', name: '地区', value: [{ n: '全部', v: '', }, { n: '大陆', v: '大陆', },], }, { key: '剧情', name: '剧情', value: [{ n: '全部', v: '', }, { n: '女频恋爱', v: '女频恋爱', }, { n: '反转爽剧', v: '反转爽剧', }, { n: '脑洞悬疑', v: '脑洞悬疑', }, { n: '年代穿越', v: '年代穿越', }, { n: '古装仙侠', v: '古装仙侠', }, { n: '现代都市', v: '现代都市', },], }, { key: '语言', name: '语言', value: [{ n: '全部', v: '', }, { n: '国语', v: '国语', },], }, { key: '年份', name: '年份', value: [{ n: '全部', v: '', }, { n: '2024', v: '2024', }, { n: '2023', v: '2023', },], }, { key: '字母', name: '字母', value: [{ n: '全部', v: '', }, { n: 'A', v: 'A', }, { n: 'B', v: 'B', }, { n: 'C', v: 'C', }, { n: 'D', v: 'D', }, { n: 'E', v: 'E', }, { n: 'F', v: 'F', }, { n: 'G', v: 'G', }, { n: 'H', v: 'H', }, { n: 'I', v: 'I', }, { n: 'J', v: 'J', }, { n: 'K', v: 'K', }, { n: 'L', v: 'L', }, { n: 'M', v: 'M', }, { n: 'N', v: 'N', }, { n: 'O', v: 'O', }, { n: 'P', v: 'P', }, { n: 'Q', v: 'Q', }, { n: 'R', v: 'R', }, { n: 'S', v: 'S', }, { n: 'T', v: 'T', }, { n: 'U', v: 'U', }, { n: 'V', v: 'V', }, { n: 'W', v: 'W', }, { n: 'X', v: 'X', }, { n: 'Y', v: 'Y', }, { n: 'Z', v: 'Z', },], }, { key: '排序', name: '排序', value: [{ n: '最近更新', v: 'time', }, { n: '最多播放', v: 'hits', }, { n: '最好评', v: 'score', },], },],
    },
    filter_url: '{{fl.分类}}-{{fl.地区}}-{{fl.排序}}-{{fl.剧情}}-{{fl.语言}}-{{fl.字母}}---fypage---{{fl.年份}}',
    filter_def: { '20': { 分类: '20' }, '21': { 分类: '21' }, '22': { 分类: '22' }, '23': { 分类: '23' }, '47': { 分类: '47' } },
    cate_exclude: '影视资讯',
    play_parse: true,
    lazy: $js.toString(() => {
        input = { parse: 1, url: input, js: '' };
    }),
    double: true,
    推荐: '*',
    一级: '.vod-list li;.pic a&&title;.lazyload&&data-original||data-background;.text-overflow&&Text;.pic a&&href',
    二级: {
        title: 'h1&&Text;.info a:eq(2)&&Text',
        img: '.lazyload&&data-original||src',
        desc: '.info span:eq(5)&&Text;.info a:eq(6)&&Text;.info a:eq(5)&&Text;.text-row-2:eq(0)&&Text;.text-overflow:eq(3)&&Text',
        content: '.text&&Text',
        tabs: '.playlist-tab li',
        lists: '.ewave-playlist-content:eq(#id)&&a',
        tab_text: 'body&&Text',
        list_text: 'body&&Text',
        list_url: 'a&&href',
        list_url_prefix: '',
    },
    //搜索:'*',
    搜索: $js.toString(() => {
        let cookie = getItem(RULE_CK, '');
        //log('储存的cookie:' + cookie);

        let ret = request(MY_URL, {
            headers: {
                Referer: encodeUrl(MY_URL),
                Cookie: cookie,
            }
        });
        if (/请输入验证码/.test(ret)) {
            //log(ret);
            cookie = verifyLogin(MY_URL);
            if (cookie) {
                log(`本次成功过验证,cookie:${cookie}`);
                setItem(RULE_CK, cookie);
            } else {
                log(`本次验证失败,cookie:${cookie}`);
            }
            ret = request(MY_URL, {
                headers: {
                    Referer: encodeUrl(MY_URL),
                    Cookie: cookie,
                }
            });
        }
        //log(ret);
        let d = [];
        let html = ret;
        let list = pdfa(html, 'ul.row&&li');
        list.forEach(item => {
            var title = pdfh(item, '.pic&&a&&title');
            var pic = pdfh(item, '.lazyload&&data-original||data-background');
            var desc = pdfh(item, '.text-overflow&&Text');
            var content = pdfh(item, 'span:eq(6)&&Text');
            var url = pdfh(item, '.pic&&a&&href');

            if (title) {
                d.push({
                    title: title,
                    img: pic,
                    desc: desc,
                    content: content,
                    url: url
                });
            }
        });
        setResult(d);
    }),
    搜索验证标识: '系统安全验证',
}