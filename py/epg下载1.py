from urllib.request import Request, urlopen
import re
import gzip
import io

urls = {
    "https://e.erw.cc/all.xml.gz": "pp.xml"   # ✅ 最终保存的文件名
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
                print("📦 检测到 gzip，正在解压...")
                with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz_file:
                    raw_data = gz_file.read()

            # 统一按文本处理
            text = raw_data.decode("utf-8", errors="ignore")

            # ✅ 提取 XML 主体
            xml_match = re.search(
                r"(<\?xml.*?</tv>)",
                text,
                re.S
            )

            if xml_match:
                xml_text = xml_match.group(1)
            else:
                xml_text = text

            # ✅ 保存为真正的 XML 文件
            with open(filename, "w", encoding="utf-8") as f:
                f.write(xml_text)

            print(f"✅ 成功生成 XML: {filename}")

    except Exception as e:
        print(f"❌ 下载失败: {url} -> {e}")
