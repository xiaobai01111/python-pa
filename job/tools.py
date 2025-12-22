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
import csv

import os
from selenium import webdriver

# Django ORM 支持
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobRecommend.settings")
import django
django.setup()
from job import models
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
            # 日志文件目录
            self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')
            os.makedirs(self.log_dir, exist_ok=True)
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
            # 写入日志文件
            self._write_to_file(timestamp, level, message)
        # 同时打印到控制台
        print(f"[{timestamp}] [{level}] {message}")
    
    def _write_to_file(self, timestamp, level, message):
        """将日志写入文件"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.log_dir, f'spider_{date_str}.log')
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{level}] {message}\n")
        except (IOError, OSError):
            pass  # 写入失败不影响主流程
    
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
# 全局变量用于收集爬取的数据
_collected_job_data = []
_data_lock = threading.Lock()

def lieSpider(key_word, city, all_page):
    """
    主函数，用于启动爬虫
    :param key_word: 搜索关键词
    :param city: 城市名称
    :param all_page: 需要爬取的页数
    """
    global _collected_job_data
    _collected_job_data = []  # 重置数据收集列表
    
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
    
    spider_logger.info(f"开始多线程爬取，线程池大小: 4")
    # 使用线程池进行多线程爬取
    pool = Pool(4)  # 创建包含3个线程的线程池，适当增加线程数，但不宜过多以免被封IP
    pool.map(get_pages, urls_list)  # 使用map方法将get_pages函数应用到所有URL
    pool.close()  # 关闭线程池，不再接受新任务
    pool.join()  # 等待所有线程完成
    # 导出数据到CSV
    if _collected_job_data: 
        csv_filename = export_to_csv(_collected_job_data, key_word, city)
        spider_logger.success(f"数据已导出到CSV: {csv_filename}")
    
    spider_logger.success("========== 爬虫任务完成 ==========")
    spider_logger.log("学生详情: 姓名：白鑫  学号：243303029", 'INFO', private=True)
    spider_logger.set_running(False)
    spider_logger.end_session()  # 结束当前会话，前端将获取到新 session_id
    return 0  # 返回0表示爬虫完成，重置状态

def export_to_csv(job_data_list, keyword, city):
    """
    将爬取的数据导出到CSV文件
    :param job_data_list: 职位数据列表
    :param keyword: 搜索关键词
    :param city: 城市名称
    :return: CSV文件路径
    """
    # 创建data目录
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'job_data_{keyword}_{city}_{timestamp}.csv'
    filepath = os.path.join(data_dir, filename)
    
    # 写入CSV
    if job_data_list:
        fieldnames = job_data_list[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(job_data_list)
        
        spider_logger.info(f"成功导出 {len(job_data_list)} 条数据到 {filename}")
    
    return filepath

def get_urls(key_word, all_page, city_code):
    """
    生成需要爬取的URL列表
    :param key_word: 搜索关键词
    :param all_page: 需要爬取的页数
    :param city_code: 城市代码
    :return: URL列表
    """
    urls_list = []
    # 猎聘网搜索页面URL格式：https://www.liepin.com/zhaopin/?city=城市代码&dqs=城市代码&key=关键词&currentPage=页码
    for page in range(1, int(all_page) + 1):
        url = f'https://www.liepin.com/zhaopin/?city={city_code}&dqs={city_code}&key={key_word}&currentPage={page}'
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
        time.sleep(5)  # 等待页面加载
        
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
    page_num = url.split('currentPage=')[-1] if 'currentPage=' in url else '1'
    spider_logger.info(f'[页面{page_num}] 开始爬取...')
    
    # 创建浏览器实例
    driver = _create_chrome_driver()
    
    try:
        # 添加随机延迟，避免被识别为爬虫
        time.sleep(random.uniform(1, 3))
        
        # 访问URL
        driver.get(url)
        
        # 显式等待：等待职位列表元素出现（最多等待15秒）
        try:
            # 等待职位卡片元素出现
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-nick="job-detail-job-info"]'))
            )
            spider_logger.info(f'[页面{page_num}] 职位列表已加载')
        except TimeoutException:
            spider_logger.warning(f'[页面{page_num}] 等待职位列表超时，尝试继续...')
        
        # 短暂等待确保数据完全渲染
        time.sleep(random.uniform(1, 2))
        
        # 滚动页面以触发懒加载
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))
        
        # 再次等待可能的懒加载内容
        time.sleep(random.uniform(0.5, 1))
        
        # 使用 Selenium DOM 解析职位数据，生成与原逻辑一致的列表结构
        job_links = driver.find_elements(By.XPATH, '//a[@data-nick="job-detail-job-info"]')

        name = []
        salary = []
        address = []
        education = []
        experience = []
        com_name = []
        labels = []
        scales = []
        href_list = []

        for a_el in job_links:
            # href
            href = a_el.get_attribute('href') or ''
            href_list.append(href)

            # 职位名称 ./div[1]/div/div[1]
            try:
                title_el = a_el.find_element(By.XPATH, './div[1]/div/div[1]')
                name.append(title_el.text.strip())
            except Exception:
                name.append('')

            # 地址 ./div[1]/div/div[2]/span[2]
            try:
                addr_el = a_el.find_element(By.XPATH, './div[1]/div/div[2]/span[2]')
                address.append(addr_el.text.strip())
            except Exception:
                address.append('')

            # 薪资 ./div[1]/span[2] 或按 class 兜底
            cur_salary = ''
            try:
                salary_el = a_el.find_element(By.XPATH, './div[1]/span[2]')
                cur_salary = salary_el.text.strip()
            except Exception:
                try:
                    salary_el = a_el.find_element(By.XPATH, './/span[contains(@class,"E8PWS")]')
                    cur_salary = salary_el.text.strip()
                except Exception:
                    cur_salary = ''
            salary.append(cur_salary)

            # 经验 ./div[2]/span[1]
            try:
                exp_el = a_el.find_element(By.XPATH, './div[2]/span[1]')
                experience.append(exp_el.text.strip())
            except Exception:
                experience.append('')

            # 学历 ./div[2]/span[2]
            try:
                edu_el = a_el.find_element(By.XPATH, './div[2]/span[2]')
                education.append(edu_el.text.strip())
            except Exception:
                education.append('')

            # 公司名称：需要从父级元素查找
            # 用户提供的XPath: //*[@id="lp-search-job-box"]/div[3]/section[1]/div[2]/div[1]/div/div[1]/div/div/div/span
            try:
                # 方法1: 从a元素的父级section查找公司信息
                parent_section = a_el.find_element(By.XPATH, './ancestor::section[1]')
                company_el = parent_section.find_element(
                    By.XPATH,
                    './/div[contains(@class, "company")]//span | .//a[contains(@class, "company")]'
                )
                com_name.append((company_el.text or '').strip())
            except Exception:
                try:
                    # 方法2: 从相邻的div查找
                    company_el = a_el.find_element(
                        By.XPATH,
                        './following-sibling::div//span | ./following-sibling::div//a'
                    )
                    text = (company_el.text or '').strip()
                    # 排除非公司名的内容（如行业标签）
                    if text and not any(x in text for x in ['人', '轮', '上市']):
                        com_name.append(text)
                    else:
                        com_name.append('')
                except Exception:
                    com_name.append('')


            # 行业 / 融资 / 人数 → label / scale
            industry = ''
            finance = ''
            headcount = ''
            current_company_name = com_name[-1] if com_name else ''
            try:
                # 方法1: 从父级section查找标签信息
                parent_section = a_el.find_element(By.XPATH, './ancestor::section[1]')
                # 查找包含行业/规模信息的元素
                info_elements = parent_section.find_elements(By.XPATH, './/span[contains(@class, "labels") or contains(@class, "tag") or contains(@class, "info")]')
                
                for el in info_elements:
                    text = (el.text or '').strip()
                    if text and text != current_company_name:
                        # 检查是否是人数
                        if '人' in text and any(c.isdigit() for c in text):
                            headcount = text
                        # 检查是否是融资/上市信息
                        elif any(x in text for x in ['轮', '上市', '融资']):
                            finance = text
                        # 其他作为行业
                        elif not industry:
                            industry = text
            except Exception:
                pass
            
            # 如果上面没找到，尝试从相邻div查找
            if not industry and not headcount:
                try:
                    sibling_div = a_el.find_element(By.XPATH, './following-sibling::div[1]')
                    all_spans = sibling_div.find_elements(By.XPATH, './/span')
                    for span in all_spans:
                        text = (span.text or '').strip()
                        if text and text != current_company_name:
                            if '人' in text and any(c.isdigit() for c in text):
                                headcount = text
                            elif any(x in text for x in ['轮', '上市', '融资']):
                                finance = text
                            elif not industry and len(text) < 20:
                                industry = text
                except Exception:
                    pass

            labels.append(' '.join([x for x in [industry, finance] if x]).strip())
            scales.append(headcount)


        # 调试信息：打印提取到的数据数量
        spider_logger.info(f'[页面{page_num}] 解析数据: 职位={len(name)}, 薪资={len(salary)}, 公司={len(com_name)}')

        # 是否成功爬取
        if len(name) == 0:
            spider_logger.warning(f'[页面{page_num}] 未获取到数据，可能被反爬')
        else:
            spider_logger.success(f'[页面{page_num}] 成功获取 {len(name)} 条职位数据')

        # 确保所有列表长度一致，取最小长度
        min_length = min(
            len(name),
            len(salary),
            len(address),
            len(education),
            len(experience),
            len(com_name),
            len(labels),
            len(scales),
            len(href_list),
        )

        # 从URL中提取关键词
        key_word = url.split('key=')[1].split('&')[0] if 'key=' in url else ''

        # 使用 Django ORM 插入数据库（支持多种数据库，自动去重）
        created_count = 0
        updated_count = 0
        for i in range(min_length):
            raw_href = href_list[i] if i < len(href_list) else ''
            
            # 修复 href：避免重复拼接域名，提取核心路径
            if raw_href.startswith('https://'):
                job_href = raw_href.split('?')[0]  # 去掉查询参数
            elif raw_href.startswith('/'):
                job_href = 'https://www.liepin.com' + raw_href.split('?')[0]
            else:
                job_href = raw_href.split('?')[0] if raw_href else ''
            
            # 提取当前记录的字段值
            job_name = name[i] if i < len(name) else ''
            job_salary = salary[i] if i < len(salary) else ''
            job_place = address[i] if i < len(address) else ''
            job_education = education[i] if i < len(education) else ''
            job_experience = experience[i] if i < len(experience) else ''
            job_company = com_name[i] if i < len(com_name) else ''
            job_label = labels[i] if i < len(labels) else ''
            job_scale = scales[i] if i < len(scales) else ''
            
            # 多重去重判断：职位名 + 公司名 + 工作地点 作为唯一标识
            # 这比仅依赖 href 更可靠
            _, created = models.JobData.objects.update_or_create(
                name=job_name,
                company=job_company,
                place=job_place,
                defaults={
                    'salary': job_salary,
                    'education': job_education,
                    'experience': job_experience,
                    'label': job_label,
                    'scale': job_scale,
                    'href': job_href,
                    'key_word': key_word
                }
            )
            
            # 收集数据到全局列表用于CSV导出
            with _data_lock:
                _collected_job_data.append({
                    'name': job_name,
                    'company': job_company,
                    'place': job_place,
                    'salary': job_salary,
                    'education': job_education,
                    'experience': job_experience,
                    'label': job_label,
                    'scale': job_scale,
                    'href': job_href,
                    'key_word': key_word
                })
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        # 显示去重结果（区分爬取失败和数据重复）
        total = created_count + updated_count
        if min_length == 0:
            # 解析到 0 条数据 = 爬取失败
            pass  # 上面已经有 "未获取到数据" 的警告
        elif updated_count == 0:
            spider_logger.success(f'[页面{page_num}] 存入 {created_count} 条新数据')
        elif created_count == 0:
            spider_logger.info(f'[页面{page_num}] {updated_count} 条数据已存在（全部重复，已更新）')
        else:
            spider_logger.success(f'[页面{page_num}] 新增 {created_count} 条，{updated_count} 条重复已更新')
        
    except Exception as e:
        spider_logger.error(f'[页面{page_num}] 存储失败: {str(e)}')
    finally:
        # 关闭浏览器
        driver.quit()





if __name__ == '__main__':
    lieSpider('java', '北京', '1')
