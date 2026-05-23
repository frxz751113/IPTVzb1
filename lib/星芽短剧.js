/*
@header({
  name: "星芽短剧",
  version: "1.0",
  type: 3,
  searchable: 1,
  quickSearch: 1,
  filterable: 1
})
*/

/// ===== 配置 =====
var HOST = "https://app.whjzjx.cn";
var TOKEN = "";

/// ===== 请求 =====
function request(url, data) {
    return java.Request(url, {
        method: "POST",
        headers: {
            "User-Agent": "okhttp/3.12.11",
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": TOKEN
        },
        data: JSON.stringify(data)
    });
}

/// ===== 初始化（登录）=====
function init(cfg) {
    try {
        var res = JSON.parse(request("https://u.shytkjgs.com/user/v1/account/login", {
            device: "24250683ETLHxxRgZTr7bhjrZuRzMnGs1M7dz8h8R"
        }));
        TOKEN = res.data.token || "";
    } catch (e) {
        TOKEN = "";
    }
    return true;
}

/// ===== 分类 =====
function home() {
    return JSON.stringify({
        class: [
            { type_id: "1", type_name: "剧场" },
            { type_id: "2", type_name: "热播剧" },
            { type_id: "3", type_name: "新剧" },
            { type_id: "5", type_name: "阳光剧场" },
            { type_id: "7", type_name: "星选好剧" },
            { type_id: "8", type_name: "会员专享" }
        ]
    });
}

/// ===== 列表 =====
function category(tid, pg, filter, extend) {
    var url = HOST + "/cloud/v2/theater/home_page?theater_class_id=" + tid +
              "&type=1&class2_ids=0&page_num=" + pg + "&page_size=24";

    var res = JSON.parse(request(url, {}));
    var list = [];

    if (res.data && res.data.list) {
        for (var i = 0; i < res.data.list.length; i++) {
            var v = res.data.list[i];
            list.push({
                vod_id: HOST + "/v2/theater_parent/detail?theater_parent_id=" + v.theater.id,
                vod_name: v.theater.title,
                vod_pic: v.theater.cover_url,
                vod_remarks: v.theater.total + "集"
            });
        }
    }

    return JSON.stringify({
        list: list,
        page: pg,
        pagecount: pg + 1
    });
}

/// ===== 详情 =====
function detail(ids) {
    var res = JSON.parse(request(ids[0], {}));
    var d = res.data;
    var urls = [];

    if (d.theaters) {
        for (var i = 0; i < d.theaters.length; i++) {
            urls.push(d.theaters[i].num + "$" + d.theaters[i].son_video_url);
        }
    }

    return JSON.stringify({
        list: [{
            vod_id: ids[0],
            vod_name: d.title,
            vod_pic: d.cover_url,
            vod_content: d.introduction,
            vod_play_from: "星芽",
            vod_play_url: urls.join("#")
        }]
    });
}

/// ===== 搜索 =====
function search(wd, quick) {
    var url = HOST + "/v3/search?keyword=" + encodeURIComponent(wd);
    var res = JSON.parse(request(url, {}));
    var list = [];

    if (res.data && res.data.list) {
        for (var i = 0; i < res.data.list.length; i++) {
            var v = res.data.list[i];
            list.push({
                vod_id: HOST + "/v2/theater_parent/detail?theater_parent_id=" + v.theater.id,
                vod_name: v.theater.title,
                vod_pic: v.theater.cover_url,
                vod_remarks: v.theater.total + "集"
            });
        }
    }

    return JSON.stringify({ list: list });
}
