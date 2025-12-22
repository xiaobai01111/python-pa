from django.shortcuts import render, redirect
from django.http import JsonResponse
from functools import wraps
# Create your views here.
from job import models
import re
import time
from psutil import cpu_percent, virtual_memory
from numpy import mean
from job import tools
from job.tools import spider_logger
from job import job_recommend

spider_code = 0  # 定义全局变量，用来识别爬虫的状态，0空闲，1繁忙


# 登录验证装饰器
def login_required(view_func):
    """检查用户是否已登录，未登录则重定向到登录页"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            # 未登录，重定向到登录页
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# python manage.py inspectdb > job/models.py
# 使用此命令可以将数据库表导入models生成数据模型


def login(request):
    if request.method == "POST":
        user_account = request.POST.get("user")  # 账号
        pass_word = request.POST.get("password")  # 密码
        # 检查用户对象是否存在（使用user_account进行验证）
        user_obj = models.UserList.objects.filter(user_account=user_account, pass_word=pass_word).first()
        if user_obj:
            # 有此用户 -->> 跳转到首页
            # 登录成功后，将user_id和user_name保存到session中
            request.session['user_id'] = user_obj.user_id
            request.session['user_name'] = user_obj.user_name
            return JsonResponse({"code": 0, "msg": "登录成功！", "user_name": user_obj.user_name})
        else:
            return JsonResponse({"code": 1, "msg": "账号或密码错误！"})
    else:
        return render(request, "login.html")



def register(request):
    if request.method == "POST":
        user_account = request.POST.get("user")  # 账号
        pass_word = request.POST.get("password")  # 密码
        repass = request.POST.get("repass")  # 确认密码
        user_name = request.POST.get("user_name")  # 昵称
        
        # 检查账号是否已存在
        user_exists = models.UserList.objects.filter(user_account=user_account).first()
        if user_exists:
            return JsonResponse({"code": 1, "msg": "账号已存在！"})
        
        # 检查两次密码是否一致
        if pass_word != repass:
            return JsonResponse({"code": 1, "msg": "两次密码不一致！"})
        
        # 手动计算新的user_id（获取当前最大的user_id并加1）
        max_user = models.UserList.objects.order_by('-user_id').first()
        if max_user:
            new_user_id = int(max_user.user_id) + 1
        else:
            new_user_id = 1
        
        # 创建新用户，手动指定user_id
        models.UserList.objects.create(
            user_id=new_user_id,
            user_account=user_account,
            user_name=user_name,
            pass_word=pass_word
        )
        return JsonResponse({"code": 0, "msg": "注册成功！"})
    else:
        return render(request, "register.html")
  



# 退出(登出)
def logout(request):
    # 1. 将session中的用户名、昵称删除
    request.session.flush()
    # 2. 重定向到 登录界面
    return redirect('login')


@login_required
def index(request):
    """此函数用于返回主页，主页包括头部，左侧菜单"""
    return render(request, "index.html")


@login_required
def welcome(request):
    """此函数用于处理控制台页面"""
    job_data_queryset = models.JobData.objects.all().values()  # 查询所有的职位信息
    all_job = len(job_data_queryset)  # 职位信息总数
    salary_list = []  # 定义一个空列表
    job_data_list = []
    for job in list(job_data_queryset):  # 使用循环处理最高薪资
        try:  # 使用try...except检验最高薪资的提取，如果提取不到则加入0
            salary_match = re.findall(r'-(\d+)k', job['salary'])
            if salary_match:
                salary_1 = float(salary_match[0])  # 使用正则提取最高薪资
                job['salary_1'] = salary_1  # 添加一个最高薪资
                salary_list.append(salary_1)  # 把最高薪资添加到salary_list用来计算平均薪资
            else:
                job['salary_1'] = 0
                salary_list.append(0)
        except (ValueError, IndexError):
            job['salary_1'] = 0
            salary_list.append(0)
        job_data_list.append(job)
    
    job_data = sorted(job_data_list, key=lambda x: x['salary_1'], reverse=True)  # 反向排序所有职位信息的最高薪资
    job_data_10 = job_data[0:10]  # 取最高薪资前10用来渲染top—10表格
    job_data_1 = job_data[0] if job_data else {}  # 取出最高薪资的职位信息
    mean_salary = int(mean(salary_list)) if salary_list else 0  # 计算平均薪资
    spider_info = models.SpiderInfo.objects.filter(spider_id=1).first()  # 查询爬虫程序运行的数据记录
    
    return render(request, "welcome.html", {
        'all_job': all_job,
        'job_data_10': job_data_10,
        'job_data_1': job_data_1,
        'mean_salary': mean_salary,
        'spider_info': spider_info
    })


@login_required
def spiders(request):
    global spider_code
    spider_code_1 = spider_code
    return render(request, "spiders.html", {'spider_code_1': spider_code_1})


def _run_spider_task(key_word, city, page, role):
    """后台线程运行爬虫任务"""
    global spider_code
    try:
        if role == '猎聘网':
            spider_code = tools.lieSpider(key_word=key_word, city=city, all_page=page)
    except Exception as e:
        spider_logger.error(f"爬虫异常: {str(e)}")
        spider_logger.set_running(False)
        spider_code = 0


@login_required
def start_spider(request):
    global spider_code
    if request.method == "POST":
        # 检查是否已有爬虫在运行
        if spider_logger.is_running:
            return JsonResponse({"code": 1, "msg": "已有爬虫正在运行，请稍后再试"})
        
        # 立即生成新的 session_id，确保前端能获取到最新的
        spider_logger.new_session()
        
        key_word = request.POST.get("key_word")
        city = request.POST.get("city")
        page = request.POST.get("page")
        role = request.POST.get("role")
        spider_code = 1  # 改变爬虫状态
        spider_model = models.SpiderInfo.objects.filter(spider_id=1).first()
        if spider_model:
            spider_model.count += 1  # 给次数+1
            spider_model.page += int(page)  # 给爬取页数加上选择的页数
            spider_model.save()
        
        # 使用线程在后台运行爬虫，让视图立即返回（支持 ASGI 模式）
        import threading
        spider_thread = threading.Thread(
            target=_run_spider_task,
            args=(key_word, city, page, role),
            daemon=True
        )
        spider_thread.start()
        
        return JsonResponse({"code": 0, "msg": "爬虫任务已启动!", "session_id": spider_logger.get_session_id()})
    else:
        return JsonResponse({"code": 1, "msg": "请使用POST请求"})


@login_required
def get_spider_logs(request):
    """获取爬虫日志"""
    since_index = int(request.GET.get('since', 0))
    session_id = request.GET.get('session_id', None)
    logs, total = spider_logger.get_logs(since_index, session_id)
    return JsonResponse({
        "code": 0,
        "logs": logs,
        "total": total,
        "is_running": spider_logger.is_running,
        "session_id": spider_logger.get_session_id()
    })


@login_required
def job_list(request):
    return render(request, "job_list.html")


@login_required
def get_job_list(request):
    """此函数用来渲染职位信息列表"""
    page = int(request.GET.get("page", "1"))  # 获取请求地址中页码
    limit = int(request.GET.get("limit", "10"))  # 获取请求地址中的每页数据数量
    keyword = request.GET.get("keyword", "")
    price_min = request.GET.get("price_min", "")
    price_max = request.GET.get("price_max", "")
    education_filter = request.GET.get("edu", "")
    city = request.GET.get("city", "")
    job_data_list = list(models.JobData.objects.filter(name__icontains=keyword, education__icontains=education_filter,
                                                       place__icontains=city).values())  # 查询所有的职位信息
    job_data = []
    if price_min != "" or price_max != "":
        for job in job_data_list:
            try:
                salary_str = '薪资' + job['salary']
                max_salary_match = re.findall(r'-(\d+)k', salary_str)
                min_salary_match = re.findall(r'薪资(\d+)', salary_str)
                
                if not max_salary_match or not min_salary_match:
                    continue
                    
                max_salary = float(max_salary_match[0])  # 使用正则提取最高薪资
                min_salary = float(min_salary_match[0])  # 使用正则提取最低薪资
                
                if price_min == "" and price_max != "":
                    if max_salary <= float(price_max):
                        job_data.append(job)
                elif price_min != "" and price_max == "":
                    if min_salary >= float(price_min):
                        job_data.append(job)
                else:
                    if min_salary >= float(price_min) and float(price_max) >= max_salary:
                        job_data.append(job)
            except (ValueError, IndexError):  # 如果筛选不出就跳过
                continue
    else:
        job_data = job_data_list
    job_data_1 = job_data[(page - 1) * limit:limit * page]
    for job in job_data_1:
        ret = models.SendList.objects.filter(user_id=request.session.get("user_id"), job_id=job['job_id']).values()
        if ret:
            job['send_key'] = 1
        else:
            job['send_key'] = 0
    
    if len(job_data) == 0 or len(job_data_list) == 0:
        return JsonResponse(
            {"code": 1, "msg": "没找到需要查询的数据！", "count": "{}".format(len(job_data)), "data": job_data_1})
    return JsonResponse({"code": 0, "msg": "success", "count": "{}".format(len(job_data)), "data": job_data_1})


@login_required
def get_psutil(request):
    """此函数用于读取cpu使用率和内存占用率"""
    # cpu_percent()可以获取cpu的使用率，参数interval是获取的间隔
    # virtual_memory()[2]可以获取内存的使用率
    _ = request  # Django视图必需的参数
    return JsonResponse({'cpu_data': cpu_percent(interval=None), 'memory_data': virtual_memory()[2]})


@login_required
def get_pie(request):
    """此函数用于渲染控制台饼图的数据,要求学历的数据和薪资待遇的数据"""
    _ = request  # Django视图必需的参数
    edu_list = ['博士', '硕士', '本科', '大专', '不限']
    edu_data = []
    for education in edu_list:
        edu_count = len(models.JobData.objects.filter(education__icontains=education))  # 使用for循环，查询字段education包含这些学历的职位信息
        edu_data.append({'name': education, "value": edu_count})  # 添加到学历的数据列表中
    
    list_5 = []
    list_10 = []
    list_15 = []
    list_20 = []
    list_30 = []
    list_50 = []
    list_51 = []
    job_data = models.JobData.objects.all().values()  # 查询所有的职位信息
    for job in list(job_data):
        try:
            salary_match = re.findall(r'-(\d+)k', job['salary'])
            if not salary_match:
                continue
            salary_1 = float(salary_match[0])  # 提取薪资待遇的最高薪资要求
            if salary_1 <= 5:  # 小于5K则加入list_5
                list_5.append(salary_1)
            elif 10 >= salary_1 > 5:  # 在5K和10K之间，加入list_10
                list_10.append(salary_1)
            elif 15 >= salary_1 > 10:  # 10K-15K加入list_15
                list_15.append(salary_1)
            elif 20 >= salary_1 > 15:  # 15K-20K加入list_20
                list_20.append(salary_1)
            elif 30 >= salary_1 > 20:  # 20K-30K 加list_30
                list_30.append(salary_1)
            elif 50 >= salary_1 > 30:  # 30K-50K加入list_50
                list_50.append(salary_1)
            elif salary_1 > 50:  # 大于50K加入list_51
                list_51.append(salary_1)
        except (ValueError, IndexError):
            continue
    salary_data = [{'name': '5K及以下', 'value': len(list_5)},  # 生成薪资待遇各个阶段的数据字典，value是里面职位信息的数量
                   {'name': '5-10K', 'value': len(list_10)},
                   {'name': '10K-15K', 'value': len(list_15)},
                   {'name': '15K-20K', 'value': len(list_20)},
                   {'name': '20K-30K', 'value': len(list_30)},
                   {'name': '30-50K', 'value': len(list_50)},
                   {'name': '50K以上', 'value': len(list_51)}]
    
    return JsonResponse({'edu_data': edu_data, 'salary_data': salary_data})


@login_required
def send_job(request):
    """此函数用于投递职位和取消投递"""
    if request.method == "POST":
        user_id = request.session.get("user_id")
        job_id = request.POST.get("job_id")
        send_key = request.POST.get("send_key")
        if int(send_key) == 1:
            models.SendList.objects.filter(user_id=user_id, job_id=job_id).delete()
        else:
            models.SendList.objects.create(user_id=user_id, job_id=job_id)
        return JsonResponse({"Code": 0, "msg": "操作成功"})
    else:
        return JsonResponse({"Code": 1, "msg": "请使用POST请求"})


@login_required
def job_expect(request):
    if request.method == "POST":
        job_name = request.POST.get("key_word")
        city = request.POST.get("city")
        user_expect = models.UserExpect.objects.filter(user=request.session.get("user_id"))
        if user_expect:
            user_expect.update(key_word=job_name, place=city)
        else:
            user_obj = models.UserList.objects.filter(user_id=request.session.get("user_id")).first()
            models.UserExpect.objects.create(user=user_obj, key_word=job_name, place=city)
        return JsonResponse({"Code": 0, "msg": "操作成功"})
    else:
        user_expect_data = models.UserExpect.objects.filter(user=request.session.get("user_id")).values()
        if len(user_expect_data) != 0:
            keyword = user_expect_data[0]['key_word']
            place = user_expect_data[0]['place']
        else:
            keyword = ''
            place = ''
        return render(request, "expect.html", {'keyword': keyword, 'place': place})


@login_required
def get_recommend(request):
    recommend_list = job_recommend.recommend_by_item_id(request.session.get("user_id"), 9)
    return render(request, "recommend.html", {'recommend_list': recommend_list})


@login_required
def send_page(request):
    return render(request, "send_list.html")


@login_required
def send_list(request):
    send_list_data = list(models.JobData.objects.filter(sendlist__user=request.session.get("user_id")).values())
    for send in send_list_data:
        send['send_key'] = 1
    if len(send_list_data) == 0:
        return JsonResponse(
            {"code": 1, "msg": "没找到需要查询的数据！", "count": "{}".format(len(send_list_data)), "data": []})
    else:
        return JsonResponse({"code": 0, "msg": "success", "count": "{}".format(len(send_list_data)), "data": send_list_data})


@login_required
def pass_page(request):
    user_obj = models.UserList.objects.filter(user_id=request.session.get("user_id")).first()
    return render(request, "pass_page.html", {'user_obj': user_obj})

##修改密码
@login_required
def up_info(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        password = request.POST.get("re_password")
        
        user_obj = models.UserList.objects.filter(user_id=request.session.get("user_id")).first()
        
        if not user_obj:
            return JsonResponse({"code": 1, "msg": "用户不存在！"})
        
        # 验证原密码是否正确
        if user_obj.pass_word != old_password:
            return JsonResponse({"code": 1, "msg": "原密码错误！"})
        
        # 验证两次新密码是否一致
        if new_password != password:
            return JsonResponse({"code": 1, "msg": "两次新密码不一致！"})
        
        # 更新密码
        user_obj.pass_word = new_password
        user_obj.save()
        
        return JsonResponse({"code": 0, "msg": "密码修改成功！"})
    else:
        return JsonResponse({"code": 1, "msg": "请使用POST请求"})



@login_required
def salary(request):
    return render(request, "salary.html")


@login_required
def edu(request):
    return render(request, "edu.html")


@login_required
def bar_page(request):
    return render(request, "bar_page.html")


@login_required
def bar(request):
    _ = request  # Django视图必需的参数
    # 获取所有职位的关键词
    key_list = [x['key_word'] for x in list(models.JobData.objects.all().values("key_word")) if x['key_word']]
    
    # 清理关键词：去除末尾的单引号和空格
    cleaned_key_list = []
    for keyword in key_list:
        # 去除末尾的单引号、双引号和空格
        cleaned = keyword.strip().rstrip("'\"")
        cleaned_key_list.append(cleaned)
    
    # 统计每个关键词的数量
    key_word_count = {}
    for keyword in cleaned_key_list:
        key_word_count[keyword] = key_word_count.get(keyword, 0) + 1
    
    # 按数量降序排序
    sorted_keywords = sorted(key_word_count.items(), key=lambda x: x[1], reverse=True)
    
    # 分离关键词和数量
    bar_x = [item[0] for item in sorted_keywords]
    bar_y = [item[1] for item in sorted_keywords]
    
    return JsonResponse({"Code": 0, "bar_x": bar_x, "bar_y": bar_y})
