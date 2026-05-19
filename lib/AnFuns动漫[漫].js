var rule = {
  模板:'海螺3',
  title: 'AnFuns动漫[漫]',
  host: 'https://www.anfuns.org',
  searchUrl: '/search/page/fypage/wd/**.html',
  url: '/type/fyclass-fypage.html',
  class_parse: 'body&&.hl-nav li:gt(1);a&&Text;a&&href;.*/(.*?).html',
}