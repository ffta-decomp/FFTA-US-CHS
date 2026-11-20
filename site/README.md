# 单文件离线资料站

构建入口：`python3 tools/build_site.py`。Windows可使用`py -3 tools/build_site.py`。

仅依赖Python标准库，从仓库已公开的README、更新日志、V4.1字符映射及字体布局数据生成页面。不会访问游戏ROM、字体文件、存档或私有构建输入，也不联网下载依赖。

输出目录为`dist/site/`，可用`--output 路径`指定其他目录：

- `index.html`：CSS、JavaScript和公开数据全部内嵌，可通过`file://`直接打开。
- `ffta2-public-site.zip`：只含上述`index.html`。
- `build.json`：构建输入及输出摘要，留在ZIP之外。

页面包含项目说明、4368行字表查询／筛选／分页、CSV／JSON／TBL下载、字体空间说明与累计更新记录。构建会校验字表目录的SHA-256清单、完整编号、游戏编码、Unicode对应及ZIP回读。输出ZIP固定元数据；同一组输入重复构建得到相同结果。

当前提供的资料站快照对应汉化版 1.0.8-fix，字表版本 V4.1。

离线功能不发起网络请求。点击GitHub、Gitee或Release等外部链接时仍需联网。资料站是文档浏览器，不是ROM汉化补丁器。

`site/template.html`是页面模板，`tools/build_site.py`负责公开文件读取和打包。`downloads/ffta2-public-site.zip`为维护者已生成的便捷取用副本；更新公开资料后需重新构建并替换该副本。不需要在线构建流水线或Gitee Pages。
