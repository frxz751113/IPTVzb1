var rule = {
title: '小米盘[盘]',
类型: '影视',
desc: '不告诉你',
//host: 'http://www.mucpan.cc',
host:'http://milvdou.fun',
hostJs: '',
headers: {'User-Agent': 'MOBILE_UA'},
编码: 'utf-8',
timeout: 5000,
homeUrl: '/',
url: '/index.php/vod/show/id/fyfilter.html',
filter_url: '{{fl.cateId}}{{fl.area}}{{fl.by}}{{fl.class}}{{fl.lang}}{{fl.letter}}/page/fypage{{fl.year}}',
detailUrl: '',
searchUrl: '/index.php/vod/search/page/fypage/wd/**.html',
searchable: 1, 
quickSearch: 1, 
filterable: 1, 
class_name: '电影&剧集&动漫&综艺',
class_url: '1&2&3&4',
filter_def: {1:{cateId:'1'},2: {cateId: '2'},3: {cateId: '3'},4: {cateId: '4'}
},
play_parse: true,
lazy: `js:
let type = '';
if (/quark/.test(input)) {
    type = 'quark'
} else if (/uc/.test(input)) {
    type = 'uc'
} else if (/aliyundrive|alipan/.test(input)) {
    type = 'ali'
};let confirm= '';
input = getProxyUrl().replace('js',type)+'&type=push'+confirm+'&url='+encodeURIComponent(input)
`,
推荐: '*',
一级: '.module-item;img&&alt;img&&data-src;.module-item-text&&Text;a:eq(0)&&href',
二级: {
title: 'h1&&Text;.video-info-items:eq(3)&&Text',
img: '.video-cover&&img&&data-src',
//主要描述;年份;地区;演员;导演
desc: '.video-info-items:eq(3)&&Text;.video-info-items:eq(2)&&Text;.tag-link:eq(-1)&&Text;.video-info-actor:eq(1)&&Text;.video-info-actor:eq(0)&&Text',
content: '.sqjj_a--span&&Text',
tabs: '.downtab-item',
tab_text: 'body--small&&Text',
lists: '.module-row-one:eq(#id)&&a.btn-down',
list_text: 'a&&title',
list_url: 'a&&href'
},
搜索: '.module-search-item;*;*;.video-serial&&Text;.video-serial&&href',
filter:'H4sIAAAAAAAAA+2XW08TQRTH3/sx9hlTtigib4o3vIt4QeND1UaNiAlUE0JIhNJyp0CwtVq8RKCglBYvKNsUvkxnt/0WzjKzZ2bOElnEBx/2sf/fv2dmzszOnNMX0HSt+U6gT3sS6dWatfud4Z4erU7rCj+N0J9kNGfG4vT3i3Dncyrc6dO6bDm+XIst2zL9ofXXcTWVpX6uBnciBbnmWKyRdR5PWLjmWMyBafNlSrVwDQYaW66Us2ggpsFAuRmyWUIDMQ2iwNqkKEyDuYy8rhijaC5McyzV/BKZ+KxauAZzGStYZWThmrQia67kWpGtgWVx2LUirsF080uVrQ9oukyDKInZWmYFRWEaRHn3ma4RRWEaWAZXrdQMsjANLLExc/ANsjAN8lJKkvgvlBemOZba/Kz5elG1cA0GSg1XRw00ENNg0Vtr1twPUl5H6wYZjMmF6id8JJgGlqkESX5FFqbBkdiepnuHjgTTxDZkzfkZvA07GliGtq0vaOlcgwSWZ6xSdrelKaT/bn8dfODh7khY+r6zRTJheP2+F3K1TMIZyA4U5BJs11LG/FVQHFwSGS6am1tqDCbBoramyNuy4uAS7Pi3V9jBJdiB8XXs4BLESC+a2VU1BpNgLe9XcAwuiWP1Ezu4JGZadM+0qMSYLBJjSY3BJIgxlKRZJiMrahhQYc2L21Yyb41m1GWDKq6aD+b4Nv2zOiio4ItvVEop1cQk5Tx1hrseivNULeSryy+9nqe3Zep3RrADBbkk7SN2cAlOy9cF7OAS7GO6TCbT2CRUab9dJiZJZwY7uCSdTJeDSdKZca2ZSVLeyVpMdTBJyXtvJNwt8m6mN2rp7x7zHqoPHXbi22GCO4JEGzBtkGkI05BMdUx1mdZjWi9R/RiiVJBoE6ZNMj2K6VGZNmLaKNMjmB6RKc6VLudKx7nS5VzpOFe6nCsd50qXc6XjXFFB/fIi0WhEOgMknzYLkx7PwHE4YDtRgseBnEDkBJAWRFqAnETkJJBTiJwCchqR00DOIHIGyFlEzgJpRaQVyDlEzgE5j8h5IBcQuQDkIiIXgVxC5BKQy4hcBnIFkStAriJyFUgbIm1AriFyDUg7Iu1AriNyHcgNRG4AuYnITSC3ELkFpAORDiC3EbkNpP7QMcRsRfkG7vVKd+DULDGSrvMvrkY70L3eYPQxtTtjVAzDLM5J9NHjaI94fwpDZCQh0Z77z7oj9hQCd+sCWkjpnMLRSOsDMR1rvUTejf/5cxS3AX34KkZOtE/SNWKu5uwCSCBxO9Hnx65JBBJXEy26aGEloUY1cwdq9PYukz10TqyOJwMbJJbcrcLnZB/dJVnbIEYeWZi2v15sr+7SQy/mobv00Ep4aJEqmx9drQTXRC8WNzMFtBlMg7m8SriaPq5J3YZrA7i2e83Io+xSNB6kCUnEqV8tS5nkvXD/F23K3g2El0Zmr/bAQyOTKtLancx/VMOA6pfzwrTfct4vxf1S3C/F/VLcL8X/+1K84cClOK7Fud4gridWbTu6uNRYge7oTf7j4D8O/uPgPw7+4/C/PA6H5cdh/xeyeq36V7J/JftXsn8l+1fyX1/Jgf7fWYJTA3ckAAA=',
}