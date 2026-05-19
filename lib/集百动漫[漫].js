var rule = {
    类型: '影视',
    title: '集百动漫[漫]',
    host: 'http://www.jibai5.com',
    url: '/bm/fyclass/fypage.html',
    searchUrl: '/vodsearch/**----------fypage---.html',
    homeUrl: '/',
    headers: {'User-Agent': 'UC_UA'},
    searchable: 1, quickSearch: 0, filterable: 0, double: true, play_parse: true, limit: 6,
    class_name: '3D动漫&动漫&沙雕剧场',
    class_url: '20&21&22',
    lazy:`js:
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
    推荐:'*',
    一级:'.boxlist li;.list-name&&Text;.lazy&&src;.duration&&Text;.list-link&&href',
    二级: {
        title: 'h2&&Text;dl:eq(7)&&Text',
        img: '.lazy&&src',
        desc: 'dd:eq(1)&&Text;dd:eq(3)&&Text;dl:eq(5)&&Text;dd:eq(0)&&Text;dd:eq(2)&&Text',
        content: 'dd:eq(7)&&Text',
        tabs:'.panel-default&&.panel-heading',
        lists: '.dslist-group:eq(#id)&&li',
        tab_text: 'body&&Text',
        list_text: 'a&&Text',
        list_url: 'a&&href'
            },
    搜索:'*',
}