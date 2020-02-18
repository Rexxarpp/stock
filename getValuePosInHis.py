import csv
import datetime
import os


def xirr(transactions):
    years = [(ta[0] - transactions[0][0]).days / 365.0 for ta in transactions]
    residual = 1
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i, ta in enumerate(transactions):
            residual += ta[1] / pow(guess, years[i])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess-1


# 入参csvFile（文件）：记录指数（基金）历史点数（净值）的文件
# 出参stockDict(字典类型)key:日期datetime.datetime类型，  value:收盘值 float型
# 出参beginEndTime(字典类型)，读取csv文件后得到的记录开始和结束时间
def createOrignDict(csvFile, stockDict, beginEndTime):
    count = 0
    beginEndTime["beginTime"] = datetime.datetime.now()
    beginEndTime["endTime"] = datetime.datetime.strptime('1980-01-01', '%Y-%m-%d')
    with open(csvFile)as f:
        f_csv = csv.reader(f)
        for i, row in enumerate(f_csv):
            if i > 0:
                date_p = datetime.datetime.strptime(row[0], '%Y-%m-%d')
                count = count + 1
                if beginEndTime["beginTime"].__gt__(date_p):  # datetime比较
                    beginEndTime["beginTime"] = date_p
                if beginEndTime["endTime"].__lt__(date_p):
                    beginEndTime["endTime"] = date_p
                stockDict[date_p] = float(row[3])
        f.close()
    print("Total %d Records insert in dictory" % count)


def getHisValueFromCsv(csvFile):
    csv_list = []
    f = open(csvFile, 'r')
    f_csv = csv.reader(f)
    for row in f_csv:
        csv_list.append(row)
    f.close()
    return csv_list #行内容。如果没有此项读出空字符串。例如：['2010-02-15', '', '3.3022', '0.1215']


def getCurrentValue(currentDate, csvList):
    c_value = -1.0
    for row in csvList:
        date_p = datetime.datetime.strptime(row[0], '%Y-%m-%d')
        if currentDate == date_p:
            c_value = float(row[1])
            return c_value
    return c_value   #/没有找到这天


def getValuePosInHis(currentValue, csvList, beginEndDate):
    rtValue = 0.0
    bigNo = 0   #比currentValue大的天数
    equalNo = 0  #与currentValue相等的天数
    smallNo = 0  #比currentValue小的天数
    smallValue = 1000.0 #csv文件中在beginEndDate之间的最小值
    bigValue = -1000.0 #csv文件中在beginEndDate之间的最大值
    for row in (csvList):
        date_p = datetime.datetime.strptime(row[0], '%Y-%m-%d')
        if beginEndDate["begin"] <= date_p and beginEndDate["end"] >= date_p:
            if row[1]: #如果PE值存在(空字符串''转成bool型为False)（row[1]：pe.  row[2]:pb.  row[3]:roe.）
                float_value = float(row[1])
                if float_value < currentValue:
                    smallNo += 1
                elif float_value > currentValue:
                    bigNo += 1
                else:
                    equalNo += 1
                if smallValue > float_value:
                    smallValue = float_value        # 找出区间内的最小值
                if bigValue < float_value:
                    bigValue = float_value          # 找出区间内的最大值
#    print("currentValue:%f" %(currentValue))
#    print("bigNo:%f.equalNo:%f.smallNo:%f" % (bigNo, equalNo, smallNo))
#    print("smallValue:%f.bigValue:%f" % (smallValue, bigValue))
    if currentValue >= smallValue and currentValue <= bigValue:
        rtValue = (float(equalNo)/2 + float(bigNo)) * 100/(equalNo + smallNo + bigNo)
    elif currentValue < smallValue:
        rtValue = 100.0 * (currentValue/smallValue - 1)
        if rtValue < -50.0:
            rtValue = -50.0
    else:
        rtValue = 100.0 * (currentValue/bigValue)
        if rtValue > 200.0:
            rtValue = 200.0
    return rtValue



# 使用今天的估值比例（比历史上百分之多少的时间便宜）来计算今天的仓位，从而得到买入或卖出的数量
# value(float)使用百分数，例如比5%时间便宜，则value = 5
# 返回值：仓位(float)。为百分数。例如仓位5%，则返回5
# x: 贵 <-50----0----100----200-> 便宜
#         |     |    |       |
# y:      0-----5----90-----100
def getPositionFromValuePos(value):
    x = value
    if x < -50:
        y = 0
    elif x < 0:
        y = 0.1 * x + 5
    elif x < 100:
        y = 0.85 * x + 5
    else:
        y = (-50 * x + 5)
    return y


