# 🎯 职位信息可视化推荐系统

> 基于 Django + Selenium + K-Means 的智能职位推荐平台，集成协同过滤算法、数据可视化和职位聚类分析。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-3.2.8-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)

---

## 📋 目录

- [功能特性](#-功能特性)
- [系统要求](#-系统要求)
- [快速开始](#-快速开始)
  - [Windows 安装指南](#windows-安装指南)
  - [Linux/macOS 安装指南](#linuxmacos-安装指南)
- [项目结构](#-项目结构)
- [使用说明](#-使用说明)
- [常见问题](#-常见问题)
- [技术栈](#-技术栈)

---

## ✨ 功能特性

### 🎯 智能推荐系统
- **五层混合推荐策略**：热门启动、意向匹配、协同过滤、混合加权、全局热门
- **协同过滤算法**：基于物品的 Item-Based CF
- **个性化推荐**：根据用户投递历史和求职意向

### 📊 数据分析与建模
- **K-Means 职位聚类**：自动发现职位类别（高薪技术岗、管理岗、初级岗等）
- **数据可视化**：学历分布、薪资分析、地域分布、技能需求、聚类结果
- **Jupyter Notebook**：完整的数据分析报告（6章结构）

### 🕷️ 智能数据采集
- **Selenium 自动化爬虫**：支持猎聘网职位数据采集
- **反爬虫策略**：User-Agent 伪装、随机延时、自动化特征隐藏
- **多线程并发**：线程池技术提升采集效率
- **自动去重**：基于 (职位名, 公司名, 地点) 联合唯一键

### � 用户系统
- 注册/登录（表单验证）
- 简历投递管理
- 投递记录查询
- 求职意向设置

### 🎨 现代化 UI
- daisyUI 组件库
- 多主题切换（Dark/Light）
- 响应式设计

---

## � 系统要求

### 必需软件

| 软件 | 版本要求 | 说明 |
|------|---------|------|
| **Python** | 3.9 或更高 | 编程语言 |
| **MySQL** | 5.7+ 或 8.0+ | 数据库 |
| **Chrome 浏览器** | 最新版 | 爬虫需要 |
| **ChromeDriver** | 与Chrome版本匹配 | Selenium驱动 |

### Windows 特别要求
- **Microsoft Visual C++ 14.0+**（某些包需要）
- **Git for Windows**（可选，用于克隆项目）

### 推荐配置
- **内存**：4GB 以上
- **硬盘**：1GB 可用空间
- **网络**：稳定的互联网连接

---

## � 快速开始

### Windows 安装指南

#### 步骤 1: 安装 Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.9 或更高版本
3. 安装时**勾选** "Add Python to PATH"
4. 验证安装：
```cmd
python --version
pip --version
```

#### 步骤 2: 安装 MySQL

1. 下载 [MySQL Installer](https://dev.mysql.com/downloads/installer/)
2. 选择 "MySQL Server" 和 "MySQL Workbench"
3. 安装过程中设置 root 密码（记住此密码）
4. 创建数据库：
```sql
CREATE DATABASE job_recommend CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 步骤 3: 安装 Chrome 和 ChromeDriver

1. 安装 [Google Chrome](https://www.google.com/chrome/)
2. 查看 Chrome 版本：`chrome://version/`
3. 下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/downloads)
4. 将 `chromedriver.exe` 放到项目的 `job/` 目录下

#### 步骤 4: 克隆项目

```cmd
git clone https://github.com/xiaobai01111/python-pa.git
cd python-pa
```

或直接下载 ZIP 并解压。

#### 步骤 5: 创建虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 步骤 6: 安装依赖

```cmd
pip install -r requirements.txt
```

**常见问题：**
- 如果遇到 `error: Microsoft Visual C++ 14.0 is required`
  - 下载安装 [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- 如果 `lxml` 安装失败：
  ```cmd
  pip install lxml --only-binary :all:
  ```

#### 步骤 7: 配置数据库

编辑 `JobRecommend/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'job_recommend',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',  # 修改这里
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 步骤 8: 初始化数据库

```cmd
python manage.py makemigrations
python manage.py migrate
```

#### 步骤 9: 运行项目

```cmd
python manage.py runserver
```

访问：http://127.0.0.1:8000

#### 步骤 10: 运行 Jupyter Notebook（可选）

```cmd
jupyter lab
```

打开 `analysis.ipynb` 查看数据分析报告。

---

### Linux/macOS 安装指南

#### 快速安装

```bash
# 1. 克隆项目
git clone https://github.com/xiaobai01111/python-pa.git
cd python-pa

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库（修改 settings.py）
# 5. 初始化数据库
python manage.py makemigrations
python manage.py migrate

# 6. 运行项目
python manage.py runserver
```

---

## 📁 项目结构

```
python-pa/
├── job/                      # 核心应用
│   ├── models.py            # 数据模型（JobData, UserExpect, SendList）
│   ├── views.py             # 视图函数
│   ├── tools.py             # 爬虫工具（lieSpider）
│   └── chromedriver.exe     # ChromeDriver（Windows）
├── JobRecommend/            # Django 项目配置
│   ├── settings.py          # 配置文件
│   └── urls.py              # 路由配置
├── templates/               # HTML 模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   └── welcome.html         # 欢迎页
├── static/                  # 静态文件
│   └── layuiadmin/          # Layui 框架
├── data/                    # 数据目录
│   └── job_data_*.csv       # 爬虫导出的CSV文件
├── analysis.ipynb           # 数据分析报告（Jupyter）
├── requirements.txt         # Python 依赖
└── README.md               # 本文件
```

---

## � 使用说明

### 1. 运行爬虫采集数据

在 Django Shell 或 Jupyter Notebook 中：

```python
from job.tools import lieSpider

# 采集数据：关键词、城市、页数
lieSpider('Python', '北京', '2')
```

**输出：**
- 数据库：`job_jobdata` 表
- CSV 文件：`data/job_data_Python_北京_20251221_*.csv`

### 2. 查看数据分析

打开 `analysis.ipynb`，运行所有单元格：

**章节内容：**
1. 项目概述与环境配置
2. 数据采集（爬虫演示）
3. 数据处理（清洗与去重验证）
4. 智能分析（推荐算法 + K-Means 聚类）
5. 数据可视化
6. 总结与展望

### 3. 使用推荐系统

1. 访问 http://127.0.0.1:8000
2. 注册/登录账号
3. 设置求职意向
4. 浏览职位并投递
5. 查看个性化推荐

---

## ❓ 常见问题

### Windows 平台

**Q: 安装依赖时报错 "Microsoft Visual C++ 14.0 is required"**

A: 安装 [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

**Q: ChromeDriver 报错 "chromedriver.exe is not found"**

A: 
1. 下载与 Chrome 版本匹配的 ChromeDriver
2. 放到 `job/chromedriver.exe`
3. 或添加到系统 PATH

**Q: MySQL 连接失败**

A: 
1. 确认 MySQL 服务已启动
2. 检查 `settings.py` 中的密码
3. 确认数据库 `job_recommend` 已创建

### 通用问题

**Q: 爬虫无法运行**

A: 
1. 检查 Chrome 和 ChromeDriver 版本是否匹配
2. 确认网络连接正常
3. 查看 `log/spider_*.log` 日志

**Q: Jupyter Notebook 中文显示乱码**

A: 
- Windows: 安装中文字体或使用英文标签
- 已在代码中处理，使用默认字体

**Q: 数据库迁移失败**

A:
```bash
# 删除迁移文件
rm -rf job/migrations/
# 重新创建
python manage.py makemigrations job
python manage.py migrate
```

---

## 🛠 技术栈

### 后端
- **Django 3.2.8** - Web 框架
- **PyMySQL 1.1.0** - MySQL 驱动
- **Selenium 4.15.2** - 自动化爬虫
- **Hypercorn 0.17.3** - ASGI 服务器（HTTP/2）

### 数据分析
- **pandas 2.0+** - 数据处理
- **numpy 2.0** - 数值计算
- **scikit-learn 1.3+** - 机器学习（K-Means）
- **matplotlib 3.7+** - 数据可视化
- **seaborn 0.12+** - 统计图表

### 前端
- **daisyUI 4.x** - UI 组件库
- **Tailwind CSS** - CSS 框架
- **Layui** - 后台管理框架
- **ECharts** - 图表库

---

## 📝 更新日志

### v2.0.0 (2025-12-21)
- ✨ 新增 K-Means 职位聚类分析
- ✨ 新增 CSV 数据导出功能
- � 重构 Jupyter Notebook（6章结构）
- � 完善数据清洗验证流程
- 🪟 添加 Windows 平台完整支持
- 📖 更新文档和安装指南

### v1.0.0
- 🎉 初始版本发布
- 实现基础推荐系统
- 实现爬虫功能
- 实现数据可视化

---

## � 许可证

本项目采用 GPL-3.0 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 👨‍� 作者

**白鑫**  
学号：243303029

---

## � 致谢

- Django 社区
- daisyUI 团队
- 所有开源贡献者
