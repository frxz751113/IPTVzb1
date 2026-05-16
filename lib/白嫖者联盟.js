//一级筛选有人机验证，需预处理，放弃
var rule = {
    title: '白嫖者联盟',
    模板: '首图',
    host: 'https://www.qyzf88.com',
    //url: '/qyvodshow/fyclass--------fypage---.html',
    url: '/qyvodtype/fyclass-fypage.html',
    searchUrl: '/qyvodsearch/**----------fypage---.html',
    headers: {//网站的请求头,完整支持所有的,常带ua和cookies
                'User-Agent': 'MOBILE_UA',
                'Referer': 'https://www.qyzf88.com', 
                'Cookie': ''
            },
    searchable: 2,
    filterable: 0,
    class_parse: '.myui-header__menu li:gt(0):lt(5);a&&Text;a&&href;/(\\d+).html',
    预处理:'',
}