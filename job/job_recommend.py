#!/usr/bin/python3.9.10
# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 9:41
# @File    : job_recommend.py
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "JobRecommend.settings"
import django

django.setup()
from job import models
from math import sqrt
import operator
from django.db.models import Count
import random


# 计算相似度
def similarity(job1_id, job2_id):
    """计算两个职位之间的相似度（基于投递用户的余弦相似度）"""
    # job1的投递用户数
    job1_users = set(models.SendList.objects.filter(job_id=job1_id).values_list('user_id', flat=True))
    
    # job2的投递用户数
    job2_users = set(models.SendList.objects.filter(job_id=job2_id).values_list('user_id', flat=True))
    
    # 两者的交集
    common_users = job1_users.intersection(job2_users)
    
    # 没有人投递当前职位或没有共同用户
    if len(job1_users) == 0 or len(job2_users) == 0 or len(common_users) == 0:
        return 0
    
    # 余弦计算相似度
    similarity_score = len(common_users) / sqrt(len(job1_users) * len(job2_users))
    return similarity_score


# 基于物品的协同过滤推荐
def recommend_by_item_id(user_id, top_n=9):
    """基于物品的协同过滤推荐算法"""
    # 投递简历最多的前三keyword
    # 先找出用户投过的简历
    send_jobs = models.SendList.objects.filter(user_id=user_id).values_list('job_id', flat=True)
    jobs_id = list(send_jobs)
    
    # 找出用户投递的职位关键字，使用Count进行聚合统计
    # 直接使用Django ORM的Count功能，更高效
    keyword_stats = models.JobData.objects.filter(
        job_id__in=jobs_id,
        key_word__isnull=False
    ).values('key_word').annotate(
        count=Count('key_word')
    ).order_by('-count')[:3]
    
    # 找出最多的3个投递简历的key_word
    user_prefer = [item['key_word'] for item in keyword_stats]
    
    # 如果当前用户没有投递过简历,则看是否选择过意向职位，选过的话，就从意向中找，没选过就随机推荐
    if not user_prefer:
        # 从用户设置的意向中选
        user_expect = models.UserExpect.objects.filter(user_id=user_id).first()
        if user_expect and user_expect.key_word:
            # 或者其他适当的处理方式
            job_list = list(models.JobData.objects.filter(key_word=user_expect.key_word).values())
            random.shuffle(job_list)
            return job_list[:top_n]
        else:
            # 从全部的职位中选
            # 或者其他适当的处理方式
            job_list = list(models.JobData.objects.all().values())
            random.shuffle(job_list)
            return job_list[:top_n]
    
    # 选用户投递简历最多的职位的标签，再随机选择30个没有投递过的简历的职位，计算距离最近
    # 没有投过的简历
    un_send = models.JobData.objects.exclude(job_id__in=jobs_id).values_list('job_id', flat=True)
    un_send = list(un_send)
    
    # 如果未投递的职位太多，随机选择30个进行计算（提高性能）
    if len(un_send) > 30:
        un_send = random.sample(un_send, 30)
    
    # 找出用户投递的职位关键字对应的职位
    send_jobs_with_prefer = models.JobData.objects.filter(
        job_id__in=jobs_id,
        key_word__in=user_prefer
    ).values_list('job_id', flat=True)
    send = list(send_jobs_with_prefer)
    
    # 在未投过的简历的职位中找到相似的职位
    recommend_dict = {}
    for un_send_job_id in un_send:
        similarity_sum = 0
        for send_job_id in send:
            # 计算相似度
            sim = similarity(send_job_id, un_send_job_id)
            similarity_sum += sim
        
        if similarity_sum > 0:
            recommend_dict[un_send_job_id] = similarity_sum
    
    # 按相似度排序
    sorted_recommend = sorted(recommend_dict.items(), key=operator.itemgetter(1), reverse=True)
    
    # 加入相似的职位列表
    recommend_list = []
    for job_id, score in sorted_recommend[:top_n]:
        job = models.JobData.objects.filter(job_id=job_id).values().first()
        if job:
            recommend_list.append(job)
    
    # 如果得不到有效数量的推荐 按照未投递的简历中的职位进行填充
    if len(recommend_list) < top_n:
        # 从用户偏好的关键词中随机选择职位填充
        additional_jobs = models.JobData.objects.filter(
            key_word__in=user_prefer
        ).exclude(
            job_id__in=jobs_id
        ).exclude(
            job_id__in=[job['job_id'] for job in recommend_list]
        ).values()[:top_n - len(recommend_list)]
        
        recommend_list.extend(list(additional_jobs))
    
    return recommend_list


if __name__ == '__main__':
    # similarity(2003, 2008)
    result = recommend_by_item_id(1)
    print(result)
