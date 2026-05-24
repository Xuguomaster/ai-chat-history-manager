# AI Chat History Manager

一个用于管理和分析AI对话记录的Web应用，帮助你整理、搜索、分析与各种AI助手的对话记录。

## ✨ 功能特性

- 📝 **对话管理**：导入、存储、分类管理AI对话记录（支持ChatGPT、Claude、文心一言等）
- 🔍 **智能搜索**：全文搜索、标签筛选、来源过滤、时间范围查询
- 📊 **数据分析**：对话统计、趋势图表、来源分布、活跃时段分析
- 🤖 **AI增强**：预留AI接口，支持接入小米Mimo、OpenAI等AI服务
- 🌙 **主题切换**：支持深色/浅色主题
- 📱 **响应式设计**：适配桌面和移动端

## 🛠️ 技术栈

### 后端
- **Python 3.10+**
- **FastAPI** - 高性能Web框架
- **SQLAlchemy** - ORM数据库操作
- **SQLite** - 轻量级数据库

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Element Plus** - Vue 3 UI组件库
- **ECharts** - 数据可视化图表库
- **Axios** - HTTP请求库
- **Vite** - 前端构建工具

## 📁 项目结构

```
ai-chat-history-manager/
├── backend/                    # 后端项目
│   ├── main.py                # FastAPI应用入口
│   ├── database.py            # 数据库配置
│   ├── models.py              # 数据模型
│   ├── schemas.py             # Pydantic模型
│   ├── requirements.txt       # Python依赖
│   ├── routers/               # API路由
│   │   ├── conversations.py   # 对话路由
│   │   ├── messages.py        # 消息路由
│   │   └── stats.py           # 统计路由
│   └── services/              # 业务逻辑
│       ├── conversation_service.py
│       └── message_service.py
├── frontend/                   # 前端项目
│   ├── index.html             # 入口HTML
│   ├── package.json           # Node依赖
│   ├── vite.config.js         # Vite配置
│   └── src/
│       ├── main.js            # Vue入口
│       ├── App.vue            # 根组件
│       ├── api/               # API封装
│       ├── router/            # 路由配置
│       ├── views/             # 页面组件
│       ├── components/        # 通用组件
│       └── styles/            # 全局样式
├── README.md
├── LICENSE
└── .gitignore
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- npm 或 yarn

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

后端启动后访问：
- API服务：http://localhost:8000
- API文档（Swagger）：http://localhost:8000/docs

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问：http://localhost:3000

## 📡 API接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/conversations` | 对话列表（支持分页、筛选） |
| GET | `/api/v1/conversations/search` | 全文搜索 |
| GET | `/api/v1/conversations/{id}` | 对话详情 |
| POST | `/api/v1/conversations` | 创建对话 |
| PUT | `/api/v1/conversations/{id}` | 更新对话 |
| DELETE | `/api/v1/conversations/{id}` | 删除对话 |
| GET | `/api/v1/messages/conversation/{id}` | 消息列表 |
| POST | `/api/v1/messages/conversation/{id}` | 添加消息 |
| POST | `/api/v1/messages/conversation/{id}/batch` | 批量添加消息 |
| GET | `/api/v1/stats` | 统计信息 |
| GET | `/api/v1/health` | 健康检查 |

## 🗺️ 开发路线

- [x] Phase 1: 基础架构搭建
- [x] Phase 2: 后端API开发
- [x] Phase 3: 前端页面开发
- [ ] Phase 4: 对话导入功能（支持JSON/CSV格式）
- [ ] Phase 5: AI增强功能（接入Mimo/OpenAI API）
- [ ] Phase 6: 数据导出功能
- [ ] Phase 7: 用户认证系统

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

[MIT](LICENSE)
