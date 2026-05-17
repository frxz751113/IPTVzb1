Object.assign(muban.mxpro.二级,{
    tabs: '.tab-item',
});
var rule = {
  模板:'mxpro',
  title: '天天影院',
  host: 'https://ttyy8.me',
  searchUrl: '/vodsearch/**----------fypage---.html',
  cate_exclude:'今日更新|发布页|热搜榜',
  // url:'/vodshow/fyclass--------fypage---.html',//不带筛选写法	
  url: '/vodshow/fyclass-fyfilter.html',//带筛选写法
  filter:'H4sIAAAAAAAAA+2a3U4bRxTHX8XydS5mISRpX6XKRVQhJWqbSk1aqYqQAH9gG2IbBHZcGzCED0OwscElsI7tl9mZXb9Fxztjn3MmkZZNQbnI3vGbc3Y+/rMz+2fGb2JxK/5j7KfYm1j8l/m/5Z9xnj0WiVT8QSz+8tlv87Tkr2e//jk/yX/px1KNUaLhx8YYjy08gFipJh+dxjTiDDfTmdSMEGeIpaJYLE0zNJJWcg2nX4NWFJJWjtf5TQ9aUUjqgBEiJP3IvHPsLPRDIc7wmkd87XSaoZH0I3fu9iFDozEWd7OHxzJGknG4gseikfS0eeQM6tBThaSO9MaocgJ1KCR17JzKEUIdCsPNi1g+c0vrkKGQZCRyYvkfyFBIFOsVeOoaFFOIM0bbG+Ld4TRDI2mltOJlbWhFIdFj0HI3/+X9DkgyLSF5hQPvPXpLFJKMfJoXLiBDIXlLhkU5q/CWKKSzUxPb62h2fCQZyaH7AcaskejWX3d7NWNQpDC2EHuqn5is+1qbr9lk3U9LQq77g+NRJQ39U0hm7agirs9h1hRSrdviZoC09pGMcZDn1T6MTiGZ+bNjWQozr5BklA9F7QwyFJKe7p7gVjSSOi7bOEMjGUvqyunBWtH4+Qx4502vsYhnAEpCzkC1Lx+FFhWS93C1gzM0En0vDnCGRqJNuc/flnESlBgakiSFxjzgDI1U5S2SoZCu4o9kzAqNeeCtBJ6HMX5hJdx0nV6frIRpSbh5mGEzD6cRH4zoLI7OmtEZHJ0xoxaOWmaU4SgzotYPKCrBiD7B0Sdm9DGOPjajj3D0kRmdw9E5M4q1skytLKyVZWplYa0sUysLa2WZWllYK8vUimGtmKkVw1oxUyuGtWKmVgxrxUytGNaKmVoxrBUztWJYK2ZqxbBWzNSKYa2YqRXDWjH2hdUj8hvcLuDVAyWfrx5RvhqVuyhjXPj6hXwQt+vYtmhvGlnPX7x+Rfe08yTPpI2sVz///se87mbsqSydid+b3w30B8EuMtjP8KUrnoDxaQznu3nrittor1QY2qsG+O5grxrsu4MdVbBHdG72sKPSSJ1oSlTAj2gk/dhKY0es0fBcWHWNX+MD7tCJpVPyUeQlfQznb+7CqwX7rFu4uUCfJU0MztBI/xdo81ydb++hfwcmJZFju1vHFrmtyG1Fbut7d1uz8ftyW6PFrHu8CHuUQvOrntwlX3WJZAytodfOwJ6qkNSx0RQ58GMa6U6YEtfgPzTS3fTSuSmi3dRH4+s3eg891Ugy7FPe2oEMhaQf1QtyzqWQ1LG5K7roHFQhqeP6WmQKjr2Bz6hIIVGvuy/dFqinkNTXWfaW1qAmhd/W8Uj3Ih0KGp2PxrdNfvHwt22MtzlZivxB5A8ifxD5g8gf3NYfPLw3fxB86+cmmt4eOAiNZBfLN9wi3GRoJBnFHfcM3XIppF+koNs2r7jt5eFUSCNppb7Hq2g3VRjuNEbUbHKnp5D0I/BuKvj8irelzF3oh0Iz4/CSZEgk83IwcD7BvaBGeiq0yzNVqEMhfUcveBM8l0bSSjUnKuCXNFJNO3xYRpr6GM5hfoMzn2rfsdHpn8JwpzHBN2fRCUnkgCIHFDmgyAH9Xwc0F7+3+6jAu5Nb3L8E3/LkGm72BGeM0Ty76G/BrquQ6Pmp7rXgf3KNpuKlFfQ99zHc6Yb8omI3p5Hs2aUVvoZ+1aQw3GkPT1cdexX5PR/Je7Fy6iav4DulMJwDEvl9t7uPnKmPpv9tHhH/K/E2p07fwS+DLrfoXdLWV9wl3cFvh/jgI87QSHsa+Ouit21uwzxrJHUkC1JpnkFHWtMSMubDoVtoutkKDHtaQld8XawOZQVo0U9K6GqKbtsiLzmByEtGXjLykvfoJWML/wFf5huqzi8AAA==',
  filter_url:'{{fl.地区}}-{{fl.排序}}-{{fl.剧情}}-{{fl.语言}}----fypage---{{fl.年份}}',
  filter_def:{
    1: {cateId: '1'},
    2: {cateId: '2'},
    3: {cateId: '3'},
    4: {cateId: '4'},
    5: {cateId: '5'}
  },
  filterable:1,
}