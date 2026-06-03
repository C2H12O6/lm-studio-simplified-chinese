#!/usr/bin/env python3
"""
LM Studio 简体中文汉化补丁 v3.0
适用于 LM Studio 0.4.15+ (Electron/Webpack)

工作原理:
  1. 将 react-i18next 语言从 en 切换到 zh_CN (启用内置中文翻译)
  2. 替换所有硬编码的英文 UI 文本为中文 (children/title/label/tooltip/placeholder 等)

用法:
  python patch_lmstudio.py                    # 应用汉化
  python patch_lmstudio.py --restore          # 恢复英文
  python patch_lmstudio.py --path <目录>       # 指定 LM Studio 路径
  python patch_lmstudio.py --dry-run          # 预览模式
"""
import os, sys, re, shutil, json, time

VERSION = "3.0.0"

def get_default_path():
    """自动检测 LM Studio 安装路径"""
    candidates = [
        r"C:\Program Files\LM Studio",
        r"C:\Program Files (x86)\LM Studio",
        os.path.expandvars(r"%LOCALAPPDATA%\LM-Studio"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\LM Studio"),
        os.path.expanduser("/Applications/LM Studio.app/Contents/Resources"),
        os.path.expanduser("~/.config/LM-Studio"),
    ]
    for p in candidates:
        js = os.path.join(p, "resources", "app", ".webpack", "renderer", "main_window.js")
        if os.path.exists(js):
            return p
    return r"C:\Program Files\LM Studio"

def get_js_path(lm_path):
    return os.path.join(lm_path, "resources", "app", ".webpack", "renderer", "main_window.js")

def load_translations():
    """加载翻译字典"""
    dict_path = os.path.join(os.path.dirname(__file__), "T_dict.json")
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Inline fallback (minimal)
    print("Warning: T_dict.json not found, using built-in translations only")
    return {}

def patch(content, translations):
    """单次正则遍历，高效替换所有模式"""
    # Step 1: 切换 i18n 语言
    old_init = 'lng:"en",defaultNS:"sidebar",fallbackLng:"en"'
    new_init = 'lng:"zh_CN",defaultNS:"sidebar",fallbackLng:"en"'
    if old_init in content:
        content = content.replace(old_init, new_init)

    # Step 2: 替换所有 JSX 属性中的英文文本
    attrs = ["children", "title", "label", "tooltip", "placeholder",
             "aria-label", "description", "prettyName", "subtitle",
             "sectionTitle", "labelSubtext"]
    pattern = "(?:" + "|".join(attrs) + '):"([^"]+)"'

    def repl(m):
        attr = m.group(0).split(':"')[0]
        en = m.group(1)
        if en in translations:
            return f'{attr}:"{translations[en]}"'
        return m.group(0)

    content, n1 = re.subn(pattern, repl, content)

    # Step 3: 处理方括号 children:["..."] 模式
    for en, zh in translations.items():
        old = f'children:["{en}"'
        new = f'children:["{zh}"'
        if old in content:
            content = content.replace(old, new)
            n1 += 1

    # Step 4: 处理 JS 常量赋值 t.XXX="English"
    for en, zh in translations.items():
        if en in content and len(en) > 5:
            old = f'="{en}"'
            new = f'="{zh}"'
            if old in content and en[0].isupper():
                content = content.replace(old, new, 1)
                n1 += 1

    return content, n1


def main():
    import argparse
    p = argparse.ArgumentParser(description=f"LM Studio 简体中文汉化补丁 v{VERSION}")
    p.add_argument("--path", default=None, help="LM Studio 安装目录 (默认自动检测)")
    p.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改")
    p.add_argument("--restore", action="store_true", help="恢复英文原始界面")
    args = p.parse_args()

    lm_path = args.path or get_default_path()
    js_path = get_js_path(lm_path)

    if not os.path.exists(js_path):
        print(f"错误: 未找到 LM Studio 界面文件")
        print(f"  路径: {js_path}")
        print(f"  请使用 --path 参数指定正确的 LM Studio 安装目录")
        return 1

    # 备份目录
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".backups")
    os.makedirs(backup_dir, exist_ok=True)
    backup = os.path.join(backup_dir, "main_window.js.original")

    if args.restore:
        if os.path.exists(backup):
            shutil.copy2(backup, js_path)
            print("已恢复英文原始界面")
            return 0
        print(f"错误: 备份文件不存在 {backup}")
        return 1

    # 创建备份
    if not os.path.exists(backup):
        shutil.copy2(js_path, backup)
        print(f"已备份: {backup}")

    # 加载翻译
    translations = load_translations()
    if not translations:
        print("错误: 翻译字典为空")
        return 1

    # 读取文件
    with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if args.dry_run:
        _, count = patch(content, translations)
        print(f"预览: 可替换 {count} 处文本")
        return 0

    # 应用补丁
    t0 = time.time()
    content, count = patch(content, translations)

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(content)

    elapsed = time.time() - t0
    print(f"汉化完成! 共替换 {count} 处文本 (耗时 {elapsed:.1f}秒)")
    print(f"备份: {backup}")
    print()
    print("下一步:")
    print("  1. 完全退出 LM Studio (右键托盘图标 → Quit)")
    print("  2. 重新打开 LM Studio")
    print("  3. 设置页面中的界面将显示中文")
    print()
    print(f"恢复英文: python {os.path.basename(__file__)} --restore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
