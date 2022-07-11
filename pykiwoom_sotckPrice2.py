from keyword import kwlist
from pykiwoom.kiwoom import *
import pandas as pd
import time

today=time.strftime("%Y%m%d", time.gmtime(time.time()))
print(today)

#csv파일 불러오기
try:
    df = pd.read_csv("kospi_price_list")
    priceData = df
    print("csv file loaded")
except:
    df = pd.DataFrame()
    df["date"] = (today, )
    df.to_csv('kospi_price_list')
    priceData = df
    print("csv file created")

#키움증권 open API+ 접속
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

kospi = kiwoom.GetCodeListByMarket('0') #kospi 종목코드 
kosdaq = kiwoom.GetCodeListByMarket('10') # kosdaq 종목코드

# #kospi 종목이름
# kospi_name = []
# for i in kospi:
#     kospi_name.append(kiwoom.GetMasterCodeName(i))

# data = kiwoom.block_request("opt10081", 종목코드=kospi[0], 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)
# print(priceData['date'][-1], data['일자'].min())

for i in kospi:
    s = kiwoom.GetConnectState()
    if s == 0 :
        break
    
    data = kiwoom.block_request("opt10081", 종목코드=i, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)

    if (priceData["date"].min() > int(data["일자"].min())) :
        print("hi")
        s2=priceData["date"]
        print(type(s2), s2)

        for i in data["일자"]:
            if s2.min() > int(i):
                s1=pd.Series([i])
                s2.append(s1, ignore_index=True)
                priceData.update(s2)

    priceData.append(data["현재가"])
    print(priceData)

    while kiwoom.tr_remained:
        s = kiwoom.GetConnectState()
        print(s, i)
        data = kiwoom.block_request("opt10081", 종목코드=i, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=2)
        
        if (priceData["date"].min() > int(data["일자"].min())) :
            for i in data["일자"]:
                if priceData["date"].min() > int(i):
                    priceData["date"].append(i)

        priceData.append = data["현재가"]
        df.to_csv('kospi_price_list')
        print("updated")
        time.sleep(2)
        if s==0 :
            break

df.to_csv('kospi_price_list')
print("done")

