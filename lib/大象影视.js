var rule = {
  类型:'影视',//影视|听书|漫画|小说
  模板:'海螺3',
  title:'大象影视',
  host:'https://slzc.cn',
  url:'/vodshow/fyfilter.html',
  searchUrl:'/vodsearch/**----------fypage---.html',
  searchable:2,
  quickSearch:0,
  filterable:1,
  filter:'H4sIAAAAAAAAA+2X204TURSG32WuMZndQqHcyfl8PhsuKk6UiJhANSGEBFOKLaeqia2EekqAloTa4glpU3yZ7im8hTPMmrVWozSNYoJm7ub//tntXjN77X/PouL2KPW3FpX72oJSr8xofr82p1Qps74HmqFlKqanNw392DfzSLu4cdbEweR5IGliQyhLVRa9CeAmkgYgDUgagTQiaQLShKQZSDOSFiAtSFqBtCJpA9KGpB1IO5IOIB1IOoF0IukC0oWkG0g3kh4gPUh6gfQi6QPSh6QfSD+SASADSAaBDCIZAjKEZBjIMJIRICNIRoGMIhkDMoZkHMg4kgkgE0jUG15g5tXSpMmtpXJ7gZaJvvVCZiM/LRN9I6zHl/VoBn7CP23cbf+yZRYDKTDvTfvnS8yN8Fl6RYZWwZ+fejinmTOYrFIEW7JTPr/WfofmUjzKyTfr5ZeswD+Sa8lCPl4MPwXHQ040LsMJcmrRKYaO9ECQnDpyEs/lSY4cLxX05Jm+HCVHqGSFXhWyYWa5Sp6zb07zsYaMZ+RGtsKGlLuJ8237+YGwvfP9bf1bGjwQOC6S0U9O7XGWwBJPt+ROHjwQWMmnl+SBsL2z9SPyQOC42J4eP7THWQLn+faAxoHAeZ4ekweC5pLhc8mUjNvMyOy+Pc4SOG4lYjwpGTqwh6LGSva+FyOpYnjbLgY1f20Lmo/voyefC7l8ha/NpbqqgV1cMu4m7ubcRdzFuSAuOFeJq4wLL3Lh5byOeB3ntcRrOfcQ93BeQ7yGc6pX8HoF1St4vYLqFbxeQfUKXq+gegWvV6V6VV6vSvUal/y1zvhm79JrPUunzpLLlXbjTt643151lmDdQR4I7LiPu+SBwO6I5eVmjGzSrH+YbQnWd+SBYL3MPEuwvmOVWAK94Ff5IWB7lih5gM4JwzlhXI8TxqXHC9cfHi9oSzKayjhE2Ji2Qv3LsdyNMot2T2NnKGQTZLGNz8hoI42ZRXulmYzEaW81E5q458pOFqtB4367yy1RSWL/7qmj3Amh/Ink8lNA2RNJNCPX3snX7+2hqNk+V8hFaZ8zhZP/Tv7/L/nv5LiT4/96jrtZjv+lsLMi2W4hS7D2MhqO2ssU6B0mjKiyPUs48eHEhxMfTnw48XE94qP6iuLj4oOOGtcUlXzX/DIiKvz6cNrLaa/r3V5LPwCF99KlehwAAA==',
  filter_url:'{{fl.cateId}}-{{fl.area}}-{{fl.by}}--{{fl.lang}}-{{fl.letter}}---fypage---{{fl.year}}',
  //实例 https://slzc.cn/vodshow/6-大陆-hits--国语-A---2---2024.html
  filter_def:{
   1:{cateId:'1'},
   2:{cateId:'2'},
   3:{cateId:'3'},
   4:{cateId:'4'},
   36:{cateId:'36'}
  },
  cate_exclude:'角色|剧情|专题|最新|排行|',
  }