# 模拟投资
def beginInv(beginDate, beginWeekDay, beginTotalMoney, cycleDays, referenceYears, endDate = datetime.datetime.now()):
    if beginDate.__lt__(beginEndTime["beginTime"]) or beginDate.__gt__(beginEndTime["endTime"]):
        print("beginData not in range")
        return
    while not (beginDate in outDict):
        beginDate = beginDate + datetime.timedelta(days=1)
    dayDiff = beginWeekDay - (beginDate.weekday() + 1)
    if dayDiff < 0:
        dayDiff = dayDiff + 7
    beginDate = beginDate + datetime.timedelta(days=dayDiff)
    print("Begin inV at date: %s,  week: %d\n" % (beginDate.strftime('%Y-%mmm-%d'), beginDate.weekday() + 1))
    csvFullPath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "out.csv"
    f = open(csvFullPath, 'w', newline='')
    f_csv = csv.writer(f)
    f_csv.writerow(["data", "cashUse", "totalMoneyIn", "pe", "pe%", "totalMoney"])

    # 获得参考日期
    referBeginEndDate = {}
    referBeginEndDate["end"] = beginDate - datetime.timedelta(days=1)
    referBeginEndDate["begin"] = referBeginEndDate["end"] - datetime.timedelta(days=referenceYears*365)

    totalMoney = beginTotalMoney
    totalMoneyIn = 0
    totalNo = 0  # 当前份额
    totalCash = beginTotalMoney

    currentDate = beginDate  # 当前日期
    cashFlow = []
    while currentDate.__lt__(endDate):

        if currentDate not in outDict:
            # print("今天没有开市，取消定投.日期:%s\n" % currentDate.strftime('%Y-%m-%d'))
            currentDate = currentDate + datetime.timedelta(days=cycleDays)
            continue

        currentPrice = outDict[currentDate]
        totalMoneyIn = currentPrice * totalNo
        totalMoney = totalMoneyIn + totalCash
        currentPeValue = getCurrentValue(currentDate, csvList)
        rt = getValuePosInHis(currentPeValue, csvList, referBeginEndDate)
        pos = getPositionFromValuePos(rt)
        cashUse = pos/100 * totalMoney - totalMoneyIn

        cashFlow.append((currentDate.date(), totalMoneyIn))
        print("今天是%s。今天的价格:%f.今天总资金:%f"% (currentDate.strftime('%Y-%m-%d'), currentPrice, totalMoney))
        print("今天的估值为：%f. 今天比历史上%f%%时间便宜" % (currentPeValue, rt))
        print("今天之前舱内金额:%f.舱外金额:%f.仓位:%f%%" % (totalMoneyIn, totalCash, totalMoneyIn * 100/totalMoney))
        print("年化收益率%f%%" % (xirr(cashFlow) * 100))
        print("今天的仓位应该是:%f%%.今天买入:%f\n" % (pos, cashUse))
        f_csv.writerow([currentDate.strftime('%Y-%m-%d'), 0.0 - cashUse, totalMoneyIn,
                        currentPeValue, rt, totalMoney])
        totalNo = totalNo + cashUse/currentPrice
        totalCash = totalCash - cashUse
        currentDate = currentDate + datetime.timedelta(days=cycleDays)
        cashFlow.pop()
        cashFlow.append((currentDate.date(), 0.0 - cashUse))
    f.close()

outDict = {}
beginEndTime = {}
zhishu_csv_file1 = "D:\\stockInfo\\163\\000300.csv"
pe_csv_file1 = "D:\\stockInfo\\danjuan\\SH000300.csv"

createOrignDict(zhishu_csv_file1, outDict, beginEndTime)
csvList = getHisValueFromCsv(pe_csv_file1)

beginDate = datetime.datetime.strptime("2017-10-20", '%Y-%m-%d')
weekday = 3
beginTotalMoney = 20000
refYears = 5
invCycle = 7
beginInv(beginDate, weekday, beginTotalMoney, invCycle, refYears)