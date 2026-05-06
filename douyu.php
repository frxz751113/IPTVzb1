<?php
/**
 * 更多分享请关注 6i.pw APP演示地址：https://pan.qingyuji.cn/f/Lv43pio/Miguolive_3.2.1.apk
 * 更多分享请关注 6i.pw APP演示地址：https://pan.qingyuji.cn/f/Lv43pio/Miguolive_3.2.1.apk
 * 更多分享请关注 6i.pw APP演示地址：https://pan.qingyuji.cn/f/Lv43pio/Miguolive_3.2.1.apk
 */
error_reporting(0);

// ===== 基础请求函数 =====
function http_request($url, $method = 'GET', $headers = [], $data = null) {
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_TIMEOUT => 15,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false,
    ]);

    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        if ($data !== null) curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    }

    if (!empty($headers)) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }

    $res = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return ['code' => $code, 'body' => $res];
}

// ===== 获取斗鱼真实地址 =====
function get_douyu_url($roomId) {
    $did = md5(mt_rand() . microtime(true));

    // 1. 获取加密参数
    $k = http_request(
        "https://www.douyu.com/wgapi/livenc/liveweb/websec/getEncryption?did={$did}",
        'GET',
        [
            'User-Agent: Mozilla/5.0',
            'Referer: https://www.douyu.com/'
        ]
    );

    if ($k['code'] !== 200) return false;

    $encData = json_decode($k['body'], true)['data'] ?? null;
    if (!$encData) return false;

    // 2. 生成签名
    $randStr = $encData['rand_str'];
    for ($i = 0; $i < $encData['enc_time']; $i++) {
        $randStr = md5($randStr . $encData['key']);
    }

    $ts = time();
    $auth = md5($randStr . $encData['key'] . $roomId . $ts);

    $postData = http_build_query([
        'enc_data' => $encData['enc_data'],
        'tt' => $ts,
        'did' => $did,
        'auth' => $auth
    ]);

    // 3. 请求播放地址
    $res = http_request(
        "https://www.douyu.com/lapi/live/getH5PlayV1/{$roomId}",
        'POST',
        [
            'Content-Type: application/x-www-form-urlencoded',
            'User-Agent: Mozilla/5.0',
            "Referer: https://www.douyu.com/{$roomId}"
        ],
        $postData
    );

    if ($res['code'] !== 200) return false;

    $data = json_decode($res['body'], true)['data'] ?? null;
    if (!$data) return false;

    // 优先 HLS
    if (!empty($data['hls_url'])) {
        return $data['hls_url'];
    }

    // 备用 RTMP
    if (!empty($data['rtmp_url'])) {
        return $data['rtmp_url'] . '/' . $data['rtmp_live'];
    }

    return false;
}

// ===== 主入口 =====
$roomId = isset($_GET['id']) ? trim($_GET['id']) : '';

if (empty($roomId)) {
    exit('no id');
}

$url = get_douyu_url($roomId);

if ($url) {
    header("Location: " . $url);
    exit;
} else {
    exit('no stream');
}
/**
 * 更多分享请关注 6i.pw
 * 更多分享请关注 6i.pw
 * 更多分享请关注 6i.pw
 */