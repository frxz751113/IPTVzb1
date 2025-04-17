from urllib.request import Request, urlopen

urls = [
    "https://epg.112114.xyz/pp.xml.gz"
]

downloaded_file_name = "pp.xml.gz"

# 遍历URL列表，下载文件
for url in urls:
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urlopen(req) as response:
            data = response.read()
            with open(downloaded_file_name, 'wb') as file:
                file.write(data)
            print(f"成功下载文件: {downloaded_file_name} 来自 {url}")
    except Exception as e:
        print(f"下载文件时出错: {e} 对于URL: {url}")
