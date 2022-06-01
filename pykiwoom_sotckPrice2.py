from keyword import kwlist
from pykiwoom.kiwoom import *
import pandas as pd
import time


#키움증권 open API+ 접속
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

kospi = kiwoom.GetCodeListByMarket('0') #kospi 종목코드 
kosdaq = kiwoom.GetCodeListByMarket('10') # kosdaq 종목코드

#kospi 종목이름
# kospi_name = []
# for i in kospi:
#     kospi_name.append(kiwoom.GetMasterCodeName(i))

today=time.strftime("%Y%m%d", time.gmtime(time.time()))
print(today)

priceData = {}
priceData["date"] = (today,)
# data = kiwoom.block_request("opt10081", 종목코드=kospi[0], 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)
# print(priceData['date'][-1], data['일자'].min())

for i in kospi:
    s = kiwoom.GetConnectState()
    if s == 0 :
        break
    
    data = kiwoom.block_request("opt10081", 종목코드=i, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=0)

    if (priceData["date"][-1] < data["일자"].min()) :
        priceData["date"]=data["일자"]

    priceData[i]=data["현재가"]

    while kiwoom.tr_remained:
        s = kiwoom.GetConnectState()
        print(s, i)
        data = kiwoom.block_request("opt10081", 종목코드=i, 기준일자=today, 수정주가구분=1, output="주식일봉차트조회", next=2)
        
        if (priceData["date"][-1] < data["일자"].min()) :
            priceData["date"]=data["일자"]

        priceData[i]=data["현재가"]

        time.sleep(4.5)

        if s==0 :
            break

df = pd.DataFrame(priceData)
df.to_csv('kospi_price_list')
print("done")

