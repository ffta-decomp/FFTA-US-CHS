# FFTA2-US-CHS

《最终幻想战略版 A2》美版（Nintendo DS）中文汉化补丁发布页。

当前正式版为 **1.0.7**，提供纯净版（clean）和增强版（plus）。增强版包含既有增强功能，以及「日版汉化体」「Z工坊圆」「文泉驿宋」三种可选字体。

- [下载 1.0.7 正式版补丁](https://github.com/ffta-decomp/FFTA2-US-CHS/releases/tag/v1.0.7)
- [完整更新日志与模拟器兼容性](CHANGELOG.md)
- [V4.1 最终字表：默认编号、游戏编码与 Unicode](charset/v4.1/)
- [下载离线资料站：单 HTML ZIP](downloads/ffta2-public-site.zip)

本版调整增强版字体中的英文字母、数字及部分符号，增加 AP 倍率与招募基准选项，并支持保存四项修改器设置。纯净版保留原有第一幕开屏；增强版默认显示三幕，后两幕可独立选择。

下载并解压 Release 中的 ZIP，用 Chrome、Edge 或 Safari 打开其中的离线 HTML 补丁工具。选择自己持有的 USA 原版 ROM，或补丁器列出的已支持旧汉化版；支持 `.nds` 文件和内含单个 `.nds` 文件的 ZIP。按页面说明选择版本与功能，生成新的游戏文件。

补丁处理在本机离线完成。升级前请备份游戏内普通存档，勿跨版本加载模拟器即时存档。本版尚未完成完整通关验证；历史版本的反馈和验证范围见更新日志。

本仓库提供用户文档、公开字表和二进制汉化补丁，不提供游戏 ROM、存档、原始汉化脚本或素材。下载包包含离线 HTML 补丁工具、Release Log、汉化版使用声明和作者声明；署名、使用说明及第三方许可均在包内。

## 构建离线资料站

安装 Python 3 后，在仓库目录运行：

```sh
python3 tools/build_site.py
```

输出为 `dist/site/index.html` 和 `dist/site/ffta2-public-site.zip`。ZIP 内只有一个 HTML，解压后直接打开即可阅读说明、查询字表和导出内嵌数据，无需服务器或额外依赖。外部 Release 下载链接仍需联网；资料站不包含 ROM 或补丁器。详见[构建说明](site/README.md)。
