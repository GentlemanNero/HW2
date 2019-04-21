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
    # 用来传递参数的
    keyvalue = {}
    # 目标网址
    url = 'http://data.stats.gov.cn/easyquery.htm'

    # 头部的填充
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) ' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                            'Version/12.0 Safari/605.1.15'

    # 参数的填充
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0501"}]'
    keyvalue['k1'] = str(gettime())

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

    conn = sqlite3.connect("datax.db")

    c = conn.cursor()
    """
    # using the placeholder
    c.execute("INSERT INTO invest VALUES (?, ?, ?, ?)", (10, 2018, store['2018']['total'], store['2018']['city']))
    # save the changes
    conn.commit()
    """
    # iterate through the records
    for row in c.execute('SELECT year, total, city FROM invest ORDER BY id'):
        print(row)

    # 设置中文字体和负号正常显示
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    # 用于存储数据的列表
    num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 纵坐标值
    num_list2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 纵坐标值

    label_list = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']  # 横坐标刻度显示值
    i = 0
    for row in c.execute('SELECT year, total, city FROM invest ORDER BY id'):
        num_list1[i] = round(row[1],1)
        num_list2[i] = round(row[2],1)
        i = i + 1

    # close the connection with the database
    conn.close()
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    # 编辑第一张统计图
    plt.figure(1)
    plt.sca(ax1)
    x = range(len(label_list))

    rects1 = plt.bar(x, num_list1, width=0.4, alpha=0.8, color='red', label="全社会固定资产投资")
    plt.ylim(220000, 660000)  # y轴取值范围
    plt.ylabel("亿元")
    plt.xticks([index + 0.2 for index in x], label_list, fontsize='6')
    plt.xlabel("年份")
    plt.title("全社会固定资产投资-年份")
    plt.legend()  # 设置题注
    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom", fontsize='8')

    # 编辑第二张统计图
    plt.sca(ax2)
    x = range(len(label_list))

    rects2 = plt.bar(x, num_list2, width=0.4, alpha=0.8, color='red', label="城镇固定资产投资")
    plt.ylim(190000, 650000)  # y轴取值范围
    plt.ylabel("亿元")
    plt.xticks([index + 0.2 for index in x], label_list, fontsize='6')
    plt.xlabel("年份")
    plt.title("城镇固定资产投资-年份")
    plt.legend()  # 设置题注
    # 编辑文本
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom",
                    fontsize='8')

    plt.show()


"""
    # 建立数据库
    c.execute('''CREATE TABLE invest
                  (id int primary key, 
                   year long,
                   total long, 
                   city long)''')

    # save the changes
    conn.commit()

    # close the connection with the database
    conn.close()
"""