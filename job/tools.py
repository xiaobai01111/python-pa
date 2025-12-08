# -*- coding: utf-8 -*-
# @Time: 2023-1-29 9:01
# @File: tools.py
# @IDE: PyCharm

import time
import random
from lxml import etree
from multiprocessing.dummy import Pool
import platform
import threading
from datetime import datetime

import os
from selenium import webdriver

# Django ORM 支持
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobRecommend.settings")
import django
django.setup()
from job import models
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ========================================
# 爬虫日志系统
# ========================================
class SpiderLogger:
    """爬虫日志记录器"""
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not SpiderLogger._initialized:
            self.logs = []
            self.max_logs = 500  # 最多保存500条日志
            self.is_running = False
            self.session_id = None  # 当前爬取任务的会话ID
            SpiderLogger._initialized = True
    
    def log(self, message, level='INFO', private=False):
        """记录日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = {
            'time': timestamp,
            'level': level,
            'message': message,
            'session_id': self.session_id,  # 记录所属会话
            'private': private  # 私有日志不发送给前端
        }
        with self._lock:
            self.logs.append(log_entry)
            # 保持日志数量在限制内
            if len(self.logs) > self.max_logs:
                self.logs = self.logs[-self.max_logs:]
        # 同时打印到控制台
        print(f"[{timestamp}] [{level}] {message}")
    
    def info(self, message):
        self.log(message, 'INFO')
    
    def success(self, message):
        self.log(message, 'SUCCESS')
    
    def warning(self, message):
        self.log(message, 'WARNING')
    
    def error(self, message):
        self.log(message, 'ERROR')
    
    def get_logs(self, since_index=0, session_id=None):
        """获取从指定索引开始的日志，可按 session_id 过滤，排除私有日志"""
        with self._lock:
            # 先过滤掉私有日志
            public_logs = [log for log in self.logs if not log.get('private', False)]
            
            # 如果指定了 session_id，只返回该会话的日志
            if session_id:
                filtered = [log for log in public_logs if log.get('session_id') == session_id]
                return filtered[since_index:], len(filtered)
            
            # 如果没有指定 session_id，只返回当前会话的日志（如果有的话）
            if self.session_id:
                filtered = [log for log in public_logs if log.get('session_id') == self.session_id]
                return filtered[since_index:], len(filtered)
            
            # 没有当前会话，返回空
            return [], 0
    
    def new_session(self):
        """生成新的会话ID，使用时间戳确保唯一"""
        import time
        self.session_id = str(int(time.time() * 1000))  # 毫秒级时间戳
        return self.session_id
    
    def get_session_id(self):
        """获取当前会话ID"""
        return self.session_id
    
    def end_session(self):
        """结束当前会话，将 session_id 设为 None"""
        self.session_id = None
    
    def clear(self):
        """清空日志"""
        with self._lock:
            self.logs = []
    
    def set_running(self, running):
        """设置爬虫运行状态"""
        self.is_running = running

# 全局日志实例
spider_logger = SpiderLogger()

# 获取当前文件的目录，定义 chromedriver 备用路径
_current_dir = os.path.dirname(os.path.abspath(__file__))
if platform.system() == 'Windows':
    chromedriver_path = os.path.join(_current_dir, 'chromedriver.exe')
else:
    chromedriver_path = os.path.join(_current_dir, 'chromedriver')

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    ChromeDriverManager = None  # 定义为None以避免未定义警告
    USE_WEBDRIVER_MANAGER = False


def _create_chrome_options():
    """创建Chrome浏览器配置选项（公共函数，避免代码重复）"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    # noinspection SpellCheckingInspection
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    # 反爬虫配置：隐藏自动化特征
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 禁用日志输出
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-logging')
    return chrome_options


def _create_chrome_driver():
    """创建Chrome浏览器驱动实例（公共函数，避免代码重复）"""
    chrome_options = _create_chrome_options()
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options)


