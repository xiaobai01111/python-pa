#!/usr/bin/python3.9.10
# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 9:41
# @File    : job_recommend.py
"""
职位推荐算法模块

推荐策略：
- 情况一：无求职意向 + 无投递记录 → 热门推荐
- 情况二：有求职意向 + 无投递记录 → 意向匹配推荐
- 情况三：无求职意向 + 有投递记录 → 协同过滤推荐
- 情况四：有求职意向 + 有投递记录 → 混合推荐
- 情况五：全局热门推荐（所有用户）
"""
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "JobRecommend.settings"
import django

django.setup()
from job import models
from math import sqrt
from django.db.models import Count, Q
import random


# ============================================================
# 基础工具函数
# ============================================================

def similarity(job1_id, job2_id):
    """计算两个职位之间的相似度（基于投递用户的余弦相似度）"""
    job1_users = set(models.SendList.objects.filter(job_id=job1_id).values_list('user_id', flat=True))
    job2_users = set(models.SendList.objects.filter(job_id=job2_id).values_list('user_id', flat=True))
    common_users = job1_users.intersection(job2_users)
    
    if len(job1_users) == 0 or len(job2_users) == 0 or len(common_users) == 0:
        return 0
    
    return len(common_users) / sqrt(len(job1_users) * len(job2_users))


def get_user_send_jobs(user_id):
    """获取用户投递过的职位ID列表"""
    return list(models.SendList.objects.filter(user_id=user_id).values_list('job_id', flat=True))


def get_user_expect(user_id):
    """获取用户求职意向"""
    return models.UserExpect.objects.filter(user_id=user_id).first()


def _build_job_list_from_sorted(sorted_jobs, top_n):
    """从排序后的(job_id, score)列表构建职位信息列表"""
    recommend_list = []
    for job_id, _ in sorted_jobs[:top_n]:
        job_item = models.JobData.objects.filter(job_id=job_id).values().first()
        if job_item:
            recommend_list.append(job_item)
    return recommend_list


def get_user_prefer_keywords(job_ids, limit=3):
    """从投递历史中提取用户偏好的关键词"""
    keyword_stats = models.JobData.objects.filter(
        job_id__in=job_ids,
        key_word__isnull=False
    ).exclude(key_word='').values('key_word').annotate(
        count=Count('key_word')
    ).order_by('-count')[:limit]
    
    return [stat['key_word'] for stat in keyword_stats]


# ============================================================
# 情况一：无求职意向 + 无投递记录 → 热门推荐
# ============================================================

def recommend_case1_hot(top_n=9):
    """
    情况一：冷启动 - 推荐热门职位
    策略：按投递次数排序的热门职位
    """
    # 统计每个职位的投递次数
    hot_jobs = models.JobData.objects.annotate(
        send_count=Count('sendlist')
    ).order_by('-send_count')[:top_n * 3]
    
    job_list = list(hot_jobs.values())
    
    # 如果热门职位不足，用随机职位填充
    if len(job_list) < top_n:
        all_jobs = list(models.JobData.objects.all().values())
        random.shuffle(all_jobs)
        job_list.extend(all_jobs[:top_n - len(job_list)])
    
    # 随机打乱增加多样性
    random.shuffle(job_list)
    return job_list[:top_n]


# ============================================================
# 情况二：有求职意向 + 无投递记录 → 意向匹配推荐
# ============================================================

