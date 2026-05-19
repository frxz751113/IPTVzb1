var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'搜漫网[漫]',
  host:'https://www.socomic.com',
  //url:'/donghua/fyclass/',//不带筛选写法
  searchUrl:'/search/',
  url: '/fyclass/fyfilter-fypage.html',//带筛选写法
  filter:'H4sIAAAAAAAAA+2aW1MaSRTHv8oUz6YKMFUB38z9fo+5bOVBF6MhqJvFjWIqVUaMAhpA14CsaHQTFDey4GVTcQz4Zeie4VtkYJNz+rQWKTZatVb1G/P7d89095nLz3Gea7YBh61F+0l7rtmedAasnzZjfYctTNiaNFtve09nlfDJMMJn7b7fOr916a3G7FW2EszWsuqmTXvRBBkfWTMSU5ANBkhayc3wzTeQ9jwiqfFhgUeGIfV6aRpa58FXkLY/pWkwZy5h318HScoy42x7B9Kn3bTvypSYPqEpjy8YazijLrpnvviZJ5KYeuhxI+tsF1PfEO0bzRrxMUj7fbRvYYplNiH199IxZxasxcS0h+45MW6GdUgHAtJ88yyEx/XSKrCx6UpqFWskz3eJzeWE+jrorlMlFg9B3EGX0hwuGqUopB5p0Gmdh2ZxWHSxWDzK/v4AaXcX7buxw0fxuEPSaffnKJuKQBqgfa+1tRph7Nv3rL2D5OXi7+bIBpapum/t4dcWX68hli6wSV26hhA2dg2x9yuVFNbHQ8+LynKKf8pjBehkWKzAt0s42AFanlKUzRWxtrRv5e2qmMpLnMzw9BpeYXSR+GZB7Nsv9U0UWGSRzS/hsL2/0GOvrvH5jJnZLet/4Ph80v2DvS4wfRkLSa82c2JdHINUZuvGI6aPpHWLLPKJXWvl8fzr9exX6O2t8k5RLjTAxgrttDuPQ1LbkNJmMW2WU6eYOuXUIaYOObWLqV1KHW4htTak1CWmLjk9IaYnpNTuPuZwu3H31Y0mqx0dgdteW9F3YjN7U62j2My1t5mr2sxFm/G5LZ5cFRrZa43s+1U3l+T513J1ATZW3VbArYSfBH6S8FPATxF+Gvhpws8AP0P4WeBnCT8H/Bzh54GfJ/wC8AuEXwR+kfBLwC8Rfhn4ZcKvAL9C+FXgV+l9Gvg1wq8Dv074DeA3CL8J/Cbht4DfIvw28NuE3wF+h/A24G2E3wV+l/B7wO8Rfh/4fcIfAH9AuP0YXlfV33tPbx6dZnpMOr0R7j29q3HyYyW5hdrl8fQ/tvqSC2wyXNZ1XkAd6X7c75ebmPlR0Tq6+nzf7q/aQwsOOG2HqaWytuxRrdFdlCk6PUkt/ZIQycIrCdH/0i0r89N8NoM+/PPBueXMW76F8/XT+bLoGIuhSvnoSVLfPP+VOCM8LjzgqUOU9Q2Wi+Os6IoYcxGewnEHJL3c/szfpDD9/t8eSgGVAioFVAqoFFApoFLAA1HAZtshKmB9u/iOO9R9u1j/nedRNMD9HE/5jvId5TvKd5TvKN9RvnMQvtNxqL7T4GurI+8sR+utlbIpZVPKppRNKZtSNqVs6kBs6lC/a6v/9ZmZHRbTAE1Z7L35DtMu6jyVYJF9GsGHtWQXLz+yYAzSvkYsjkWyxgxajUeymkSahfFpNUj/48VfxvlwAg2wQ95zuZjGPUtvy+rbY265XFpEE5NmFJot62FIh6Q9R/JG8S98BEv2GIzwEXz4e/3SqP77V2/1PyCr/3WhtcjiueGVvluc+cdcGRML4fF7lR+2KD9Uftii/FD5ofLDFuWHP+yH2osvoDg66/owAAA=',
  filter_url:'{{fl.类型}}_{{fl.地区}}_{{fl.年份}}_{{fl.字母}}_{{fl.排序}}',
  //https://www.socomic.com/donghua/w1/xy_dl_2024_A_hits-2.html
  filter_def:{
    w1: {cateId: 'w1'},
    w2: {cateId: 'w2'},
    w3: {cateId: 'w3'},
    b1: {cateId: 'b1'},
    b3: {cateId: 'b3'}
  },
  searchable:0,
  quickSearch:0,
  filterable:0,
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.nav li;a&&Text;a&&href;.*/(.*?)/',
  cate_exclude:'排行榜|最新',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'li.col-md-2;li;*;*;.note&&Text;.loading&&href',
  一级:'#content li;h5&&Text;.video-pic&&data-original;.note&&Text;.loading&&href',
  二级:{
    title:'.video-pic&&title;em&&Text',
    img:'.video-pic&&style',
    desc:'.col-md-6:eq(6)&&Text;.col-xs-12:eq(2)&&Text;.col-md-6:eq(2)&&Text;.text a&&Text;.col-md-6 a&&Text',
    content:'.details-content-default&&Text',
    tabs:'.dropdown-menu li',
    lists:'.playlist:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'*',
}