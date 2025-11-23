# 职位信息可视化推荐系统

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [数据库设计](#数据库设计)
- [核心功能](#核心功能)
- [使用说明](#使用说明)
- [API接口](#api接口)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## ✨ 功能特性

### 🎯 核心功能

- **智能推荐系统**
  - 基于物品的协同过滤算法
  - 个性化职位推荐
  - 用户求职意向管理

- **数据采集**
  - 猎聘网职位信息爬虫
  - 自动化数据采集
  - 爬虫运行统计

- **数据可视化**
  - 职位关键字柱形图
  - 学历分布饼图
  - 薪资分布饼图
  - 系统资源监控（CPU/内存）

- **用户管理**
  - 用户注册/登录
  - 密码修改
  - 简历投递管理
  - 投递记录查询

- **职位管理**
  - 职位列表展示
  - 多条件筛选（薪资、学历、城市）
  - 职位详情查看
  - 一键投递功能

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

### 前端技术

| 技术 | 说明 |
|------|------|
| Layui | UI框架 |
| LayuiAdmin | 后台管理模板 |
| ECharts | 数据可视化 |
| jQuery | JavaScript库 |

### 数据库

- **MySQL 8.0** - 关系型数据库

---

## 🏗 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户界面层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ 登录注册 │  │ 职位列表 │  │ 数据可视化│  │ 推荐系统│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      业务逻辑层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ 用户管理 │  │ 职位管理 │  │ 推荐算法 │  │ 爬虫管理│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      数据访问层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ ORM模型  │  │ 数据查询 │  │ 数据统计 │  │ 数据存储│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      数据库层                            │
│                      MySQL 8.0                           │
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
git clone https://github.com/yourusername/JobRecommend.git
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
python manage.py runserver
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

## 🎯 核心功能

### 1. 智能推荐算法

基于物品的协同过滤算法（Item-Based Collaborative Filtering）

**算法流程：**

```python
def recommend_by_item_id(user_id, top_n=9):
    """
    1. 分析用户投递历史，找出最常投递的3个职位关键词
    2. 计算未投递职位与已投递职位的相似度
    3. 使用余弦相似度计算职位间的相似性
    4. 返回相似度最高的top_n个职位
    """
```

**相似度计算公式：**

```
similarity(job1, job2) = |共同投递用户| / √(|job1投递用户| × |job2投递用户|)
```

### 2. 网络爬虫

**支持平台：** 猎聘网

**爬取内容：**
- 职位名称
- 薪资范围
- 工作地点
- 学历要求
- 工作经验
- 公司信息
- 职位标签

**技术实现：**
- Selenium自动化
- 多线程爬取
- 数据清洗
- 自动去重

### 3. 数据可视化

**图表类型：**

1. **柱形图** - 职位关键字分布
2. **饼图** - 学历要求分布
3. **饼图** - 薪资范围分布
4. **仪表盘** - 系统资源监控

**技术实现：**
- ECharts图表库
- 实时数据更新
- 响应式设计

---

## 📖 使用说明

### 用户操作流程

#### 1. 注册登录

```
访问首页 → 点击注册 → 填写信息 → 登录系统
```

#### 2. 设置求职意向

```
个人中心 → 求职意向 → 填写期望职位和城市 → 保存
```

#### 3. 浏览职位

```
职位列表 → 筛选条件（薪资/学历/城市） → 查看详情 → 投递简历
```

#### 4. 获取推荐

```
推荐页面 → 查看个性化推荐 → 投递感兴趣的职位
```

#### 5. 管理投递

```
投递列表 → 查看已投递职位 → 取消投递
```

### 管理员操作

#### 1. 启动爬虫

```
爬虫管理 → 选择平台（猎聘网） → 设置关键词和城市 → 设置页数 → 启动爬虫
```

#### 2. 查看统计

```
控制台 → 查看爬虫运行统计 → 查看职位数据统计
```

#### 3. 数据可视化

```
数据分析 → 查看各类图表 → 分析职位市场趋势
```

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

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 代码规范

- 遵循PEP 8 Python代码规范
- 添加必要的注释和文档字符串
- 编写单元测试
- 更新相关文档

---

## 📝 更新日志

### v1.0.0 (2024-01-01)

- ✨ 初始版本发布
- ✅ 实现用户注册登录
- ✅ 实现职位爬虫
- ✅ 实现推荐算法
- ✅ 实现数据可视化

---


</div>
