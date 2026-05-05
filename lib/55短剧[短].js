var rule = {
  类型: '影视',//影视|听书|漫画|小说
  title: '55短剧[短]',
  host: 'https://www.duanju55.com',
  url: '/index.php/vod/show/fyclass/page/fypage.html',
  searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
  searchable: 2,
  quickSearch: 0,
  filterable: 1,
  //filter: { "1": [{ "key": "剧情", "name": "剧情", "value": [{ "n": "全部", "v": "" }, { "n": "都市", "v": "/class/都市" }, { "n": "赘婿", "v": "/class/赘婿" }, { "n": "战神", "v": "/class/战神" }, { "n": "古代言情", "v": "/class/古代言情" }, { "n": "现代言情", "v": "/class/现代言情" }, { "n": "历史", "v": "/class/历史" }, { "n": "脑洞", "v": "/class/脑洞" }, { "n": "玄幻", "v": "/class/玄幻" }, { "n": "电视节目", "v": "/class/电视节目" }, { "n": "搞笑", "v": "/class/搞笑" }, { "n": "网剧", "v": "/class/网剧" }, { "n": "喜剧", "v": "/class/喜剧" }, { "n": "萌宝", "v": "/class/萌宝" }, { "n": "神豪", "v": "/class/神豪" }, { "n": "致富", "v": "/class/致富" }, { "n": "奇幻脑洞", "v": "/class/奇幻脑洞" }, { "n": "超能", "v": "/class/超能" }, { "n": "强者回归", "v": "/class/强者回归" }, { "n": "甜宠", "v": "/class/甜宠" }, { "n": "励志", "v": "/class/励志" }, { "n": "豪门恩怨", "v": "/class/豪门恩怨" }, { "n": "复仇", "v": "/class/复仇" }, { "n": "长生", "v": "/class/长生" }, { "n": "神医", "v": "/class/神医" }, { "n": "马甲", "v": "/class/马甲" }, { "n": "亲情", "v": "/class/亲情" }, { "n": "小人物", "v": "/class/小人物" }, { "n": "奇幻", "v": "/class/奇幻" }, { "n": "无敌", "v": "/class/无敌" }, { "n": "现实", "v": "/class/现实" }, { "n": "重生", "v": "/class/重生" }, { "n": "闪婚", "v": "/class/闪婚" }, { "n": "职场商战", "v": "/class/职场商战" }, { "n": "穿越", "v": "/class/穿越" }, { "n": "年代", "v": "/class/年代" }, { "n": "权谋", "v": "/class/权谋" }, { "n": "高手下山", "v": "/class/高手下山" }, { "n": "悬疑", "v": "/class/悬疑" }, { "n": "家国情仇", "v": "/class/家国情仇" }, { "n": "虐恋", "v": "/class/虐恋" }, { "n": "古装", "v": "/class/古装" }, { "n": "时空之旅", "v": "/class/时空之旅" }, { "n": "玄幻仙侠", "v": "/class/玄幻仙侠" }, { "n": "欢喜冤家", "v": "/class/欢喜冤家" }, { "n": "传承觉醒", "v": "/class/传承觉醒" }, { "n": "情感", "v": "/class/情感" }, { "n": "逆袭", "v": "/class/逆袭" }, { "n": "家庭", "v": "/class/家庭" }, { "n": "女频恋爱", "v": "/class/女频恋爱" }, { "n": "反转爽剧", "v": "/class/反转爽剧" }, { "n": "古装仙侠", "v": "/class/古装仙侠" }, { "n": "年代穿越", "v": "/class/年代穿越" }, { "n": "脑洞悬疑", "v": "/class/脑洞悬疑" }, { "n": "现代都市", "v": "/class/现代都市" }] }] },
  //filter_url: '{{fl.剧情}}/page/fypage',
  headers: {
    'User-Agent': 'PC_UA',
  },
  timeout: 5000,
  class_name: '全部&都市&赘婿&战神&古代&言情&历史&脑洞&玄幻&搞笑&喜剧&萌宝&神豪&奇幻&强者&回归&甜宠&豪门&恩怨&复仇&神医&马甲&亲情&人物&无敌&重生&闪婚&职场&商战&穿越&年代&权谋&高手&下山&悬疑&家国&虐恋&古装&时空&之旅&仙侠&欢喜&冤家&传承&觉醒&情感&逆袭&家庭',  
  class_url: 'id/1&class/都市/id/1&class/赘婿/id/1&class/战神/id/1&class/古代/id/1&class/言情/id/1&class/历史/id/1&class/脑洞/id/1&class/玄幻/id/1&class/搞笑/id/1&class/喜剧/id/1&class/萌宝/id/1&class/神豪/id/1&class/奇幻/id/1&class/强者/id/1&class/回归/id/1&class/甜宠/id/1&class/豪门/id/1&class/恩怨/id/1&class/复仇/id/1&class/神医/id/1&class/马甲/id/1&class/亲情/id/1&class/人物/id/1&class/无敌/id/1&class/重生/id/1&class/闪婚/id/1&class/职场/id/1&class/商战/id/1&class/穿越/id/1&class/年代/id/1&class/权谋/id/1&class/高手/id/1&class/下山/id/1&class/悬疑/id/1&class/家国/id/1&class/虐恋/id/1&class/古装/id/1&class/时空/id/1&class/之旅/id/1&class/仙侠/id/1&class/欢喜/id/1&class/冤家/id/1&class/传承/id/1&class/觉醒/id/1&class/情感/id/1&class/逆袭/id/1&class/家庭',
  play_parse: true,
  lazy: $js.toString(() => {
    input = { parse: 1, url: input, js: '' };
  }),
  tab_exclude: '猜你喜欢',
  double: false,
  推荐: '.SecondList_secondListItem;.SecondList_bookName&&Text;.image_imageDark&&src;.SecondList_totalChapterNum&&Text;.SecondList_bookName&&href',
  一级: '.BrowseList_itemBox;.BrowseList_bookName span&&Text;.image_imageItem&&src;.BrowseList_totalChapterNum&&Text;.BrowseList_bookName&&href',
  二级: {
    title: 'h1&&Text;.breadcrumb_crumbItem:eq(1)&&Text',
    img: '.DramaDetail_bookCover&&src',
    desc: '.DramaDetail_tagsBox&&Text',
    content: '.DramaDetail_tagsBox&&Text',
    tabs: '.pcDrama_titleText',
    lists: '.pcDrama_catalog:eq(#id)&&a',
    tab_text: 'body&&Text',
    list_text: 'body&&Text',
    list_url: 'a&&href',
  },
  搜索: '.TagBookList_tagItem;.TagBookList_bookName&&Text;.image_imageItem&&src;.TagBookList_totalChapterNum&&Text;.TagBookList_bookName&&href',
}