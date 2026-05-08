import urllib.request as req
import xml.etree.ElementTree as ET
import re
from collections import defaultdict

# ======================
# ✅ EPG 配置区（三组预留）
# ======================

EPISODES = {
    "https://epg.112114.xyz/pp.xml": "pp.xml",
    "https://epg.pw/xmltv/epg_HK.xml": "HK.xml",
    "https://epg.pw/xmltv/epg_TW.xml": "third.xml"
}

MERGED_OUTPUT = "merged_epg.xml"


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
            raw = resp.read()
            text = raw.decode("utf-8", errors="ignore")

            # ✅ HTML 页面里提取 XML
            if "<tv" in text and "<programme" in text:
                xml_match = re.search(r"(<\?xml.*?</tv>)", text, re.S)
                if xml_match:
                    text = xml_match.group(1)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ 下载成功: {filename}")

    except Exception as e:
        print(f"❌ 下载失败: {url} -> {e}")


# ======================
# ✅ 合并多个 XMLTV（关键修复版）
# ======================

def merge_xmltv(files, output):
    channels = {}
    programmes = defaultdict(list)

    first_root = None

    for file in files:
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            if first_root is None:
                first_root = root  # ✅ 保留第一份 tv 属性

            for ch in root.findall("channel"):
                cid = ch.get("id")
                if cid not in channels:
                    channels[cid] = ch

            for prog in root.findall("programme"):
                programmes[prog.get("channel")].append(prog)

        except Exception as e:
            print(f"❌ 解析失败: {file} -> {e}")

    if first_root is None:
        print("❌ 没有任何可用的 XMLTV 根节点")
        return

    # ✅ 使用第一份 <tv> 的属性（generator-info-name 等）
    tv = ET.Element("tv", attrib=first_root.attrib)

    for ch in channels.values():
        tv.append(ch)

    for plist in programmes.values():
        for p in plist:
            tv.append(p)

    tree = ET.ElementTree(tv)
    tree.write(
        output,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"✅ 合并完成: {output}")


# ======================
# ✅ 主流程
# ======================

def main():
    files = []

    for url, filename in EPISODES.items():
        download_epg(url, filename)
        files.append(filename)

    if files:
        merge_xmltv(files, MERGED_OUTPUT)
    else:
        print("❌ 没有可用的 EPG 文件")


if __name__ == "__main__":
    main()
