# -*- coding: utf-8 -*-
# @Time: 2023-1-29 9:01
# @File: tools.py
# @IDE: PyCharm

import time
import random
from lxml import etree
from multiprocessing.dummy import Pool
import pymysql
import platform

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定 chromedriver 的路径，根据操作系统选择对应的文件
    if platform.system() == 'Windows':
        chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')
    else:
        chromedriver_path = os.path.join(current_dir, 'chromedriver')


# city, all_page, spider_code
def lieSpider(key_word, city, all_page):
    """
    主函数，用于启动爬虫
    :param key_word: 搜索关键词
    :param city: 城市名称
    :param all_page: 需要爬取的页数
    """
    city_dict = {'全国': '410', '北京': '010', '上海': '020', '天津': '030', '重庆': '040', '广州': '050020',
                 '深圳': '050090',
                 '苏州': '060080', '南京': '060020', '杭州': '070020', '大连': '210040', '成都': '280020',
                 '武汉': '170020',
                 '西安': '270020'}
    # 生成需要爬取的URL列表
    urls_list = get_urls(key_word, all_page, city_dict.get(city, '410'))  # 默认为全国
    # 使用线程池进行多线程爬取
    pool = Pool(3)  # 创建包含3个线程的线程池，适当增加线程数，但不宜过多以免被封IP
    pool.map(get_pages, urls_list)  # 使用map方法将get_pages函数应用到所有URL
    pool.close()  # 关闭线程池，不再接受新任务
    pool.join()  # 等待所有线程完成

    print("爬虫执行完成")
    print("学生详情：  姓名：白鑫   学号：243303029")

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
    print(f'生成了{len(urls_list)}个URL')
    return urls_list


def get_city():
    """
    抓取城市列表及其对应的代码
    :return: 城市列表，每个元素为[城市名称, 城市代码]
    """
    print('开始抓取城市列表...')
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器界面
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
        # 禁用日志输出
    chrome_options.add_argument('--log-level=3')  # 只显示严重错误
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')

    # 使用 Service 指定 chromedriver 路径
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
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
    print(f'开始爬取: {url}')
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')
    # 反爬虫配置：隐藏自动化特征
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 禁用日志输出
    chrome_options.add_argument('--log-level=3')  # 只显示严重错误
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    
    # 创建浏览器实例
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 获取数据库连接
    conn, cursor = get_mysql()
    
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
                print(f'警告：页面可能异常，已保存到 {debug_file}')
            except Exception:
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
        print(f'提取到的数据: name={len(name)}, salary={len(salary)}, company={len(com_name)}, href={len(href_list)}')

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

        # 插入数据库
        for i in range(min_length):
            sql = """
                INSERT INTO job_data (name, salary, place, education, experience, company, label, scale, href, key_word)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                name[i] if i < len(name) else '',
                salary[i] if i < len(salary) else '',
                address[i] if i < len(address) else '',
                education[i] if i < len(education) else '',
                experience[i] if i < len(experience) else '',
                com_name[i] if i < len(com_name) else '',
                labels[i] if i < len(labels) else '',
                scales[i] if i < len(scales) else '',
                'https://www.liepin.com' + href_list[i] if i < len(href_list) else '',
                key_word
            )
            cursor.execute(sql, values)
        
        # 提交事务
        conn.commit()
        print(f'成功爬取并存储{min_length}条职位信息')
        
        
    except Exception as e:
        print(f'爬取页面失败: {url}, 错误: {e}')
        conn.rollback()  # 回滚事务
    finally:
        # 关闭资源
        cursor.close()
        conn.close()
        driver.quit()





def get_mysql():
    """
    连接MySQL数据库
    :return: 数据库连接和游标
    """
    # 从Django配置中读取数据库连接信息
    # 这里直接使用配置信息，实际项目中应该从settings.py导入
    conn = pymysql.connect(
        host='127.0.0.1',  # 数据库主机地址
        port=3306,  # 数据库端口
        user='root',  # 数据库用户名
        password='20040226Bx/',  # 数据库密码
        database='recommend_job',  # 数据库名称
        charset='utf8mb4'  # 字符集，支持中文和特殊字符
    )
    cursor = conn.cursor()  # 创建游标对象
    return conn, cursor



if __name__ == '__main__':
    lieSpider('java', '北京', '1')
