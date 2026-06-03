# LM Studio 简体中文汉化补丁

一键将 LM Studio (0.4.15+) 界面全面翻译为简体中文。

## 工作原理

LM Studio 基于 Electron + Webpack 构建，UI 文本嵌入在编译后的 `main_window.js` 中。本补丁通过两种方式实现汉化：

1. **i18n 语言切换**: 将内置的 react-i18next 语言从 `en` 切换到 `zh_CN`，自动启用侧栏、导航等所有通过翻译键管理的文本
2. **硬编码文本替换**: 使用正则表达式单次遍历，将 `children`、`title`、`label`、`tooltip`、`description` 等属性中约 3000+ 处硬编码英文替换为中文
3. 请注意，此补丁为deepseek V4pro与mimio V2.5共同创建并且交叉验证完毕，并且已人工检查，但不保证是否仍然有BUG

## 安装

### Windows (推荐)

双击 `install.bat` 或运行：

```powershell
python patch_lmstudio.py
```

### macOS / Linux

```bash
chmod +x install.sh && ./install.sh
```

### 手动安装

```bash
# 1. 将 patch_lmstudio.py 和 T_dict.json 复制到 LM Studio 安装目录
# 2. 运行
python patch_lmstudio.py
```

## 参数

| 参数 | 说明 |
|------|------|
| `--path <目录>` | 指定 LM Studio 安装目录（默认自动检测） |
| `--dry-run` | 预览模式，不实际修改文件 |
| `--restore` | 恢复英文原始界面 |

## 恢复英文

```bash
python patch_lmstudio.py --restore
```

或手动从 `.backups/main_window.js.original` 复制回去。

## 支持的功能区域

- 顶部导航栏 (对话、模型、服务、开发者、设置)
- 对话界面 (消息操作、系统提示、词元统计)
- 模型管理 (搜索、下载、加载、详情)
- 模型配置 (推理参数、覆盖设置、预设)
- 本地服务 (API、端口、认证)
- MCP/插件管理
- 所有设置页面 (外观、对话、开发者、实验性)
- LM Link 设备连接
- 转录/音频功能
- 错误提示、对话框、工具提示

## 局限性

- 修复在 LM Studio 更新后会失效，需重新运行补丁
- 部分动态生成的文本可能未被覆盖
- 不修改 Chromium 原生 UI (文件对话框等由 `.pak` 文件控制)

## 文件说明

| 文件 | 说明 |
|------|------|
| `patch_lmstudio.py` | 核心补丁脚本 |
| `T_dict.json` | 翻译字典 (1084 条) |
| `install.bat` | Windows 一键安装 |
| `install.sh` | macOS/Linux 安装脚本 |
| `.gitignore` | Git 忽略配置 |

## 贡献

欢迎提交 PR 补充翻译或修复问题。

1. Fork 本仓库
2. 在 `T_dict.json` 中添加/修改翻译
3. 提交 PR

## 许可

MIT License
