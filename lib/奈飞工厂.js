muban.短视2.二级.lists = '.anthology-list&&.anthology-list-box:eq(#id) li';
var rule = {
  模板:'短视2',
  title: '奈飞工厂',
  host: 'https://www.netflixgc.com',
  class_name: '电影&电视剧&漫剧&综艺&记录',//&伦理
  class_url: '1&2&3&23&24',//&30
  url: '/index.php/api/vod#type=fyclassfyfilter&page=fypage',
  filterable: 1,
  filter_url: '&class={{fl.class}}&area={{fl.area}}&year={{fl.year}}&lang={{fl.lang}}&letter={{fl.letter}}&by={{fl.by}}',
  filter:'H4sIAAAAAAAAA+1aXU8bRxT9K6t9TqVZyFd5CwRSEhJIQpImVR7cyGqjUlqBWwlFSAZjwECMiRLTBIs0SVM7FIIpCAUjO3/Gs2v/i+x6hrn3Toi2luqAonnzOfd6Zvbuzp1z1n5g2Y7dYX1nPbDsn6Jj/kf73lBkdNQ+YdnDkZ+jAeFt7fPV+YD5PTL0W/QgfTiI8WShnig0YgG0rfETEMvmeCqvYhLiDG92y00kVYaEOMOdyLjxrMqQkMwyV6iWczCLgGSW/BLf24dZBCRjpPJ4HRKSMeY2vfIajCEgGeP1DJ5FQnItk+tedgmuRUCSkZhzJ59BhoBklre7vLQBswhIMqYf1Z++gQwBSUZmwY2j+yIgzqi9z/h1VBkSkpXO/lEtpWClApKKTVTqzypQMQFxxpXuwZ6+3m9VygHGOd909qt48BnHOju7rP4r3Sp+gMn3b/TdgAECgKPnBgb6uq3BmypDETirpx/WGHy2xq27Mi63TGQkGsE7hueKfKHU/I7xKmm+UoaaCUjqvvzaza1D3QXEGfXnb/AYEpL7/7DIS3/D/ReQ3P/5LTyGhGQd209whoTkWpZWefIdXIuAOKP6fsorL7vZTZUEDJ2rSOcqirn0uzAWjYyQu7C3U90vN38X2ljbSRVpAC3ajqPterQNR9v0qIOjjh5lOMq0qPM1ivpAi57F0bN69AyOntGjp3H0tB49haOn9CiulaPXysG1cvRaObhWjl4rB9fK0Wvl4Fo5eq0YrhXTa8VwrZheK4ZrxfRaMVwrpteK4VoxvVYM14rptWK4VkyvFcO1YnqtGK4V02vFcK0YO2TvDEWGf8B7p7a5USvEm987fqvwv4o7RwC1DoYzJNQ6GM6QUOs+ZAwBtd6CMyTUugodo6hniJaFk4D5uJ/iPGAOqXQ0FovSPrWx7G4+bL7W5+DYoucinIiE71J8F+HPK/484eFkpWdqD5yGhL+g+Av0DIYDmPC9iu8l/EXFXyT8JcVfInyf4vsIf1nxl6nuAMVBeFAaVGcMKH6A8FcVf5Xw1xR/jfDXFX+d8IOKHyQ8CBeqWkCuUJ1yS/G3CA/qhWqr24q/Tfg7ir9DePYVNNXg88fP9vdj+Ll20494afHw59pdSLm5uJstqhFj9/1vkQ3aSPESsK1+vB8b1VNqm1N8dlqljN77ZSQqV2bd9dk227gb426MuyHEcXU34d4l3P/8F+9yuJ9AGet5d+dfyBCQPGWLRXev4uUm4EFTDMlL7lb3YYdLaLyL8S7Guxjv0tEy7+J3I2JIFo27Me7GuJuOL8zdtNstcjduZtVbR2peQNI/Ehu1F3FoHgKSzjG57m6Dq5CQavU0f/sP0uoNSNaRK/nqG9YhIOnaMzv1BMgwCclKn1Z4ZhZWKiCZJV3wMlBmCUnGny/4Cuq4AtLOv13dy6DO34BkHX9V+MpLWIeA5FpeJetxcEgSas7EzS5jZxJA7Yzi7+C9u4TUdc77XhS5zgZszmXVNx5jPyhhc/443NuGu85wb+sP6z3ex7MEsDkH/Wkv1yqvFO5zwt2U8R6CMN7DeI/j7j3CncWn3IlR4EaBGwV+dL8v6BI8NvZr9P9Q4F7uebVU8vJIYiumOaUerkzD9V74bxnheq82tcUXX+ErAuZo1VYr/3dj1JZRW0ZtSeKYqK1Wvuk1eszoMaPHjk6PnbRb9Eo00F4pEEkSUhm1Ui3NIxnVgCQjPc0X4YdlCcklZmf4AvpLiIAkI/3S24HXiBISOZNfcueQbhSQNMCZNW9qFxqggGSl4X8aKa3x8hMvNQMTKebLlXPkEDn0jwZG8BnBZwSfJIzg6zCCzwg+I/ha9xM4s6ngM/vP7D+z/z7P/rPGPwA/TveiQTwAAA==',
  filter_def: {1:{cateId:'1'},2:{cateId:'2'},3:{cateId:'3'},23:{cateId:'23'},24:{cateId:'24'},30:{cateId:'30'}},  
  推荐: '.border-box.public-r .public-list-box:gt(4);a&&title;img&&data-src;.public-list-prb&&Text;a&&href',
}