# 我的 Star 项目导航  2025/5/5

一个自动同步 GitHub Stars 并按类别展示的项目。
## 项目结构

```
my-stared-list/
├── .github/
│   └── workflows/
│       ├── update_stars.yml      # 自动同步 starred 仓库
│       └── generate_category.yml # 自动生成分类模板
├── star-category.yaml           # 手动维护的分类配置
├── star-category-by-keywords.yaml # 自动生成的分类模板
├── update_readme.py             # 生成 README.md
├── generate_category_template.py # 自动生成分类模板
└── index.html                   # docsify 页面
```

## 文件说明

| 文件                                        | 说明                                     | 编辑方式                         |
| ------------------------------------------- | ---------------------------------------- | -------------------------------- |
| `.github/workflows/update_stars.yml`      | GitHub Actions 工作流，同步 starred 仓库 | 手动配置                         |
| `.github/workflows/generate_category.yml` | GitHub Actions 工作流，自动生成分层分类  | 手动配置                         |
| `star-category.yaml`                      | 手动维护的分类配置文件                   | **手动编辑**               |
| `star-category-by-keywords.yaml`          | 自动生成的分类模板                       | **自动生成，请勿手动编辑** |
| `update_readme.py`                        | 读取分类配置，生成 README.md             | 手动配置                         |
| `generate_category_template.py`           | 根据关键词自动分类仓库                   | 手动配置                         |
| `index.html`                              | docsify 页面配置                         | 手动配置                         |

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions                              │
├─────────────────────────────────────────────────────────────────┤
│  update_stars.yml                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │ GitHub API   │ --> │ 生成 README  │ --> │  Push 到仓库  │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  generate_category.yml                                          │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │ 解析 README  │ --> │ 关键词分类   │ --> │ 更新分类文件  │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 分类机制

```
┌─────────────────────────────────────────────────────────────┐
│  自动分类流程                                               │
├─────────────────────────────────────────────────────────────┤
│  1. 读取 README.md 解析仓库列表                              │
│  2. 对每个仓库名称进行关键词匹配                              │
│  3. 统计每个类别匹配的关键词数量                              │
│  4. 选择匹配数量最多的类别作为归属                            │
│  5. 如果无匹配，归入"其他"类别                               │
└─────────────────────────────────────────────────────────────┘
```
## 工作流程

### 1. 同步 Stars (update_stars.yml)
- **触发方式**: 每周一 01:00 UTC + 手动触发
- **功能**: 从 GitHub API 获取 starred 仓库，保存到 README.md

### 2. 生成分类 (generate_category.yml)
- **触发方式**: 每周日、周三 01:00 UTC + 手动触发
- **功能**: 根据仓库名称关键词自动分类，输出 star-category-by-keywords.yaml
- **分类逻辑**: 单标签分类，每个项目只归属一个类别

## 分类优先级

关键词匹配数量最多的类别优先。例如 `tmwgsicp/wechat-download-api` 匹配：
- `舆情分析`: 3个关键词
- `ESP32/Hardware`: 2个关键词
- 其他: 更少

最终归入 **舆情分析**。

## 手动调整分类

如需手动调整某个项目的分类：
1. 编辑 `star-category.yaml`
2. 将目标项目移到新类别
3. 触发 workflow 时会保留你的调整

## 注意事项

1. `star-category-by-keywords.yaml` 由代码自动生成，**不要手动编辑**
2. 如需自定义分类，请编辑 `star-category.yaml`
3. GitHub Token 权限不足会导致 workflow 失败
4. API 速率限制可能影响获取数量

## 部署

本项目使用 docsify 展示，部署在 GitHub Pages。

如需启用：
1. 进入仓库 Settings → Pages
2. Source 选择 `main` branch, `/ (root)` folder
3. 等待几分钟即可访问
