from urllib.request import Request, urlopen
import re

urls = {
    "https://epg.112114.xyz/pp.xml": "pp.xml",
    #"https://epg.pw/xmltv/epg_HK.xml": "HK.xml"
}

for url, filename in urls.items():
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        with urlopen(req, timeout=30) as resp:
            raw_data = resp.read()

            # 先当文本处理
            text = raw_data.decode("utf-8", errors="ignore")

            # ✅ 判断是不是 XML（哪怕被 HTML 包着）
            if "<tv" in text and "<programme" in text:
                # 提取 XML 主体（防止前面有 HTML）
                xml_content = re.search(
                    r"(<\?xml.*?</tv>)",
                    text,
                    re.S
                )

                if xml_content:
                    xml_text = xml_content.group(1)
                else:
                    xml_text = text

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(xml_text)

                print(f"✅ 成功保存 XML: {filename}")
                continue

            # ❌ 否则认为是普通网页，直接拒绝
            print(f"❌ 跳过（不是 XML）: {url}")

    except Exception as e:
        print(f"❌ 下载失败: {url} -> {e}")
