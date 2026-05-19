var rule = {
    title: 'iFun',
    host: 'https://ifun.cc',
    url: '/list/fyclass/fyfilter',
    searchUrl: '/search?key=**',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    filter: {
        'movie': [{ key: '类型', name: '类型', value: [{ n: '剧情', v: 'ju-qing?', }, { n: '喜剧', v: 'xi-ju?', }, { n: '爱情', v: 'ai-qing?', }, { n: '动作', v: 'dong-zuo?', }, { n: '惊悚', v: 'jing-song?', }, { n: '犯罪', v: 'fan-zui?', }, { n: '悬疑', v: 'xuan-yi?', }, { n: '恐怖', v: 'kong-bu?', }, { n: '科幻', v: 'ke-huan?', }, { n: '奇幻', v: 'qi-huan?', }, { n: '传记', v: 'chuan-ji?', }, { n: '战争', v: 'zhan-zheng?', }, { n: '家庭', v: 'jia-ting?', }, { n: '冒险', v: 'mao-xian?', }, { n: '人性', v: 'ren-xing?', }, { n: '青春', v: 'qing-chun?', }, { n: '历史', v: 'li-shi?', }, { n: '文艺', v: 'wen-yi?', }, { n: '温情', v: 'wen-qing?', }, { n: '搞笑', v: 'gao-xiao?', },], },],
        'tv': [{ key: '类型', name: '类型', value: [{ n: '国产剧', v: '?region=cn&', }, { n: '港剧', v: '?region=hk&', }, { n: '台剧', v: '?region=tw&', }, { n: '日剧', v: '?region=jp&', }, { n: '韩剧', v: '?region=kr&', }, { n: '欧美剧', v: '?region=west&', }, { n: '英剧', v: '?region=gb&', }, { n: '泰剧', v: '?region=th&', }, { n: '其它', v: '?region=other&', }, { n: '剧情', v: 'ju-qing?', }, { n: '爱情', v: 'ai-qing?', }, { n: '喜剧', v: 'xi-ju?', }, { n: '悬疑', v: 'xuan-yi?', }, { n: '犯罪', v: 'fan-zui?', }, { n: '古装', v: 'gu-zhuang?', }, { n: '奇幻', v: 'qi-huan?', }, { n: '惊悚', v: 'jing-song?', }, { n: '科幻', v: 'ke-huan?', }, { n: '家庭', v: 'jia-ting?', }, { n: '动作', v: 'dong-zuo?', }, { n: '历史', v: 'li-shi?', }, { n: '青春', v: 'qing-chun?', }, { n: '搞笑', v: 'gao-xiao?', }, { n: '推理', v: 'tui-li?', }, { n: '战争', v: 'zhan-zheng?', }, { n: '人性', v: 'ren-xing?', }, { n: '女性', v: 'nv-xing?', }, { n: '同性', v: 'tong-xing?', }, { n: '武侠', v: 'wu-xia?', },], },],
        'variety': [{ key: '类型', name: '类型', value: [{ n: '真人秀', v: 'zhen-ren-xiu?', }, { n: '脱口秀', v: 'tuo-kou-xiu?', }, { n: '音乐', v: 'yin-le?', }, { n: '搞笑', v: 'gao-xiao?', }, { n: '喜剧', v: 'xi-ju?', }, { n: '美食', v: 'mei-shi?', }, { n: '温情', v: 'wen-qing?', }, { n: '文化', v: 'wen-hua?', }, { n: '歌舞', v: 'ge-wu?', },], },],
        'anime': [{ key: '类型', name: '类型', value: [{ n: '喜剧', v: 'xi-ju?', }, { n: '奇幻', v: 'qi-huan?', }, { n: '冒险', v: 'mao-xian?', }, { n: '剧情', v: 'ju-qing?', }, { n: '科幻', v: 'ke-huan?', }, { n: '动作', v: 'dong-zuo?', }, { n: '搞笑', v: 'gao-xiao?', }, { n: '爱情', v: 'ai-qing?', }, { n: '家庭', v: 'jia-ting?', }, { n: '儿童', v: 'er-tong?', }, { n: '短片', v: 'duan-pian?', }, { n: '温情', v: 'wen-qing?', }, { n: '悬疑', v: 'xuan-yi?', },], },],
        'doc': [{ key: '类型', name: '类型', value: [{ n: '传记', v: 'chuan-ji?', }, { n: '历史', v: 'li-shi?', }, { n: '自然', v: 'zi-ran?', }, { n: '音乐', v: 'yin-le?', }, { n: '剧情', v: 'ju-qing?', }, { n: '美食', v: 'mei-shi?', }, { n: '社会', v: 'she-hui?', }, { n: '犯罪', v: 'fan-zui?', },], },],
    },
    filter_url: '{{fl.类型}}page=fypage',
    filter_def: {},
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 5000,
    class_parse: 'ul.cat-menu&&li;a&&Text;a&&href;list/(.*?)/',
    cate_exclude: '',
    play_parse: true,
    lazy: $js.toString(() => {
        input = { parse: 1, url: input, js: '' };
    }),
    double: true,
    推荐: '.videos;div.item;*;*;*;*',
    一级: '.videos&&a.item;.title&&Text;img&&src;.rt&&Text;a&&href',
    二级: {
        title: 'h1&&Text',
        img: 'img&&src',
        desc: '.updated&&Text',
        content: '.intro&&.inner&&p:eq(-1)&&Text',
        tabs: $js.toString(() => {
            TABS = ['播放'];
        }),
        lists: '.episode-list&&li',
        tab_text: 'body&&Text',
        list_text: 'body&&Text',
        list_url: 'a&&href',
        list_url_prefix: '',
    },
    搜索: '.videos&&div.item;*;*;div.vs&&Text;*',
}