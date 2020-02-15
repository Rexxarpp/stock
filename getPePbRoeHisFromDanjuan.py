import requests
import json
import os
import csv
import time

def timeStampToStr(timeStamp):
    timeArry = time.localtime(timeStamp)
    timeStr = time.strftime("%Y-%m-%d", timeArry)
    return timeStr

urlBegin = "https://danjuanapp.com/djapi/index_eva/"
urlMid = "_history/"
urlEnd = "?day=all"
stock = [("SPACEVCP", "标普价值"), ("CSIH30269", "红利低波"), ("SH000015", "上证红利"), ("CSI930740", "300红利LV"),
         ("SH000922", "中证红利"), ("CSI931157", "红利成长LV"), ("SH000919", "300价值"), ("SZ399998", "中证煤炭"),
         ("SZ399393", "国证地产"), ("SH000016", "上证50"), ("CSPSADRP", "标普红利"),("CSI930949", "神奇公式"),
         ("SZ399812", "养老产业"), ("SZ399986", "中证银行"), ("HKHSCEI", "国企指数"), ("HSFML25", "香港大盘"),
         ("SH000925", "基本面50"), ("SZ399550", "央视50"), ("HKHSI", "恒生指数"), ("SH000010", "上证180"),
         ("SH000903", "中证100"), ("SH000300", "沪深300"), ("CSI931142", "东证竞争"), ("SPCQVCP", "标普质量"),
         ("SPHCMSHP", "香港中小"), ("SZ399324", "深证红利"), ("SZ399317", "国证A指"),("SZ399701", "基本面60"),
         ("SZ399702", "基本面120"), ("SH000905", "中证500"), ("SZ399001", "深证成指"), ("SZ399975", "证券公司"),
         ("SH000827", "中证环保"), ("SZ399997", "中证白酒"), ("SH000932", "主要消费"), ("SZ399417", "新能源车"),
         ("CSIH11136", "中国互联"), ("CSIH30533", "中概互联50"), ("SH000852", "中证1000"), ("SZ399971", "中证传媒"),
         ("SZ399989", "中证医疗"), ("SZ399967", "中证军工"), ("935600", "MSCI印度"), ("SZ399330", "深证100"),
         ("SP500", "标普500"), ("GDAXI", "德国DAX"), ("SH000989", "全指可选"),
         ("NDX", "纳指100"), ("SZ399396", "食品饮料"), ("SH000978", "医药100"), ("SH000991", "全指医药"),
         ("SZ399610", "TMT50"),("SZ399006", "创业板"), ("SH000993", "全指信息"), ("SH000170", "50AH优选"),
         ("CSI716567", "MSCI中国"),("CSI930782", "500低波"), ("CSI931087", "科技龙头")]
pre = ["pe", "pb", "roe"]
index_growth_begin = "index_eva_"
index_growth_end = "_growths"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

csvFilePathBase = "D:\\stockInfo\\danjuan\\"
if not os.path.exists(csvFilePathBase):
    os.mkdir(csvFilePathBase)

for s in range(len(stock)):
    csvFullPath = csvFilePathBase + stock[s][0] + ".csv"
    textFullPath = csvFilePathBase + stock[s][0] + "_info.txt"
    f_info = open(textFullPath, 'w')
    f_info.write("Stock name:%s.Stock code:%s\n" % (stock[s][0], stock[s][1]))
    data_dict = {}
    for p in range(len(pre)):
        url = urlBegin + pre[p] + urlMid + stock[s][0] + urlEnd
        r = requests.get(url, headers=headers)
        r_dict = json.loads(r.text)
        f_info.write("\n+++++++   %s info++++++++\n" % (pre[p]))
        rtcode = r_dict["result_code"]
        print("rtcode:%d\n"%rtcode)
        f_info.write("rtcode:%d\n" % rtcode)

        index_growth = index_growth_begin + pre[p] + index_growth_end
        data_list = r_dict["data"][index_growth]

        beginTime = int(time.time())
        endTime = 0
        for i in range(len(data_list)):
            timestamp = int(data_list[i]["ts"]/1000)
            if timestamp not in data_dict:
                data_dict[timestamp] = {pre[p]: data_list[i][pre[p]]}
            else:
                data_dict[timestamp][pre[p]] = data_list[i][pre[p]]

            if beginTime > timestamp:
                beginTime = timestamp
            if endTime < timestamp:
                endTime = timestamp
        beginTimeStr = timeStampToStr(beginTime)
        f_info.write("beginTime: %s\n" % beginTimeStr)
        endTimeStr = timeStampToStr(endTime)
        f_info.write("endTime: %s\n" % endTimeStr)


        #图形中的标线值
        if "horizontal_lines" in r_dict["data"]:  #roa数据中没有标线，只有PE pb数据中有
            h_lines_list = r_dict["data"]["horizontal_lines"]
            for i in range(len(h_lines_list)):
                name = h_lines_list[i]["line_name"]
                value = h_lines_list[i]["line_value"]
                print((name, value))
                f_info.write("%s: %s\n" % (name, value))
    f_info.close()

    with open(csvFullPath, 'w', newline='')as f:    # newline=''防止出现空行
        f_csv = csv.writer(f)
        data_list = sorted(data_dict.items(), key=lambda k: k[0])
        for i in range(len(data_list)):
            timeStr = timeStampToStr(data_list[i][0])
            pe = None
            pb = None
            roa = None
            if "pe" in data_list[i][1]:
                pe = data_list[i][1]["pe"]
            if "pb" in data_list[i][1]:
                pb = data_list[i][1]["pb"]
            if "roe" in data_list[i][1]:
                roa = data_list[i][1]["roe"]
            data_list_current = [timeStr, pe, pb, roa]
            f_csv.writerow(data_list_current)
        f.close()


