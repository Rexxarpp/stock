import csv

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
    print("Total %d Records insert in dictory" % count)


def getValuePosInHis(currentValue, csvFile, beginEndDate):
    return 50



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
    pass


# 模拟投资
def beginInv(beginDate, beginWeekDay, beginTotalMoney, referenceYears, endDate = datetime.datetime.now()):
    if beginDate.__lt__(beginEndTime["beginTime"]) or beginDate.__gt__(beginEndTime["endTime"]):
        print("beginData not in range")
        return
    while not (beginDate in outDict):
        beginDate = beginDate + datetime.timedelta(days=1)
    dayDiff = beginWeekDay - (beginDate.weekday() + 1)
    if dayDiff < 0:
        dayDiff = dayDiff + 7
    beginDate = beginDate + datetime.timedelta(days=dayDiff)
    print("Begin inV at date: %s,  week: %d\n" % (beginDate.strftime('%Y-%m-%d'), beginDate.weekday() + 1))

    # 获得参考日期
    referBeginEndDate["end"] = beginDate - datetime.timedelta(days=1)
    referBeginEndDate["begin"] = referBeginEndDate["end"] - datetime.timedelta(days=referenceYears*365)

    currentDate = beginDate  # 当前日期

    while currentDate.__lt__(endDate):

        if currentDate not in outDict:
            # print("今天没有开市，取消定投.日期:%s\n" % currentDate.strftime('%Y-%m-%d'))
            currentDate = currentDate + datetime.timedelta(cycleDays)
            continue

        currentPrice = outDict[currentDate]