import requests
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup as bs

def getCodeList():
    df = pd.read_csv('NaverCrawling\db\kospi_list') #코스피 목록 불러오기
    lists = df['종목코드'].values.tolist() #코스피 종목코드 리스트
    print(lists)
    return lists

def updatePriceData(code, delatDay): 
    df = pd.DataFrame() #빈 dataframe 만들기    
    
    for p in range (1, int(deltaDay/10)):
        pageUrl = '{}&page={}'.format(url, p) #이렇게 하는 이유는 p가 int인데, pageUrl은 str이라서
        pageReq = requests.get(url=pageUrl, headers= headers)
        dfPage = pd.read_html(pageReq.text)[0] #페이지의 가격 정보를 dataframe형식으로 전환
        df = pd.concat([df, dfPage]) #하나의 dataframe에 행으로 이어붙이기
        
    #dataframe은 모두 string이기 때문에 자료형 변경
    df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'}) #영문으로 컬럼명 변경
    df['date'] = pd.to_datetime(df['date']) 
    df = df.dropna()
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = \
                            df[['close','diff', 'open', 'high', 'low', 'volume']].astype(int) # int형으로 변경
    df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']] # 컬럼 순서 정렬
    
    return df

codeList = getCodeList() 
dfFile = pd.read_csv("NaverCrawling\db\kospi_closePrice") #파일 로드


#결측일수 구하기
latestDay = dfFile["date"][0]
print("lastdate :" + str(latestDay))
today = datetime.now()
deltaDay = (today-latestDay).days

dfUdpated = pd.DataFrame() #빈 dataframe 만들기

# 각 종목별로 종가를 뽑아서 하나의 dataframe에 합치기 (column기준) 
for code in codeList:
   dfStock = updatePriceData(code, deltaDay) #종목에 대한 가격 정보 가져오기
   dfClose = dfStock["close"].to_frame() #종가만 뽑아오기
   dfUdpated = pd.merge(dfStock, dfClose) #merge매서드로 하나의 dataframe으로 병합

print("Updated", dfUdpated)
dfFile = pd.concat([dfFile, dfUdpated]) #파일데이터에 업데이트데이터 추가
dfFile.to_csv('KOSPI_closePice_up') #저장