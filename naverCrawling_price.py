import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs



def getCodeList():
    df = pd.read_csv('dataset\kospi_list') #코스피 목록 불러오기
    lists = df['종목코드'].values.tolist() #코스피 종목코드 리스트
    return lists

def getStockPrice(code):
    url = 'https://finance.naver.com/item/sise_day.naver?code=' + code #data불러올 웹주소
    headers = {'User-agent': 'Mozilla/5.0'} #★★크롤러가 아닌 웹브라우저에서 접속하는 것처럼 보이기 위한정보
    req = requests.get(url=url, headers=headers) #get방식을 통해 url에 있는 데이터에 접근
    rawData = bs(req.text, 'html.parser')

    pgRR = rawData.find('td', class_='pgRR') #마지막 페이지 정보가 있는 항목에 접근
    lastPage = int(pgRR.a["href"].split("=")[-1]) #마지막페이지 값 추출

    df = pd.DataFrame()
    print(type(df))
    for p in range (1, lastPage+1):
        pageUrl = '{}&page={}'.format(url, p) #이렇게 하는 이유는 p가 int인데, pageUrl은 str이라서
        pageReq = requests.get(url=pageUrl, headers= headers)
        dfFromPage = pd.read_html(pageReq.text)[0]
        df = df.append(dfFromPage)
    
    df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'}) #영문으로 컬럼명 변경
    df['date'] = pd.to_datetime(df['date']) 
    df = df.dropna()
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = \
                            df[['close','diff', 'open', 'high', 'low', 'volume']].astype(int) # int형으로 변경
    df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']] # 컬럼 순서 정렬
    df = df.sort_values(by = 'date') # 날짜순으로 정렬

    df.sort_values(by='date')

    return df

codeList = getCodeList() #주식시장 코드 불러오기

# 작업파일 불러오기
dfOpen = pd.read_csv('kospi_openPrice')
dfClose = pd.read_csv('kospi_closePrice') 
dfLow = pd.read_csv('kospi_lowestPrice')
dfHigh = pd.read_csv('kospi_highestPrice') 
dfVolume = pd.read_csv('kospi_volume')

# #맨터음 파일 생성
# rawDf = getStockPrice(codeList[0])
# dfOpen = pd.DataFrame({'date': rawDf['date']})
# dfClose = pd.DataFrame({'date': rawDf['date']})
# dfLow = pd.DataFrame({'date': rawDf['date']})
# dfHigh = pd.DataFrame({'date': rawDf['date']})
# dfVolume = pd.DataFrame({'date': rawDf['date']})


# 이전 작업때 얼마나 작업을 햇었는지 확인
currentCodeIndex = min(len(dfOpen.columns), 
                       len(dfClose.columns),
                       len(dfLow.columns),
                       len(dfHigh.columns),
                       len(dfVolume.columns))-1
lastCodeIndex = len(codeList)-1


#이전에 끝났던 부분부터 다시 작업 시작
for index in range(currentCodeIndex, 5):
    rawDf = getStockPrice(codeList[index]) #크롤링으로 해당 종목에 대한 가격 데이터 df
    
    # serise + dataframe
    dfOpen[codeList[index]] = rawDf['open']
    dfClose[codeList[index]] = rawDf['close']
    dfLow[codeList[index]] = rawDf['low']
    dfHigh[codeList[index]] = rawDf['high']
    dfVolume[codeList[index]] = rawDf['volume']
    
    #serise --> dataframe + dateframe
    # dfOpenC = pd.concat(dfOpen, rawDf['open'].to_frame())
    # dfCloseC = pd.concat(dfClose, rawDf['close'].to_frame())
    # dfLowC = pd.concat(dfLow, rawDf['low'].to_frame())
    # dfHighC = pd.concat(dfHigh, rawDf['high'].to_frame())
    # dfVolumeC = pd.concat(dfVolume, rawDf['volume'].to_frame())

dfOpen.to_csv('kospi_openPrice')
dfClose.to_csv('kospi_closePrice')
dfLow.to_csv('kospi_lowestPrice')
dfHigh.to_csv('kospi_highestPrice')
dfVolume.to_csv('kospi_volume')

print("done")
