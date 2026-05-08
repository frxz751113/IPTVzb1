from urllib.request import Request, urlopen
import re
import gzip
import io

urls = {
    "https://e.erw.cc/all.xml.gz": "e.xml.gz",
    # "https://epg.pw/xmltv/epg_HK.xml": "HK.xml"
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

            # ✅ 判断是否为 gzip
            content_encoding = resp.headers.get("Content-Encoding", "").lower()
            is_gzip = (
                content_encoding == "gzip"
                or url.lower().endswith(".xml.gz")
            )

            if is_gzip:
                # 解压 gzip
                with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz_file:
                    raw_data = gz_file.read()

            # 统一按文本处理
            text = raw_data.decode("utf-8", errors="ignore")

            # ✅ 判断是不是 XML（哪怕被 HTML 包着）
            if "<tv" in text and "<programme" in text:
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

            # ❌ 非 XML
            print(f"❌ 跳过（不是 XML）: {url}")

    except Exception as e:
        print(f"❌ 下载失败: {url} -> {e}")