# city, all_page, spider_code
def lieSpider(key_word, city, all_page):
    """
    主函数，用于启动爬虫
    :param key_word: 搜索关键词
    :param city: 城市名称
    :param all_page: 需要爬取的页数
    """
    spider_logger.set_running(True)
    spider_logger.info("========== 爬虫任务启动 ==========")
    spider_logger.info(f"搜索关键词: {key_word}")
    spider_logger.info(f"目标城市: {city}")
    spider_logger.info(f"爬取页数: {all_page}")
    
    city_dict = {'全国': '410', '北京': '010', '上海': '020', '天津': '030', '重庆': '040', '广州': '050020',
                 '深圳': '050090',
                 '苏州': '060080', '南京': '060020', '杭州': '070020', '大连': '210040', '成都': '280020',
                 '武汉': '170020',
                 '西安': '270020'}
    # 生成需要爬取的URL列表
    urls_list = get_urls(key_word, all_page, city_dict.get(city, '410'))  # 默认为全国
    
    spider_logger.info(f"开始多线程爬取，线程池大小: 3")
    # 使用线程池进行多线程爬取
    pool = Pool(3)  # 创建包含3个线程的线程池，适当增加线程数，但不宜过多以免被封IP
    pool.map(get_pages, urls_list)  # 使用map方法将get_pages函数应用到所有URL
    pool.close()  # 关闭线程池，不再接受新任务
    pool.join()  # 等待所有线程完成

    spider_logger.success("========== 爬虫任务完成 ==========")
    spider_logger.log("学生详情: 姓名：白鑫  学号：243303029", 'INFO', private=True)
    spider_logger.set_running(False)
    spider_logger.end_session()  # 结束当前会话，前端将获取到新 session_id
    return 0  # 返回0表示爬虫完成，重置状态

def get_urls(key_word, all_page, city_code):
    """
    生成需要爬取的URL列表
    :param key_word: 搜索关键词
    :param all_page: 需要爬取的页数
    :param city_code: 城市代码
    :return: URL列表
    """
    urls_list = []
    # 猎聘网搜索页面URL格式：https://www.liepin.com/zhaopin/?city=城市代码&dqs=城市代码&key=关键词&curPage=页码
    for page in range(int(all_page)):
        url = f'https://www.liepin.com/zhaopin/?city={city_code}&dqs={city_code}&key={key_word}&curPage={page}'
        urls_list.append(url)
    spider_logger.info(f'生成待爬取链接数: {len(urls_list)}')
    for i, url in enumerate(urls_list):
        spider_logger.info(f'  链接{i+1}: {url}')
    return urls_list


def get_city():
    """
    抓取城市列表及其对应的代码
    :return: 城市列表，每个元素为[城市名称, 城市代码]
    """
    print('开始抓取城市列表...')
    driver = _create_chrome_driver()
    
    try:
        # 访问猎聘网城市选择页面
        driver.get('https://www.liepin.com/citylist/')
        time.sleep(2)  # 等待页面加载
        
        # 获取页面HTML
        html = driver.page_source
        req_html = etree.HTML(html)
        
        # 提取城市信息（根据实际页面结构调整XPath）
        city_list = []
        # 这里需要根据实际的猎聘网页面结构来编写XPath
        # 示例：提取城市名称和代码
        cities = req_html.xpath('//div[@class="city-list"]//a')
        for city in cities:
            city_name = city.xpath('./text()')[0] if city.xpath('./text()') else ''
            city_code = city.xpath('./@href')[0].split('/')[-1] if city.xpath('./@href') else ''
            if city_name and city_code:
                city_list.append([city_name, city_code])
        
        print(f'成功抓取{len(city_list)}个城市')
        return city_list
    except Exception as e:
        print(f'抓取城市列表失败: {e}')
        return []
    finally:
        driver.quit()  # 关闭浏览器




