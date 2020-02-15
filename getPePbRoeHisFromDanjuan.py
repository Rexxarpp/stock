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
stock = [("SH000016", "上证50"), ("SZ399986", "中证银行")]
pre = ["pe", "pb", "roe"]
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

csvFilePathBase = "D:\\stockInfo\\danjuan"
if not os.path.exists(csvFilePathBase):
    os.mkdir(csvFilePathBase)

url = "https://danjuanapp.com/djapi/index_eva/pe_history/SH000016?day=all"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
r = requests.get(url, headers = headers)
r_dict = json.loads(r.text)
print(type(r_dict))

keys = r_dict.keys()
rtcode = r_dict["result_code"]
print("rtcode:%d"%rtcode)

pe_list = r_dict["data"]["index_eva_pe_growths"]
pe_list_new = []
beginTime = int(time.time())
endTime = 0
for i in range(len(pe_list)):
    pe = pe_list[i]["pe"]
    timestamp = int(pe_list[i]["ts"]/1000)
    if beginTime > timestamp:
        beginTime = timestamp
    if endTime < timestamp:
        endTime = timestamp
    timeArry = time.localtime(timestamp)
    timeStr = timeStampToStr(timestamp)
    pe_list_new.append([timeStr, pe])
print (len(pe_list_new))

#图形中的标线值
h_lines_list = r_dict["data"]["horizontal_lines"]
h_lines_list_new = []
for i in range(len(h_lines_list)):
    name = h_lines_list[i]["line_name"]
    value = h_lines_list[i]["line_value"]
    h_lines_list_new.append((name, value))
    print((name, value))

csvFullPath = "D:\\stockInfo\\danjuan\\SH000016_pe.csv"
textFullPath = "D:\\stockInfo\\danjuan\\SH000016_pe_info.txt"
with open(csvFullPath, 'w', newline='')as f:    # newline=''防止出现空行
    f_csv = csv.writer(f)
    f_csv.writerows(pe_list_new)

f_info = open(textFullPath, 'w')
# f_info.write("rtcode")
f_info.write("rtcode: %d\n" % rtcode)

beginTimeStr = timeStampToStr(beginTime)
f_info.write("beginTime: %s\n" % beginTimeStr)

endTimeStr = timeStampToStr(endTime)
f_info.write("endTime: %s\n" % endTimeStr)

for i in range(len(h_lines_list_new)):
    f_info.write("%s: %s\n" % (h_lines_list_new[i][0], h_lines_list_new[i][1]))
f_info.close()

