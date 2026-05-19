var rule = {
模板:'首图2',
  类型:'影视',//影视|听书|漫画|小说
  title:'樱花动漫2[漫]',
  host:'https://m.91s.cc',
  //url:'/vodtype/fyclass-fypage.html',
  searchUrl:'/vodsearch/**----------2---.html',
  searchable:2,
  quickSearch:0,
  filterable:0,
  cate_exclude:'新动漫网',
  url: '/vodshow/fyclass-fyfilter.html',//带筛选写法
  filter:'H4sIAAAAAAAAA+2VyUojURSGX+VSaxe5Feed8zzPiguRgKJtQzuAiCCoTYtDQ9NNLVy4UYgLjRM2HYlPY5XJW3QlKf865+jGdc4u5/v+m1ROXfi3jGOdRjNjtoyzlNoMPzr+v4eXp5xTZZyVuS+pIgmODmK4Mbe8nno7slI6sJ8u7KZLrjg6ZrsKzk241TClQdgktUlpXWpdaS21VtoEtQlhbQOx4SBsPbX10tZRWydtLbW10tZQWyMt3ZWVu7J0V1buytJdWbkrS3dl5a4s3ZUt7srMRom3S3HlBZljeSkAP3cpmoCbGG8Gb2a8BbyF8VbwVsbbwNsYbwdvZ7wDvIPxTvBOxrvAuxjvBu9mvAe8h/Fe8F7G+8D7GO8H72d8AHyA8UHwQcaHwIcYHwYfZnwEfITxUfBRxsfAxxgfBx9nfAJ8gvFJ8EnGp8CnGJ8Gn/7gCuczV/n0jrjCMfzcFfZPc+FRuGikicC7oIlopInXu3OaiEaayB/e0kQ00kTBy/nHHg3FhOXOLlmoPLLnvf/Dnrc8sv/8/Jf95/LIEvuP/vVunCiP719FcPLLz/4UryKG719F4D0WvAd88dpieIr+8Es2G9z8hl9YXFvli8zs+T++w6/Of/2Wip7LzIbU1Q7UDtQO1A7UDtQOrNAOTGoHagdqB2oHagdqB1ZoB1ZrB2oHagdqB2oHagdWYgea7f90v01tEhwAAA==',
  filter_url:'-{{fl.排序}}--{{fl.语言}}-{{fl.语言}}---fypage---{{fl.年份}}',
  //实例 https://m.91s.cc/vodshow/2--hits--国语-A---2---2024.html
  filter_def:{ 
    1: {cateId: '1'}, 
    2: {cateId: '2'}, 
    3: {cateId: '3'},
    4: {cateId: '4'}
  },
  }