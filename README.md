# 📰 NewsCrawler

## 🕸️ 仓库描述 🕸️

该仓库是一个新闻爬虫项目，用于从多个新闻源中获取新闻数据,如央视新闻、网易新闻、新浪新闻、腾讯新闻、今日头条等。

## 🚀 功能特性

- **多新闻源支持**：支持从多个主流新闻网站抓取数据。
- **数据存储**：支持将抓取的新闻数据存储到 Mysql 数据库中。
- **定时任务**：支持定时抓取新闻数据，保持数据更新。
- **钉钉通知**：支持通过钉钉机器人发送抓取新闻。

---

## 📊 支持的新闻源

| 网站   | 国内最新新闻 | 热点新闻 |
|------|--------|------|
| 央视新闻 | ✅      | ❌    |
| 网易新闻 | ✅      | ✅    |
| 新浪新闻 | ✅      | ✅    |
| 腾讯新闻 | ✅      | ✅    |
| 今日头条 | ❌      | ✅    |

---

## 🛠️ 快速开始

### 1. 安装依赖

确保已安装 Python 3.11 或更高版本，然后运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

或

```bash
poetry install
```

### 3. 运行爬虫

运行以下命令启动指定新闻源的爬虫：

```bash
python main.py --spider <spider_name> --news-type <news_type>
```

- **`<spider_name>`**：爬虫名称，可选值：`cctv`、`netease`、`sina`、`tencent`、`toutiao`。
- **`<news_type>`**：新闻类型，可选值：`hot_news`（热点新闻）或 `latest_china_news`（国内最新新闻）。

#### 启动定时任务

如果需要定时抓取新闻，可以使用 `--interval` 参数指定抓取间隔（单位：分钟）：

```bash
python main.py --spider netease --news-type hot_news --interval 10
```



---

## 📜 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目。
2. 创建新的分支 (`git checkout -b feature/YourFeature`)。
3. 提交更改 (`git commit -m 'Add some feature'`)。
4. 推送到分支 (`git push origin feature/YourFeature`)。
5. 提交 Pull Request。

---

## 📧 联系

如有问题或建议，请联系：  
📩 Email: 1078769434@qq.com

---

## 🙏 致谢

