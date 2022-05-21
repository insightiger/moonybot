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
kospi_name = []
for i in kospi:
    kospi_name.append(kiwoom.GetMasterCodeName(i))

priceData = []
data = kiwoom.block_request("opt10081", 종목코드="005930", 기준일자="20220521", 수정주가구분=1, output="주식일봉차트조회", next=0)

print(time.localtime)
print(data.head())
priceData.append(data)

while kiwoom.tr_remained:
    data = kiwoom.block_request("opt10081", 종목코드="005930", 기준일자="20220521", 수정주가구분=1, output="주식일봉차트조회", next=2)
    priceData.append(data)
    time.sleep(1)

df = pd.concat(priceData)
df.to_csv('priceData', index=False)
