# 从亿牛网获得指数历史PE数据
#b
import requests
import json
import csv
import os

urlBase = "https://eniu.com/chart/peindex/"
stock = [("sh000001", "上证指数"), ("sz399300", "沪深300"),
("sh000016", "上证50"), ("sz399102", "创业板综")]
headers = {'User-Agent':  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/76.0.3809.87 Safari/537.36'}

csvFilePathBase = "D:\\stockInfo"
if not os.path.exists(csvFilePathBase):
    os.mkdir(csvFilePathBase)

for s in range(len(stock)):
    url = urlBase + stock[s][0]
    csVfileName = stock[s][0] + ".csv"
    csvFullPath = os.path.join(csvFilePathBase, csVfileName)

    r = requests.get(url, headers=headers)
    r_dict = json.loads(r.text)

    pe = []

    for i in range(1, len(r_dict['pe'])):
        pe.append((r_dict["date"][i], r_dict["pe"][i]))
    print("名称:%s,数量：%d" % (stock[s][1], len(pe)))

    with open(csvFullPath, 'w', newline='')as f:    # newline=''防止出现空行
        f_csv = csv.writer(f)
        f_csv.writerows(pe)
