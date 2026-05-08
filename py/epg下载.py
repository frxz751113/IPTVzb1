import urllib.request as req
import re
import os

# ======================
# ✅ EPG 配置区（三组预留）
# ======================

EPISODES = {
    "https://epg.112114.xyz/pp.xml": "pp.xml",
    #"https://epg.pw/xmltv/epg_HK.xml": "HK.xml",
    #"https://epg.pw/xmltv/epg_TW.xml": "third.xml"
}

MERGED_OUTPUT = "epg.xml"

# ======================
# ✅ 要删除的标签行（仅限行级）
# ======================

REMOVE_TAGS = {
    "<desc>",
    "<date>",
    "<audio>",
    "<stereo>",
    "</audio>"
}


# ======================
# ✅ 下载单个 EPG
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

            # HTML 页面里提取 XML
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
# ✅ 文本级合并 + 行级清洗
# ======================

def merge_xmltv_text(files, output):
    all_lines = []

    for idx, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned = []

        for line in lines:
            stripped = line.strip()

            # ✅ 只删除指定的行级标签
            if any(stripped.startswith(tag) for tag in REMOVE_TAGS):
                continue

            cleaned.append(line.rstrip("\n"))

        # ✅ 第一个文件：保留头两行
        if idx == 0:
            all_lines.extend(cleaned[:2])
            all_lines.extend(cleaned[2:-1])

        # ✅ 最后一个文件：保留尾部
        elif idx == len(files) - 1:
            all_lines.extend(cleaned[1:-1])
            all_lines.append(cleaned[-1])

        # ✅ 中间文件
        else:
            all_lines.extend(cleaned[1:-1])

    # ✅ 写最终文件
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

    print(f"✅ 合并完成（已移除多余标签行）: {output}")


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

files_to_remove = ['pp.xml', 'HK.xml', "third.xml"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在,则提示异常并打印提示信息
        print(f"文件 {file} 不存在,跳过删除。")
        
if __name__ == "__main__":
    main()
