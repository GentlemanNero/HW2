import requests
import time
import sqlite3
import json
import matplotlib.pyplot as plt
import matplotlib

# 用来获取 时间戳
def gettime():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    # 用来自定义头部
    headers = {}
    # 用来传递参数
    keyvalue = {}
    # 目标网址
    url = 'http://data.stats.gov.cn/easyquery.htm'

    # 头部的填充
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) ' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                            'Version/12.0 Safari/605.1.15'

    # 下面是参数的填充
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = str(gettime())

    # 发出请求，使用get方法，这里使用我们自定义的头部和参数
    # r = requests.get(url, headers=headers, params=keyvalue)
    # 建立一个Session
    s = requests.session()
    # 在Session基础上进行一次请求
    r = s.post(url, params=keyvalue, headers=headers)
    # 打印返回过来的状态码
    print(r.status_code)
    # 修改dfwds字段内容
    keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"2018"}]'
    # 再次进行请求
    r = s.post(url, params=keyvalue, headers=headers)

    #用于获取数据存入数据库
    store={'0':0}
    text = json.loads(r.text)
    total=text['returndata']['datanodes'][0]['data']['data']
    male=text['returndata']['datanodes'][1]['data']['data']
    female=text['returndata']['datanodes'][2]['data']['data']
    store['2018'] = {'total':total, 'male':male, 'female':female}


    #数据库
    conn = sqlite3.connect("data.db")

    c = conn.cursor()

    for row in c.execute('SELECT year, total, male, female FROM numbers ORDER BY id'):
        print(row[1])

"""
    # 建立数据库
    c.execute('''CREATE TABLE year
          (id int primary key, year int)''')
    c.execute('''CREATE TABLE numbers
          (id int primary key, 
           year int,
           total int, 
           male int, 
           female int)''')

    # save the changes
    conn.commit()

    # close the connection with the database
    conn.close()
"""


# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
#用于存储数据的列表
num_list1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]      # 纵坐标值
num_list2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]      # 纵坐标值
num_list3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]      # 纵坐标值


label_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006','2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014','2015', '2016', '2017', '2018']    # 横坐标刻度显示值
i=0
for row in c.execute('SELECT year, total, male, female FROM numbers ORDER BY id'):
    num_list1[i] = row[1]
    num_list2[i] = row[2]/row[1]
    num_list3[i] = row[3]/row[1]
    i = i + 1


ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

#编辑第一张统计图
plt.figure(1)
plt.sca(ax1)
x = range(len(num_list1))
rects1 = plt.bar(x, num_list1, width=0.4, alpha=0.8, color='red', label="年末总人口")
plt.ylim(120000, 150000)     # y轴取值范围
plt.ylabel("人口数/千万")
plt.xticks([index + 0.2 for index in x], label_list, fontsize='6')
plt.xlabel("年份")
plt.title("年末总人口-年份")
plt.legend()     # 设置题注
# 编辑文本
for rect in rects1:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom",fontsize='8')

#编辑第二张统计图
plt.sca(ax2)
x = range(len(label_list))
plt.plot(x,num_list2,'b')
plt.plot(x,num_list3,'r')
plt.ylim(0.48, 0.52)     # y轴取值范围
plt.ylabel("人口数/千万")
plt.xticks([index + 0.2 for index in x], label_list,fontsize='6')
plt.xlabel("年份")
plt.title("性别人口比例-年份")
plt.legend(['男性人口比例', '女性人口比例'], fontsize='8')     # 设置题注



plt.show()
