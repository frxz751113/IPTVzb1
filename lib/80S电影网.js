var rule = {
  title:'80s电影网',
  host:'https://www.jlfjz.com/',
  url:'list/fyfilter_____fypage.html',//list/guocanju______3.html
  searchUrl:'/search/?wd;post&wd=**',
  searchable:2,
  quickSearch:0,
  filterable:1,
  filter_url:'{{fl.tag}}_{{fl.area}}',
  filter:{
       "dianying":[{"key":"tag","name":"电影","value":[{"n":"动作片","v":"dongzuopian"},{"n":"喜剧片","v":"xijupian"},{"n":"爱情片","v":"aiqingpian"},{"n":"科幻片","v":"kehuanpian"},{"n":"恐怖片","v":"kongbupian"},{"n":"剧情片","v":"juqingpian"},{"n":"战争片","v":"zhanzhengpian"},{"n":"纪录片","v":"jilupian"},{"n":"动画片","v":"donghuapian"}]}]
        ,"dianshiju":[{"key":"tag","name":"电视剧","value":[{"n":"国产剧","v":"guocanju"},{"n":"香港剧","v":"xianggangju"},{"n":"台湾剧","v":"taiwanju"},{"n":"韩国剧","v":"hanguoju"},{"n":"印泰剧","v":"taiguoju"},{"n":"欧美剧","v":"oumeiju"},{"n":"海外剧","v":"haiwaiju"},{"n":"日本剧","v":"ribenju"}]}]
       , "dongman":[{"key":"area","name":"动漫","value":[{"n":"冒险","v":"maoxian"},{"n":"热血","v":"rexue"},{"n":"搞笑","v":"gaoxiao"},{"n":"少女","v":"shaonv"},{"n":"恋爱","v":"lianai"},{"n":"魔幻","v":"mohuan"},{"n":"推理","v":"tuili"},{"n":"神魔","v":"shenmo"},{"n":"竞技","v":"jingji"},{"n":"游戏","v":"youxi"},{"n":"益智","v":"yizhi"},{"n":"机战","v":"jizhan"},{"n":"宠物","v":"chongwu"},{"n":"格斗","v":"gedou"}]}]
        ,"zongyi":[{"key":"area","name":"综艺","value":[{"n":"真人秀","v":"zhenrenxiu"},{"n":"脱口秀","v":"tuokouxiu"},{"n":"选秀","v":"xuanxiu"},{"n":"情感","v":"qinggan"},{"n":"访谈","v":"fangtan"},{"n":"美食","v":"meishi"},{"n":"旅游","v":"lvyou"},{"n":"财经","v":"caijing"},{"n":"军事","v":"junshi"},{"n":"职场","v":"zhichang"},{"n":"音乐","v":"yinle"},{"n":"时尚","v":"shishang"},{"n":"娱乐","v":"yule"},{"n":"体育","v":"tiyu"},{"n":"生活","v":"shenghuo"},{"n":"社会","v":"shehui"}]}]
        ,"duanju":[{"key":"area","name":"短剧","value":[{"n":"爱情","v":"aiqing"},{"n":"励志","v":"lizhi"},{"n":"明星","v":"mingxing"},{"n":"生活","v":"shenghuo"},{"n":"青春","v":"qingchun"},{"n":"搞笑","v":"gaoxiao"},{"n":"恐怖","v":"kongbu"},{"n":"职场","v":"zhichang"},{"n":"校园","v":"xiaoyuan"},{"n":"悬疑","v":"xuanyi"},{"n":"罪案","v":"zuian"},{"n":"文艺","v":"wenyi"},{"n":"魔幻","v":"mohuan"},{"n":"冒险","v":"maoxian"}]}]
  },
  filter_def:{
		dianshiju:{tag:'dianshiju'},
		dianying:{tag:'dianying'},
        dongman:{tag:'dongman'},
        zongyi:{tag:'zongyi'},
        duanju:{tag:'duanju'},
	},
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  class_name:'电视剧&电影&动漫&综艺&短剧',
  class_url:'dianshiju&dianying&dongman&zongyi&duanju',
  timeout:5000,
  //class_parse:'ul.type-slide li;a&&Text;a&&href;.*/(.*?)\.html',
  cate_exclude: '留言',
  tab_exclude:'更多|不能播放|来源',
  drpy:'热播',
  play_parse:true,
  lazy: $js.toString(() => {
        let init_js = `Object.defineProperties(navigator, {platform: {get: () => 'iPhone'}});`;
        input = {
            parse: 1,
            url: input,
            js: '',
            parse_extra: '&init_script=' + encodeURIComponent(base64Encode(init_js)),
        }
    }),
  double:true,
  推荐:'.stui-vodlist;li;a&&title;a&&data-original;.text-right&&Text;a&&href;.stui-vodlist__detail&&.text-muted&&Text',
  一级:'.box-video-list&&li;a&&title;a&&data-original;.note&&Text;a&&href;.stui-vodlist__detail&&.text-muted&&Text',
  二级:{
    title:'h1&&Text;.info&&li:eq(2)&&Text',
    img:'.details-pic&&a&&style',
    desc:';.details-info&&.hidden-sm&&Text;p:eq(3)&&a:eq(1)&&Text;.info&&li:eq(3)&&Text;.info&&li:eq(5)&&Text',
    content:'.info .details-content-all&&Text',
    tabs:'.nav.nav-tabs.hidden-xs&&li',
    //drpy:'.nav.nav-tabs.hidden-xs&&li',
    lists:'.playlist&&a ',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href'
  },
  搜索:'.details-info-min;a&&title;a&&data-original;span:eq(1)&&Text;a&&href',
}