def get_pages(url):
    """
    爬取单个页面的职位信息并存储到数据库
    :param url: 需要爬取的页面URL
    """
    page_num = url.split('curPage=')[-1] if 'curPage=' in url else '0'
    spider_logger.info(f'[页面{int(page_num)+1}] 开始爬取...')
    
    # 创建浏览器实例
    driver = _create_chrome_driver()
    
    try:
        # 添加随机延迟，避免被识别为爬虫
        time.sleep(random.uniform(1, 3))
        
        # 访问URL
        driver.get(url)
        
        # 随机等待时间，模拟人类行为
        time.sleep(random.uniform(4, 7))
        
        # 滚动页面以触发懒加载
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))
        
        # 获取页面HTML
        html = driver.page_source
        
        # 调试：保存HTML页面（仅在没有数据时保存）
        if '职位' not in html or 'job' not in html.lower():
            page_num = url.split('curPage=')[-1] if 'curPage=' in url else '0'
            debug_file = f'debug_page_{page_num}.html'
            try:
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                spider_logger.warning(f'页面可能异常，已保存调试文件: {debug_file}')
            except (IOError, OSError):
                pass
        
        req_html = etree.HTML(html)

        # 提取职位信息
        name = req_html.xpath('//div[@class="jsx-2387891236 ellipsis-1"]/text()')
        salary = req_html.xpath('//span[@class="jsx-2387891236 job-salary"]/text()')
        address = req_html.xpath('//span[@class="jsx-2387891236 ellipsis-1"]/text()')
        education = req_html.xpath('//div[@class="jsx-2387891236 job-labels-box"]/span[2]/text()')
        experience = req_html.xpath('//div[@class="jsx-2387891236 job-labels-box"]/span[1]/text()')
        com_name = req_html.xpath('//span[@class="jsx-2387891236 company-name ellipsis-1"]/text()')
        tag_list = req_html.xpath('//div[@class="jsx-2387891236 company-tags-box ellipsis-1"]')
        href_list = req_html.xpath('//a[@data-nick="job-detail-job-info"]/@href')
        
        # 调试信息：打印提取到的数据数量
        spider_logger.info(f'[页面{int(page_num)+1}] 解析数据: 职位={len(name)}, 薪资={len(salary)}, 公司={len(com_name)}')
        
        # 是否成功爬取
        if len(name) == 0:
            spider_logger.warning(f'[页面{int(page_num)+1}] 未获取到数据，可能被反爬')
        else:
            spider_logger.success(f'[页面{int(page_num)+1}] 成功获取 {len(name)} 条职位数据')

        # 处理标签信息，将每个职位的标签提取出来并分离label和scale
        labels = []  # 存储行业/融资阶段等标签
        scales = []  # 存储公司规模
        
        for tag_div in tag_list:
            tag_texts = tag_div.xpath('.//span/text()')
            
            # 分离标签和规模
            label_parts = []
            scale_part = ''
            
            for tag in tag_texts:
                # 判断是否是规模信息（包含"人"字或类似模式）
                if '人' in tag or '-' in tag and any(char.isdigit() for char in tag):
                    scale_part = tag
                else:
                    label_parts.append(tag)
            
            labels.append(' '.join(label_parts))  # 将行业等标签用空格连接
            scales.append(scale_part)  # 存储规模信息

        # 确保所有列表长度一致，取最小长度
        min_length = min(len(name), len(salary), len(address), len(education), 
                        len(experience), len(com_name), len(labels), len(scales), len(href_list))
        
        # 从URL中提取关键词
        key_word = url.split('key=')[1].split('&')[0] if 'key=' in url else ''

        # 使用 Django ORM 插入数据库（支持多种数据库，自动去重）
        created_count = 0
        updated_count = 0
        for i in range(min_length):
            job_href = 'https://www.liepin.com' + href_list[i] if i < len(href_list) else ''
            
            # 使用 update_or_create 去重：href 作为唯一标识
            # 如果存在相同 href 的记录则更新，否则创建新记录
            _, created = models.JobData.objects.update_or_create(
                href=job_href,  # 查找条件：职位链接唯一
                defaults={
                    'name': name[i] if i < len(name) else '',
                    'salary': salary[i] if i < len(salary) else '',
                    'place': address[i] if i < len(address) else '',
                    'education': education[i] if i < len(education) else '',
                    'experience': experience[i] if i < len(experience) else '',
                    'company': com_name[i] if i < len(com_name) else '',
                    'label': labels[i] if i < len(labels) else '',
                    'scale': scales[i] if i < len(scales) else '',
                    'key_word': key_word
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        if updated_count > 0:
            spider_logger.success(f'[页面{int(page_num)+1}] 新增 {created_count} 条，更新 {updated_count} 条（已去重）')
        else:
            spider_logger.success(f'[页面{int(page_num)+1}] 成功存入数据库 {created_count} 条记录')
        
    except Exception as e:
        spider_logger.error(f'[页面{int(page_num)+1}] 存储失败: {str(e)}')
    finally:
        # 关闭浏览器
        driver.quit()





if __name__ == '__main__':
    lieSpider('java', '北京', '1')
