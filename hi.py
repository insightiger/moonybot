from pykiwoom.kiwoom import *
import pandas as pd


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')

data = {}

data["종목코드"]=kospi
kospi_name = []

for i in kospi:
    kospi_name.append(kiwoom.GetMasterCodeName(i))

data['종목명']=kospi_name
df = pd.DataFrame(data)
df.to_csv('kospi_list', index=False)