def recommend_case2_expect(user_expect, top_n=9):
    """
    情况二：有意向无行为 - 意向匹配推荐
    策略：关键词+城市精确匹配 → 关键词模糊匹配 → 城市匹配
    """
    recommend_list = []
    keyword = user_expect.key_word
    place = user_expect.place
    
    # Step1: 关键词 + 城市 完全匹配
    if keyword and place:
        exact_match = models.JobData.objects.filter(
            Q(key_word=keyword) | Q(name__icontains=keyword),
            place__icontains=place
        ).annotate(send_count=Count('sendlist')).order_by('-send_count')
        recommend_list.extend(list(exact_match.values()[:top_n]))
    
    # Step2: 关键词匹配（模糊搜索职位名称）
    if len(recommend_list) < top_n and keyword:
        existing_ids = [j['job_id'] for j in recommend_list]
        keyword_match = models.JobData.objects.filter(
            Q(key_word=keyword) | Q(name__icontains=keyword)
        ).exclude(job_id__in=existing_ids).annotate(
            send_count=Count('sendlist')
        ).order_by('-send_count')
        recommend_list.extend(list(keyword_match.values()[:top_n - len(recommend_list)]))
    
    # Step3: 城市匹配 + 热门排序
    if len(recommend_list) < top_n and place:
        existing_ids = [j['job_id'] for j in recommend_list]
        place_match = models.JobData.objects.filter(
            place__icontains=place
        ).exclude(job_id__in=existing_ids).annotate(
            send_count=Count('sendlist')
        ).order_by('-send_count')
        recommend_list.extend(list(place_match.values()[:top_n - len(recommend_list)]))
    
    # Step4: 不足则用热门填充
    if len(recommend_list) < top_n:
        existing_ids = [j['job_id'] for j in recommend_list]
        hot_fill = recommend_case1_hot(top_n - len(recommend_list))
        for job_item in hot_fill:
            if job_item['job_id'] not in existing_ids:
                recommend_list.append(job_item)
                if len(recommend_list) >= top_n:
                    break
    
    random.shuffle(recommend_list)
    return recommend_list[:top_n]


# ============================================================
# 情况三：无求职意向 + 有投递记录 → 协同过滤推荐
# ============================================================

def recommend_case3_cf(_user_id, send_job_ids, top_n=9):
    """
    情况三：无意向有行为 - 协同过滤推荐
    策略：基于投递历史的 Item-Based CF
    """
    # 提取用户偏好关键词
    user_prefer = get_user_prefer_keywords(send_job_ids)
    
    # 获取未投递的职位
    un_send_query = models.JobData.objects.exclude(job_id__in=send_job_ids)
    un_send_ids = list(un_send_query.values_list('job_id', flat=True))
    random.shuffle(un_send_ids)
    un_send_ids = un_send_ids[:50]  # 限制计算量
    
    # 获取用户投递过的关键词匹配职位
    send_prefer_ids = list(models.JobData.objects.filter(
        job_id__in=send_job_ids,
        key_word__in=user_prefer
    ).values_list('job_id', flat=True))
    
    # 计算相似度
    recommend_dict = {}
    for un_send_id in un_send_ids:
        sim_sum = sum(similarity(send_id, un_send_id) for send_id in send_prefer_ids)
        if sim_sum > 0:
            recommend_dict[un_send_id] = sim_sum
    
    # 按相似度排序
    sorted_jobs = sorted(recommend_dict.items(), key=lambda x: x[1], reverse=True)
    recommend_list = _build_job_list_from_sorted(sorted_jobs, top_n)
    
    # 不足则用相同关键词职位填充
    if len(recommend_list) < top_n and user_prefer:
        existing_ids = [j['job_id'] for j in recommend_list] + send_job_ids
        fill_jobs = models.JobData.objects.filter(
            key_word__in=user_prefer
        ).exclude(job_id__in=existing_ids).values()
        fill_list = list(fill_jobs)
        random.shuffle(fill_list)
        recommend_list.extend(fill_list[:top_n - len(recommend_list)])
    
    random.shuffle(recommend_list)
    return recommend_list[:top_n]


# ============================================================
# 情况四：有求职意向 + 有投递记录 → 混合推荐
# ============================================================

