import urllib.request as req
import re

# ======================
# ✅ EPG 配置
# ======================

EPISODES = {
    "https://epg.112114.xyz/pp.xml": "pp.xml",
    "https://epg.pw/xmltv/epg_HK.xml": "HK.xml",
    "https://epg.pw/xmltv/epg_TW.xml": "third.xml"
}

MERGED_OUTPUT = "merged_epg.xml"


# ======================
# ✅ 下载 EPG
# ======================

def download_epg(url, filename):
    try:
        request = req.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        with req.urlopen(request, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")

            # HTML 里提取 XML
            if "<tv" in raw and "<programme" in raw:
                xml_match = re.search(r"(<\?xml.*?</tv>)", raw, re.S)
                if xml_match:
                    raw = xml_match.group(1)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(raw)

            print(f"✅ 下载成功: {filename}")

    except Exception as e:
        print(f"❌ 下载失败: {url} -> {e}")


# ======================
# ✅ 文本级合并（按你规则）
# ======================

def merge_xmltv_text(files, output):
    all_lines = []

    for idx, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 去掉多余空行
        lines = [l.rstrip("\n") for l in lines if l.strip()]

        if idx == 0:
            # ✅ 第一个文件：取前两行作为头
            all_lines.extend(lines[:2])
            all_lines.extend(lines[2:-1])
        elif idx == len(files) - 1:
            # ✅ 最后一个文件：取中间 + 最后一行作为尾
            all_lines.extend(lines[1:-1])
            all_lines.append(lines[-1])
        else:
            # ✅ 中间文件：去掉头尾
            all_lines.extend(lines[1:-1])

    # ✅ 写最终文件
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

    print(f"✅ 文本级合并完成: {output}")


# ======================
# ✅ 主流程
# ======================

def main():
    files = []

    for url, filename in EPISODES.items():
        download_epg(url, filename)
        files.append(filename)

    if files:
        merge_xmltv_text(files, MERGED_OUTPUT)
    else:
        print("❌ 没有可用的 EPG 文件")


if __name__ == "__main__":
    main()
