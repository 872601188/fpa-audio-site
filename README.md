# 功能点审核培训音频系统

基于 Flask + Bootstrap + SQLite 的音频播放网站，支持 OSS 音频在线播放和下载。

## 🚀 快速开始

### 方式一：直接运行

```bash
cd /root/.openclaw/workspace/fpa-audio-site
./start.sh
```

### 方式二：手动启动

```bash
cd /root/.openclaw/workspace/fpa-audio-site
python3 app.py
```

## 🌐 访问地址

- **本地访问**: http://localhost:5000
- **局域网访问**: http://你的IP:5000

## 🔐 登录信息

- **用户名**: `Admin`
- **密码**: `Admin123`

## 📁 项目结构

```
fpa-audio-site/
├── app.py                 # Flask 主应用
├── start.sh               # 启动脚本
├── fpa_audio.db           # SQLite 数据库（自动创建）
├── templates/
│   ├── login.html         # 登录页面
│   ├── index.html         # 音频列表页面
│   └── player.html        # 音频播放器页面
└── README.md              # 本文件
```

## ✨ 功能特性

- ✅ 用户登录认证（Session + Cookie）
- ✅ Bootstrap 5 响应式界面
- ✅ 音频列表展示（卡片式布局）
- ✅ 在线音频播放器（可视化效果）
- ✅ 音频下载功能
- ✅ OSS 音频流代理播放
- ✅ 音量控制、进度条拖动
- ✅ 前进/后退 10 秒快捷操作

## 🎵 音频内容

网站包含 5 个音频文件：

| 部分 | 内容 | 时长 | 大小 |
|------|------|------|------|
| Part 1 | 开场白 | ~1.5 分钟 | 1.4 MB |
| Part 2 | 基本概念与总体审核原则 | ~5 分钟 | 4.8 MB |
| Part 3 | 事务功能审核规则 | ~12 分钟 | 12.0 MB |
| Part 4 | 数据功能审核规则 | ~7 分钟 | 7.1 MB |
| Part 5 | 典型案例与常见问题 | ~15 分钟 | 15.1 MB |

**音频源**: 阿里云 OSS `meetingweike` bucket
**音色**: CosyVoice 复刻音色

## 🔧 技术栈

- **后端**: Flask 3.x + Flask-SQLAlchemy + Flask-Login
- **前端**: Bootstrap 5 + Bootstrap Icons
- **数据库**: SQLite 3
- **音频存储**: 阿里云 OSS

## 📝 数据库模型

### User 表
- `id`: 主键
- `username`: 用户名
- `password_hash`: 密码哈希

### AudioFile 表
- `id`: 主键
- `title`: 音频标题
- `part_number`: 部分编号
- `description`: 描述
- `oss_url`: OSS 音频链接
- `file_size_mb`: 文件大小(MB)
- `duration_minutes`: 时长(分钟)

## 🐛 调试模式

开发模式已开启 (`debug=True`)，修改代码后自动重载。

## ⚠️ 注意事项

1. 首次运行会自动创建数据库和默认管理员账号
2. 音频数据会自动从 OSS 链接初始化
3. 生产环境请关闭 debug 模式并使用 WSGI 服务器

## 📄 许可证

仅供内部培训使用