def recommend_case4_hybrid(_user_id, user_expect, send_job_ids, top_n=9):
    """
    情况四：有意向有行为 - 混合推荐
    策略：意向匹配(40%) + 协同过滤(60%)
    """
    keyword = user_expect.key_word
    place = user_expect.place
    user_prefer = get_user_prefer_keywords(send_job_ids)
    
    # 将意向关键词加入偏好（优先级最高）
    if keyword and keyword not in user_prefer:
        user_prefer.insert(0, keyword)
    
    # 获取未投递职位
    un_send_query = models.JobData.objects.exclude(job_id__in=send_job_ids)
    
    # 优先筛选符合城市意向的职位
    if place:
        place_filtered = un_send_query.filter(place__icontains=place)
        if place_filtered.exists():
            un_send_query = place_filtered
    
    un_send_ids = list(un_send_query.values_list('job_id', flat=True))
    random.shuffle(un_send_ids)
    un_send_ids = un_send_ids[:60]
    
    # 计算综合得分
    score_dict = {}
    
    for candidate_id in un_send_ids:
        candidate = models.JobData.objects.filter(job_id=candidate_id).first()
        if not candidate:
            continue
        
        # 意向匹配得分 (40%)
        expect_score = 0
        if keyword and (candidate.key_word == keyword or (candidate.name and keyword in candidate.name)):
            expect_score += 0.3
        if place and candidate.place and place in candidate.place:
            expect_score += 0.1
        
        # 协同过滤得分 (60%)
        cf_score = 0
        send_prefer_ids = list(models.JobData.objects.filter(
            job_id__in=send_job_ids,
            key_word__in=user_prefer
        ).values_list('job_id', flat=True)[:10])
        
        for send_id in send_prefer_ids:
            cf_score += similarity(send_id, candidate_id) * 0.6
        
        total_score = expect_score + cf_score
        if total_score > 0:
            score_dict[candidate_id] = total_score
    
    # 按综合得分排序
    sorted_jobs = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    recommend_list = _build_job_list_from_sorted(sorted_jobs, top_n)
    
    # 不足则用意向匹配填充
    if len(recommend_list) < top_n:
        existing_ids = [j['job_id'] for j in recommend_list] + send_job_ids
        fill_query = models.JobData.objects.filter(
            Q(key_word__in=user_prefer) | Q(name__icontains=keyword) if keyword else Q(key_word__in=user_prefer)
        ).exclude(job_id__in=existing_ids)
        
        if place:
            fill_query = fill_query.filter(place__icontains=place)
        
        fill_list = list(fill_query.values())
        random.shuffle(fill_list)
        recommend_list.extend(fill_list[:top_n - len(recommend_list)])
    
    random.shuffle(recommend_list)
    return recommend_list[:top_n]


# ============================================================
# 情况五：全局热门推荐
# ============================================================

def recommend_case5_global_hot(top_n=9):
    """
    情况五：全局热门推荐
    策略：所有用户的热门职位排行
    """
    hot_jobs = models.JobData.objects.annotate(
        send_count=Count('sendlist')
    ).filter(send_count__gt=0).order_by('-send_count')[:top_n]
    
    job_list = list(hot_jobs.values())
    
    # 热门不足则随机填充
    if len(job_list) < top_n:
        existing_ids = [j['job_id'] for j in job_list]
        fill_jobs = list(models.JobData.objects.exclude(
            job_id__in=existing_ids
        ).values())
        random.shuffle(fill_jobs)
        job_list.extend(fill_jobs[:top_n - len(job_list)])
    
    return job_list[:top_n]


# ============================================================
# 主推荐函数
# ============================================================

def recommend_by_item_id(user_id, top_n=9):
    """
    智能推荐主函数 - 根据用户状态自动选择推荐策略
    
    Args:
        user_id: 用户ID
        top_n: 推荐数量
    
    Returns:
        推荐职位列表
    """
    # 获取用户数据
    send_job_ids = get_user_send_jobs(user_id)
    user_expect = get_user_expect(user_id)
    
    has_expect = user_expect and (user_expect.key_word or user_expect.place)
    has_send = len(send_job_ids) > 0
    
    # 根据情况选择推荐策略
    if not has_expect and not has_send:
        # 情况一：无意向 + 无投递 → 热门推荐
        return recommend_case1_hot(top_n)
    
    elif has_expect and not has_send:
        # 情况二：有意向 + 无投递 → 意向匹配
        return recommend_case2_expect(user_expect, top_n)
    
    elif not has_expect and has_send:
        # 情况三：无意向 + 有投递 → 协同过滤
        return recommend_case3_cf(user_id, send_job_ids, top_n)
    
    else:
        # 情况四：有意向 + 有投递 → 混合推荐
        return recommend_case4_hybrid(user_id, user_expect, send_job_ids, top_n)


def get_global_hot_jobs(top_n=9):
    """
    获取全局热门职位（情况五）
    供管理员或首页展示使用
    """
    return recommend_case5_global_hot(top_n)


if __name__ == '__main__':
    print("=" * 50)
    print("测试推荐算法")
    print("=" * 50)
    
    # 测试用户推荐
    result = recommend_by_item_id(1)
    print(f"\n用户1的推荐结果（{len(result)}条）:")
    for item in result[:3]:
        print(f"  - {item.get('name', 'N/A')} | {item.get('salary', 'N/A')} | {item.get('place', 'N/A')}")
    
    # 测试全局热门
    hot = get_global_hot_jobs(5)
    print(f"\n全局热门职位（{len(hot)}条）:")
    for item in hot:
        print(f"  - {item.get('name', 'N/A')} | {item.get('company', 'N/A')}")
