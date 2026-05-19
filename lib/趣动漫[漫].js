var rule = {
  title: '趣动漫[漫]',
  desc: '不告诉你',
  host: 'https://www.qdm8.com',
  url: '/type/fyclass-fypage.html',
  searchUrl: '/search/**----------fypage---.html',
  searchable: 2, quickSearch: 0, filterable: 0,
  class_name: '漫电影&国漫&欧美漫&日漫',
  class_url: 'dmdianying&guoman&oman&riman',
  play_parse: true, limit: 6, double: true,
  lazy: `js: input = { jx: 0, parse: 1, url: input }`,
  推荐: '*',
  一级: '.myui-vodlist li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href',
  二级: {
    title: '.myui-content__detail&&h1&&Text',
    img: '.lazyload&&data-original',
    desc: '.myui-content__detail&&p:eq(2)&&Text;.myui-content__detail&&a:eq(2)&&Text;.myui-content__detail&&a:eq(1)&&Text;;',
    content: '.myui-content__detail&&p:eq(5)&&Text',
    tabs: '.nav.nav-tabs&&li',
    lists: '.myui-content__list:eq(#id)&&li a'
  },
  搜索: '.myui-vodlist__media li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href;.detail&&p:eq(2)&&Text',
}