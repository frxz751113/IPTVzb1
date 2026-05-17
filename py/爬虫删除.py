import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(BASE, "delete_list.txt")

def delete_subclasses(dir_path, base_name):
    """删除 dir_path 目录下，base_name$ 开头的所有 smali 文件"""
    if not os.path.isdir(dir_path):
        return

    prefix = base_name + "$"
    for f in os.listdir(dir_path):
        if f.startswith(prefix) and f.endswith(".smali"):
            full = os.path.join(dir_path, f)
            try:
                os.remove(full)
                print(f"   🔗 已删除子类: {full}")
            except Exception as e:
                print(f"   ❌ 删除子类失败: {full} -> {e}")

def delete():
    if not os.path.exists(LIST_FILE):
        print("❌ delete_list.txt 不存在")
        return

    deleted = 0
    skipped = 0

    print("📂 开始执行删除（支持主类已删的情况）")
    print("-" * 60)

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue
            if line.startswith("##"):
                continue

            # ✅ 只处理“主类:”行
            if "主类:" not in line:
                continue

            # ✅ 提取路径
            path = line.split("主类:", 1)[1].strip()
            path = path.replace("/", "\\")

            dir_path = os.path.dirname(path)
            file_name = os.path.basename(path)

            if not file_name.endswith(".smali"):
                continue

            base_name = file_name[:-6]  # 去掉 .smali

            # ✅ 情况 1：主类还存在 → 先删主类，再删子类
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"🗑️ 已删除主类: {path}")
                    deleted += 1
                except Exception as e:
                    print(f"❌ 删除主类失败: {path} -> {e}")
                    skipped += 1

                delete_subclasses(dir_path, base_name)

            # ✅ 情况 2：主类已被删 → 只删子类
            else:
                print(f"⚠️ 主类已不存在，尝试删除子类: {base_name}$*")
                before = deleted
                delete_subclasses(dir_path, base_name)
                after = deleted

                if before == after:
                    print(f"   ⚠️ 未找到子类")
                    skipped += 1

    print("-" * 60)
    print(f"✅ 完成")
    print(f"   删除: {deleted}")
    print(f"   跳过: {skipped}")

if __name__ == "__main__":
    delete()
