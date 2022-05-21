from pykiwoom.kiwoom import *
import pandas as pd
import time

#키움증권 open API+ 접속
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

kospi = kiwoom.GetCodeListByMarket('0') #kospi 종목코드 
kosdaq = kiwoom.GetCodeListByMarket('10') # kosdaq 종목코드

data = {}

data["code"]=kospi #kospi 종목코드 담기

#kospi 종목에 따른 종목명 담기
kospi_name = []
for i in kospi:
    kospi_name.append(kiwoom.GetMasterCodeName(i))

data['종목명']=kospi_name

# CSV파일로 저장
# df = pd.DataFrame(data)
# df.to_csv('kospi_list', index=False)
