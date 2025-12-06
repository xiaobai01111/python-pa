# 🎯 职位信息可视化推荐系统

> 基于 Django + daisyUI 的智能职位推荐平台，集成协同过滤算法、数据可视化和职位爬虫功能。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-3.2.8-green.svg)
![daisyUI](https://img.shields.io/badge/daisyUI-4.x-purple.svg)
![License](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)

## 📋 目录

- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [系统截图](#-系统截图)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [数据库设计](#-数据库设计)
- [核心算法](#-核心算法)
- [API接口](#-api接口)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 🎯 智能推荐
- 基于物品的协同过滤算法（Item-Based CF）
- 个性化职位推荐
- 用户求职意向管理

### 🕷️ 数据采集
- 猎聘网职位信息爬虫
- Selenium 自动化采集
- 支持多城市、多关键词

### 📊 数据可视化
- 职位关键字柱形图（ECharts）
- 学历/薪资分布饼图
- 系统资源实时监控

### 👤 用户系统
- 注册/登录（表单验证）
- 密码修改
- 简历投递管理
- 投递记录查询

### 💼 职位管理
- 职位列表（分页、筛选）
- 多条件搜索（薪资、学历、城市）
- 一键投递/取消

### 🎨 现代化 UI
- daisyUI 组件库
- 多主题切换支持
- 响应式设计

---

## 🛠 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.9+ | 编程语言 |
| Django | 3.2.8 | Web框架 |
| PyMySQL | 1.1.0 | MySQL数据库驱动 |
| Selenium | 4.15.2 | 网页自动化工具 |
| lxml | 4.9.3 | HTML/XML解析 |
| NumPy | 2.0.0 | 数值计算 |
| psutil | 5.9.6 | 系统监控 |
| Hypercorn | 0.17.3 | ASGI服务器 (HTTP/2) |
| WhiteNoise | 6.11.0 | 静态文件服务 |

### 前端技术

| 技术 | 说明 |
|------|------|
| daisyUI | Tailwind CSS 组件库 |
| TailwindCSS | 原子化 CSS 框架 |
| Layui | 后台管理 UI 框架 |
| LayuiAdmin | 后台管理模板 |
| ECharts | 数据可视化图表 |
| jQuery | DOM 操作库 |

### 数据库

- **MySQL 8.0** - 关系型数据库

### 开发工具

- **Chrome DevTools** - 前端调试
- **ChromeDriver** - Selenium 自动化

---

## 🖼️ 系统截图

| 控制台 | 职位列表 |
|:---:|:---:|
| 系统监控、数据统计 | 职位搜索、筛选、投递 |

| 职位推荐 | 数据可视化 |
|:---:|:---:|
| 协同过滤推荐 | 学历/薪资分布图 |

---

## 🏗 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端展示层 (daisyUI + Layui)          │
├─────────────────────────────────────────────────────────┤
│  登录注册 │ 职位列表 │ 数据可视化 │ 推荐系统 │ 爬虫管理  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    业务逻辑层 (Django Views)             │
├─────────────────────────────────────────────────────────┤
│  用户管理 │ 职位管理 │ 推荐算法 │ 爬虫服务 │ 数据统计   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    数据访问层 (Django ORM)               │
├─────────────────────────────────────────────────────────┤
│                       MySQL 8.0                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- MySQL 8.0+
- Chrome浏览器（用于爬虫）
- ChromeDriver（与Chrome版本匹配）

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/xiaobai01111/python-pa.git
cd JobRecommend
```

2. **创建虚拟环境**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置数据库**

编辑 `JobRecommend/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recommend_job',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **导入数据库**

```bash
mysql -u root -p < recommend_job.sql
```

6. **运行迁移**

```bash
python manage.py migrate
```

7. **启动服务**

```bash
# HTTP/1.1 模式（开发推荐）
python manage.py runserver

# HTTP/2 模式（需要先生成证书）
python manage.py cert --generate  # 生成自签名证书
python manage.py runserver2       # 启动 HTTP/2 服务器
```

### 管理命令

使用 `python manage.py --help` 查看所有命令，常用命令：

| 命令 | 说明 |
|------|------|
| `runserver` | 启动 HTTP/1.1 开发服务器 |
| `runserver2` | 启动 HTTP/2 开发服务器 (HTTPS) |
| `runserver2 --http1` | 使用 Hypercorn 但不启用 HTTPS |
| `cert --generate` | 生成自签名 SSL 证书 |
| `cert --renew` | 续签 SSL 证书 |
| `cert --info` | 查看证书信息 |

**证书命令示例：**
```bash
python manage.py cert --help           # 查看证书命令帮助
python manage.py cert --generate       # 生成证书（有效期365天）
python manage.py cert -g --days 730    # 生成证书（有效期730天）
python manage.py cert --info           # 查看证书有效期
python manage.py cert --renew          # 续签证书
```

**HTTP/2 服务器命令示例：**
```bash
python manage.py runserver2 --help     # 查看服务器命令帮助
python manage.py runserver2            # 默认 https://127.0.0.1:8000
python manage.py runserver2 8080       # 指定端口
python manage.py runserver2 --http1    # HTTP/1.1 模式（无需证书）
```

8. **访问系统**

打开浏览器访问：`http://127.0.0.1:8000`

---

## 📁 项目结构

```
JobRecommend/
├── job/                          # 主应用目录
│   ├── migrations/               # 数据库迁移文件
│   ├── __init__.py
│   ├── admin.py                  # Django管理后台配置
│   ├── apps.py                   # 应用配置
│   ├── models.py                 # 数据模型定义
│   ├── views.py                  # 视图函数
│   ├── tools.py                  # 爬虫工具
│   ├── job_recommend.py          # 推荐算法
│   ├── chromedriver              # ChromeDriver (Linux)
│   └── chromedriver.exe          # ChromeDriver (Windows)
│
├── JobRecommend/                 # 项目配置目录
│   ├── __init__.py
│   ├── settings.py               # 项目设置
│   ├── urls.py                   # URL路由配置
│   ├── asgi.py                   # ASGI配置
│   └── wsgi.py                   # WSGI配置
│
├── templates/                    # HTML模板
│   ├── base.html                 # 基础模板
│   ├── login.html                # 登录页面
│   ├── register.html             # 注册页面
│   ├── index.html                # 主页
│   ├── welcome.html              # 控制台
│   ├── job_list.html             # 职位列表
│   ├── recommend.html            # 推荐页面
│   ├── send_list.html            # 投递列表
│   ├── spiders.html              # 爬虫管理
│   ├── bar_page.html             # 柱形图
│   ├── salary.html               # 薪资分布
│   ├── edu.html                  # 学历分布
│   ├── expect.html               # 求职意向
│   └── pass_page.html            # 密码修改
│
├── static/                       # 静态文件
│   └── layuiadmin/               # LayuiAdmin资源
│       ├── layui/                # Layui框架
│       ├── lib/                  # 第三方库
│       ├── modules/              # 自定义模块
│       └── style/                # 样式文件
│
├── .venv/                        # 虚拟环境
├── manage.py                     # Django管理脚本
├── requirements.txt              # 项目依赖
├── recommend_job.sql             # 数据库SQL文件
├── .python-version               # Python版本
└── README.md                     # 项目说明文档
```

---

## 💾 数据库设计

### ER图

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  UserList   │         │  SendList   │         │  JobData    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ user_id (PK)│◄───────┤ user_id (FK)│         │ job_id (PK) │
│ user_name   │         │ job_id (FK) ├────────►│ name        │
│user_account │         │ send_id (PK)│         │ salary      │
│ pass_word   │         └─────────────┘         │ place       │
└─────────────┘                                 │ education   │
       │                                        │ experience  │
       │                                        │ company     │
       │                                        │ label       │
       ▼                                        │ scale       │
┌─────────────┐                                │ href        │
│ UserExpect  │                                │ key_word    │
├─────────────┤                                └─────────────┘
│ expect_id   │
│ user_id (FK)│
│ key_word    │
│ place       │
└─────────────┘

┌─────────────┐
│ SpiderInfo  │
├─────────────┤
│ spider_id   │
│ spider_name │
│ count       │
│ page        │
└─────────────┘
```

### 数据表说明

#### 1. user_list（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | INT (PK) | 用户ID |
| user_name | VARCHAR(255) | 用户名称（昵称） |
| user_account | VARCHAR(255) | 用户账号（登录名） |
| pass_word | VARCHAR(255) | 密码 |

#### 2. job_data（职位表）

| 字段 | 类型 | 说明 |
|------|------|------|
| job_id | INT (PK) | 职位ID |
| name | VARCHAR(255) | 职位名称 |
| salary | VARCHAR(255) | 薪资范围 |
| place | VARCHAR(255) | 工作地点 |
| education | VARCHAR(255) | 学历要求 |
| experience | VARCHAR(255) | 工作经验 |
| company | VARCHAR(255) | 公司名称 |
| label | VARCHAR(255) | 职位标签 |
| scale | VARCHAR(255) | 公司规模 |
| href | TEXT | 职位链接 |
| key_word | VARCHAR(255) | 关键词 |

#### 3. send_list（投递记录表）

| 字段 | 类型 | 说明 |
|------|------|------|
| send_id | INT (PK) | 投递ID |
| user_id | INT (FK) | 用户ID |
| job_id | INT (FK) | 职位ID |

#### 4. user_expect（求职意向表）

| 字段 | 类型 | 说明 |
|------|------|------|
| expect_id | INT (PK) | 意向ID |
| user_id | INT (FK) | 用户ID |
| key_word | VARCHAR(255) | 期望职位关键词 |
| place | VARCHAR(255) | 期望工作地点 |

#### 5. spider_info（爬虫统计表）

| 字段 | 类型 | 说明 |
|------|------|------|
| spider_id | INT (PK) | 爬虫ID |
| spider_name | VARCHAR(255) | 爬虫名称 |
| count | INT | 运行次数 |
| page | INT | 累计爬取页数 |

---

## 🎯 核心算法

### 协同过滤推荐

基于物品的协同过滤算法（Item-Based CF）：

```python
# 相似度计算
similarity(job1, job2) = |共同投递用户| / √(|job1投递用户| × |job2投递用户|)
```

**推荐流程：**
1. 分析用户投递历史，提取职位关键词
2. 计算未投递职位与已投递职位的相似度
3. 返回相似度最高的 Top-N 职位

---

## 🔌 API接口

### 用户相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/login/` | POST | 用户登录 |
| `/register/` | POST | 用户注册 |
| `/logout/` | GET | 用户登出 |
| `/up_info/` | POST | 修改密码 |

### 职位相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/get_job_list/` | GET | 获取职位列表 |
| `/send_job/` | POST | 投递/取消职位 |
| `/send_list/` | GET | 获取投递列表 |
| `/get_recommend/` | GET | 获取推荐职位 |

### 数据相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/get_pie/` | GET | 获取饼图数据 |
| `/bar/` | GET | 获取柱形图数据 |
| `/get_psutil/` | GET | 获取系统资源 |

### 爬虫相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/start_spider/` | POST | 启动爬虫 |

---

## ❓ 常见问题

### Q1: 爬虫无法运行？

**A:** 检查以下几点：
1. ChromeDriver版本是否与Chrome浏览器匹配
2. ChromeDriver是否有执行权限（Linux需要 `chmod +x`）
3. 网络连接是否正常

### Q2: 数据库连接失败？

**A:** 检查：
1. MySQL服务是否启动
2. 数据库配置是否正确（settings.py）
3. 数据库用户权限是否足够

### Q3: 推荐结果为空？

**A:** 可能原因：
1. 用户没有投递记录
2. 数据库职位数据不足
3. 建议先投递几个职位或设置求职意向

### Q4: 图表不显示？

**A:** 解决方法：
1. 清除浏览器缓存（Ctrl + Shift + F5）
2. 检查静态文件是否正确加载
3. 查看浏览器控制台是否有JavaScript错误

---

## 📝 更新日志

### v2.1.0 (2025-12-07)

- 🚀 **HTTP/2 支持**：新增 Hypercorn ASGI 服务器，支持 HTTP/2 协议
- 🔐 **SSL 证书管理**：`python manage.py cert` 命令管理证书
- 📝 **爬虫日志优化**：实时日志显示，支持 session 隔离
- 🔧 **后台任务**：爬虫改为后台线程运行，提升响应速度
- 📦 **静态文件**：集成 WhiteNoise，支持 ASGI 模式静态文件服务

### v2.0.0 (2025-12-06)

- 🎨 **UI 重构**：全面升级为 daisyUI 组件
- ✨ **多主题支持**：支持亮色/暗色等多种主题切换
- 🔧 **表单验证**：使用 daisyUI Validator 组件
- 📱 **响应式设计**：适配移动端和桌面端
- 🃏 **卡片组件**：职位推荐使用 daisyUI Card
- 📊 **表格优化**：数据表格支持点击展开详情

### v1.0.0 (2024-01-01)

- ✨ 初始版本发布
- ✅ 实现用户注册登录
- ✅ 实现职位爬虫
- ✅ 实现推荐算法
- ✅ 实现数据可视化

---

## 📄 许可证

本项目采用 [GPL-3.0](LICENSE) 许可证。