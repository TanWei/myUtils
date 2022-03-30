#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__= 'tanwei'
 
import json
import jsonpath
import requests
import datetime
import matplotlib.pyplot as plt
import datetime
import numpy as np
 
def get_date_list(days):
    """返回前days天日期列表"""
    date_list = list()
    for i in range(1, days+1):
        day = datetime.datetime.now() - datetime.timedelta(days=i)
        date_to = datetime.datetime(day.year, day.month, day.day).strftime('%Y-%m-%d')
        # date_to = datetime.datetime(day.year, day.month, day.day)
        date_list.append(date_to)
    date_list.reverse()
    return date_list

# def date_range(start_date,end_date):
#     for n in range(int((end_date-start_date).days)):
#         yield start_date+datetime.timedelta(n)
def getTotalByText(text):
    json_text = json.loads(text)
    totals = jsonpath.jsonpath(json_text, "$..total")
    if totals != False:
        total = int(totals[0])
    return total
class huatuoCrashSpider(object):
    """
    爬虫类
    """
    def __init__(self):
        self.path = r"data.xls"
        self.dataurl= \
        r"http://etapi.xesv5.com/bhapi/data/get_crash?page_no=1&page_num=5&timestamp={}&role=204&state={}&offline=3"

    def run(self):
        datas = get_date_list(7)
        
        rates=[]
        total_normal = 0
        totoal_crash = 0;
        for data in datas:            
            url_normal = self.dataurl.format(data, 0)
            url_crash = self.dataurl.format(data, 1)
            
            with requests.get(url_normal) as r1, requests.get(url_crash) as r2:
                if not r1.ok or not r2.ok:
                    print("!!!!!wrong page!!!!!")
                    break
                normal_num = getTotalByText(r1.text)
                total_normal += normal_num
                crash_num = getTotalByText(r2.text)
                totoal_crash += crash_num
                rates.append((crash_num / normal_num) * 100)
        print(total_normal/totoal_crash)
        test(datas, rates, total_normal, totoal_crash)
        
def test(x_, y_, total_normal, totoal_crash):
    ResNet_acc  = y_
    names = x_
    x = range(len(names))
    plt.plot(x, ResNet_acc,  marker='o', mec='#64B5CD',ms=10,  mfc='#64B5CD', c = '#64B5CD')
    plt.title(r"Student client crash rate %")


    plt.xticks(x, names) # 让x轴的刻度以names标签显示


    for i in range(len(ResNet_acc)):
        plt.text(x[i], ResNet_acc[i] - 1, '%s' %round(ResNet_acc[i],3), ha='center', fontsize=10)

    # 调整图与y的边距
    plt.margins(0.05)
    plt.subplots_adjust(bottom=0.15)
    # plt.xlabel(u"Hyperparameter C") #X轴标签
    # plt.ylabel("Accuracy%") #Y轴标签
    plt.yticks(np.arange(0, 15, 1))
    plt.grid(False) # 展示网格
    ax=plt.gca()##获取坐标轴信息,gca=get current axic
    print(ax)
    ax.spines['right'].set_color('none')##设置右边框颜色为无
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')##位置有bottom(left),top(right),both,default,none
    ax.yaxis.set_ticks_position('left')##定义坐标轴是哪个轴，默认为bottom(left)
    ax.spines['bottom'].set_position(('data',0 ))##移动x轴，到y=0
    ax.spines['left'].set_position(('data',-0.5))##还有outward（向外移动），axes（比例移动，后接小数）

    plt.text(x[len(x)-1], 12.5, 'total crash rate: %s%%' %round((totoal_crash/total_normal)*100,3), ha='center', fontsize=10)
    plt.show()
             

if __name__== '__main__':
    spider= huatuoCrashSpider()
    spider.run()
    print("done")