globalThis.verifyBox = function(HOST, rule) {
    const firstRes = request(HOST, {
        headers: rule.headers,
        withHeaders: true,
        redirect: false,
        method: 'GET'
    });    
    const res = typeof firstRes === 'string' ? JSON.parse(firstRes) : firstRes;
    const html = res.body || firstRes;    
    if (!html.includes('人机验证') && !html.includes('防火墙正在检查您的访问')) {
        return html;
    }    
    const setCookie = res['set-cookie'] || '';
    let phpsessid = '';    
    if (Array.isArray(setCookie)) {
        for (const c of setCookie) {
            if (c.includes('PHPSESSID')) {
                phpsessid = c.split(';')[0].trim();
                break;
            }
        }
    } else if (setCookie.includes('PHPSESSID')) {
        phpsessid = setCookie.split(';')[0].trim();
    }    
    if (phpsessid) {
        rule.headers.cookie = phpsessid;
        if (typeof rule_fetch_params !== 'undefined') {
            rule_fetch_params.headers = {...rule.headers};
        }
    }    
    const tokenMatch = html.match(/var token = encrypt\("([^"]+)"\)/);
    if (!tokenMatch) return html;    
    const encrypt = (str) => {
        const staticchars = "PXhw7UT1B0a9kQDKZsjIASmOezxYG4CHo5Jyfg2b8FLpEvRr3WtVnlqMidu6cN";
        let encodechars = "";        
        for (let i = 0; i < str.length; i++) {
            const idx = staticchars.indexOf(str[i]);
            const code = idx === -1 ? str[i] : staticchars[(idx + 3) % 62];
            encodechars += staticchars[Math.floor(Math.random() * 62)] + 
                          code + 
                          staticchars[Math.floor(Math.random() * 62)];
        }        
        try {
            return btoa(encodechars);
        } catch (e) {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(encodechars).toString('base64');
            }
            return encodechars;
        }
    };    
    const value = encrypt(HOST);
    const token = encrypt(tokenMatch[1]);
    const postData = `value=${value}&token=${token}`;    
    const verifyRes = request(`${rule.host}/robot.php`, {
        headers: {
            ...rule.headers,
            'content-type': 'application/x-www-form-urlencoded',
            'origin': rule.host,
            'referer': HOST
        },
        withHeaders: true,
        method: 'POST',
        body: postData
    });    
    const verifyJson = typeof verifyRes === 'string' ? JSON.parse(verifyRes) : verifyRes;
    let verifyBody;    
    if (typeof verifyJson.body === 'string') {
        try {
            verifyBody = JSON.parse(verifyJson.body);
        } catch {
            verifyBody = {msg: 'error'};
        }
    } else {
        verifyBody = verifyJson.body || verifyJson;
    }    
    if (verifyBody.msg === 'ok') {
        const start = Date.now();
        while (Date.now() - start < 1500) {}        
        const finalRes = request(HOST, {
            headers: rule.headers,
            withHeaders: false,
            redirect: false,
            method: 'GET'
        });        
        return typeof finalRes === 'string' ? finalRes : (finalRes.body || finalRes);
    }    
    return html;
};

