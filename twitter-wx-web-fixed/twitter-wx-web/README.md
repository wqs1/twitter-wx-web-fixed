# Twitter → 微信 自动推送系统（含中文 Web 管理界面）

本项目是一个基于 Docker 的自动化工具，可实时监听多个 Twitter 用户的新推文，并通过 [Server 酱](https://sct.ftqq.com/) 推送到微信。系统还提供一个 **中文 Web 控制界面**，用于配置 Token、推特账号、轮询间隔等参数，并支持查看运行日志。

---

## ✨ 功能特性

- 🐳 全容器化部署，支持一键运行
- 🧑‍💻 中文 Web 配置界面，支持密码登录
- 🔄 实时监听多个 Twitter 用户
- 📲 微信推送支持 Server 酱（免费）
- 🔐 登录认证保护
- 📜 实时查看监听日志
- 🛠️ 支持配置 Token、用户名、推送间隔等

---

## 📦 使用说明

### 1. 获取必要信息

- 前往 [Twitter 开发者平台](https://developer.twitter.com/) 获取 Bearer Token
- 注册并登录 [Server 酱](https://sct.ftqq.com/) 获取 `SendKey`

### 2. 快速部署（使用 Docker）

```bash
# 解压
unzip twitter-wx-web.zip
cd twitter-wx-web

# 启动
docker-compose up -d
```

### 3. 访问 Web 控制台

浏览器打开：http://你的服务器IP:8080

默认登录：

- 用户名：`admin`
- 密码：`123456`

---

## 🧾 项目结构

```
twitter-wx-web/
├── app/
│   ├── web.py           # Web 服务
│   ├── listener.py      # 推特监听器
│   ├── config.json      # 配置文件
│   ├── log.txt          # 日志文件
│   └── templates/       # HTML 模板
├── Dockerfile
├── docker-compose.yml
├── supervisord.conf     # 管理监听进程
└── requirements.txt
```

---

## 🔐 安全建议

- 初次登录后请立即修改默认密码
- 配置文件 `config.json` 中包含敏感 Token，上传 GitHub 时请将其加入 `.gitignore`

---

## 📄 LICENSE

MIT License - 可自由使用和修改
