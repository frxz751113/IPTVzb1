import os
import re
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.abspath(__file__))
SPIDER = os.path.join(ROOT, "com/github/catvod/spider")
MERGE = os.path.join(ROOT, "com/github/catvod/spider/merge")

# ======================
# ✅ 绝对不可删的系统核心
# ======================
CORE_ROOTS = {
    # 入口
    "Init", "DexNative", "BaseSpiderAmns",

    # 基础工具
    "Utils", "Json", "Http", "Log", "Context",

    # 播放器解析
    "Parse", "Parser", "Parser$1", "Parser$2",
    "Player", "JsEngine", "WebView", "Regex", "Crypto",

    # 原生 / 桥接
    "Native", "NativeBridge",

    # 全局配置
    "Config", "Constant", "Global", "Setting",

    # 资源 / Dex
    "Resource", "JarLoader", "DexLoader",

    # 系统兼容
    "Compat", "SDK", "Version",

    # 👇 你指定的必须活着的系列
    "Proxy", "Zhaozy", "PushAmns", "PushAgent",
}

# ======================
# ✅ 爬虫壳说明
# ======================
SPIDER_DESC = {
    "Ali": "阿里云盘", "Bili": "哔哩哔哩", "DouYin": "抖音",
    "AList": "AList 网盘", "AppTT": "影视 APP 源", "AppYs": "影视备用源",
    "Bttwoo": "BT / 磁力",
}

# ======================
# 1️⃣ 构建调用图
# ======================
graph = defaultdict(set)
spiders = set()

def scan_file(path):
    name = os.path.basename(path).replace(".smali", "")
    spiders.add(name)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for m in re.findall(r'Lcom/github/catvod/spider/(?:merge/)?([^;]+);', line):
                t = m.split("/")[-1].replace(";", "")
                graph[name].add(t)

for root, _, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".smali") or "$" in f:
            continue
        scan_file(os.path.join(root, f))

# ======================
# 2️⃣ 动态加入 Push* 系列
# ======================
for s in list(spiders):
    if s.startswith("Push"):
        CORE_ROOTS.add(s)

# ======================
# 3️⃣ 只扩散“系统核心”的闭包（不保护普通爬虫壳）
# ======================
sys_white = set(CORE_ROOTS)
queue = deque(CORE_ROOTS)

while queue:
    cur = queue.popleft()
    for nxt in graph.get(cur, []):
        if nxt not in sys_white:
            sys_white.add(nxt)
            queue.append(nxt)

# ======================
# 4️⃣ 所有“非系统核心”的爬虫壳，全部可删
# ======================
spider_chains = {}

for spider in sorted(spiders):
    if spider in CORE_ROOTS:
        continue

    # ✅ 不管有没有被引用，统统进清单
    spider_chains[spider] = sorted(graph.get(spider, set()))

# ======================
# 5️⃣ 输出 delete_list.txt
# ======================
OUT = os.path.join(ROOT, "delete_list.txt")
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# ✅ 可删除爬虫壳（已全部列出，仅保护系统核心）\n\n")

    for spider, chain in spider_chains.items():
        desc = SPIDER_DESC.get(spider, "未知用途爬虫壳")
        f.write(f"## 🧩 {spider}  ({desc})\n")
        f.write(f"# 主类: {SPIDER}/{spider}.smali\n")

        if chain:
            f.write("# 私有插件:\n")
            for dep in chain:
                f.write(f"#   └─ {dep}\n")
        f.write("\n")

    # merge 孤儿
    used_by_spider = set()
    for chain in spider_chains.values():
        used_by_spider.update(chain)

    orphan_merges = []
    for root, _, files in os.walk(MERGE):
        for file in files:
            name = file.replace(".smali", "")
            if name not in used_by_spider and name not in CORE_ROOTS:
                orphan_merges.append(os.path.join(root, file))

    if orphan_merges:
        f.write("\n## 🧩 未被引用的插件（可安全删除）\n\n")
        for p in orphan_merges:
            f.write(f"{p}\n")

print("✅ 扫描完成（爬虫壳已全部列入删除清单）")