var rule = {
  title: '看看屋',
  //host:'https://www.kankanwu.cc',
  //hostJs: 'print(HOST);let html=request(HOST,{headers:{"User-Agent":PC_UA}});let src=jsp.pdfh(html,"ul&&li a:eq(1)&&href");print(src);HOST=src',
  host:'https://www.kankanwu.vip',
  hostJs: $js.toString(() => {
        rule.headers = rule.headers || {};
        let Html = globalThis.verifyBox(HOST, rule);
        let url = jsp.pdfh(Html, "ul li:first-child a&&href");
        HOST = url;
    }),
  url: '/vodshow/fyfilter.html',
  searchUrl: '/vodsearch/**----------fypage---.html',
  searchable:1,quickSearch:1,double:false,timeout:5000,play_parse:true,filterable:1,invalid:true,
  class_name:'电影&电视剧&动漫&综艺',
  class_url:'1&2&4&3',
  filter_url:'{{fl.类型}}-{{fl.area}}-{{fl.by}}-{{fl.class}}-----fypage---{{fl.year}}',
  filter_def:{'1':{类型:'1'},'2':{类型:'2'},'3':{类型:'3'},'4':{类型:'4'},},
  lazy: `js: 
    let pclick = 'document .querySelector("#playleft iframe").contentWindow.document.querySelector("#start").click()';
    input = { parse: 1, url: input, js: pclick, click: pclick}`,
  推荐: '*',
  一级: '.stui-vodlist li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href',
  二级: {
    title: '.stui-content__detail .title&&Text;.stui-content__detail&&p:eq(-2)&&a&&Text',
    title1: '.stui-content__detail .title&&Text;.stui-content__detail&&p&&Text',
    img: '.stui-content__thumb .lazyload&&data-original',
    desc: '.stui-content__detail p&&Text;.data.visible-xs:eq(2)&&Text;.data.visible-xs:eq(0)&&Text;.stui-content__detail p:eq(4)&&Text;.stui-content__detail&&p:eq(5)&&Text',
    desc1: '.stui-content__detail p:eq(4)&&Text;;;.stui-content__detail p:eq(1)&&Text',
    content: '.detail&&Text',
    tabs: '.stui-vodlist__head h3',
    lists: '.stui-content__playlist:eq(#id) li',
  },
  搜索: '*',
  filter: {
    "1":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"恐怖","v":"恐怖"},{"n":"动作","v":"动作"},{"n":"科幻","v":"科幻"},{"n":"剧情","v":"剧情"},{"n":"战争","v":"战争"},{"n":"警匪","v":"警匪"},{"n":"犯罪","v":"犯罪"},{"n":"动画","v":"动画"},{"n":"奇幻","v":"奇幻"},{"n":"武侠","v":"武侠"},{"n":"冒险","v":"冒险"},{"n":"枪战","v":"枪战"},{"n":"悬疑","v":"悬疑"},{"n":"惊悚","v":"惊悚"},{"n":"经典","v":"经典"},{"n":"青春","v":"青春"},{"n":"伦理","v":"伦理"},{"n":"文艺","v":"文艺"},{"n":"微电影","v":"微电影"},{"n":"古装","v":"古装"},{"n":"历史","v":"历史"},{"n":"运动","v":"运动"},{"n":"农村","v":"农村"},{"n":"儿童","v":"儿童"},{"n":"网络电影","v":"网络电影"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"大陆","v":"大陆"},{"n":"香港","v":"香港"},{"n":"台湾","v":"台湾"},{"n":"美国","v":"美国"},{"n":"法国","v":"法国"},{"n":"英国","v":"英国"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"德国","v":"德国"},{"n":"泰国","v":"泰国"},{"n":"印度","v":"印度"},{"n":"意大利","v":"意大利"},{"n":"西班牙","v":"西班牙"},{"n":"加拿大","v":"加拿大"},{"n":"其他","v":"其他"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"2025"},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"time"},{"n":"人气","v":"hits"},{"n":"评分","v":"score"}]}],
    "2":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""},{"n":"古装","v":"古装"},{"n":"战争","v":"战争"},{"n":"青春偶像","v":"青春偶像"},{"n":"喜剧","v":"喜剧"},{"n":"家庭","v":"家庭"},{"n":"犯罪","v":"犯罪"},{"n":"动作","v":"动作"},{"n":"奇幻","v":"奇幻"},{"n":"剧情","v":"剧情"},{"n":"历史","v":"历史"},{"n":"经典","v":"经典"},{"n":"乡村","v":"乡村"},{"n":"情景","v":"情景"},{"n":"商战","v":"商战"},{"n":"网剧","v":"网剧"},{"n":"其他","v":"其他"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"内地","v":"内地"},{"n":"香港","v":"香港"},{"n":"台湾","v":"台湾"},{"n":"美国","v":"美国"},{"n":"法国","v":"法国"},{"n":"英国","v":"英国"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"德国","v":"德国"},{"n":"泰国","v":"泰国"},{"n":"印度","v":"印度"},{"n":"意大利","v":"意大利"},{"n":"西班牙","v":"西班牙"},{"n":"加拿大","v":"加拿大"},{"n":"其他","v":"其他"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"2025"},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"time"},{"n":"人气","v":"hits"},{"n":"评分","v":"score"}]}],
    "3":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""},{"n":"选秀","v":"选秀"},{"n":"情感","v":"情感"},{"n":"访谈","v":"访谈"},{"n":"播报","v":"播报"},{"n":"旅游","v":"旅游"},{"n":"音乐","v":"音乐"},{"n":"美食","v":"美食"},{"n":"纪实","v":"纪实"},{"n":"曲艺","v":"曲艺"},{"n":"生活","v":"生活"},{"n":"游戏互动","v":"游戏互动"},{"n":"财经","v":"财经"},{"n":"求职","v":"求职"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"内地","v":"内地"},{"n":"港台","v":"港台"},{"n":"欧美","v":"欧美"},{"n":"日韩","v":"日韩"},{"n":"其他","v":"其他"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"2025"},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"time"},{"n":"人气","v":"hits"},{"n":"评分","v":"score"}]}],
    "4":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""},{"n":"情感","v":"情感"},{"n":"科幻","v":"科幻"},{"n":"热血","v":"热血"},{"n":"推理","v":"推理"},{"n":"搞笑","v":"搞笑"},{"n":"冒险","v":"冒险"},{"n":"萝莉","v":"萝莉"},{"n":"校园","v":"校园"},{"n":"动作","v":"动作"},{"n":"机战","v":"机战"},{"n":"运动","v":"运动"},{"n":"战争","v":"战争"},{"n":"少年","v":"少年"},{"n":"少女","v":"少女"},{"n":"社会","v":"社会"},{"n":"原创","v":"原创"},{"n":"亲子","v":"亲子"},{"n":"益智","v":"益智"},{"n":"励志","v":"励志"},{"n":"其他","v":"其他"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"国产","v":"国产"},{"n":"欧美","v":"欧美"},{"n":"日本","v":"日本"},{"n":"其他","v":"其他"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"2025"},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"time"},{"n":"人气","v":"hits"},{"n":"评分","v":"score"}]}],
    }
}
