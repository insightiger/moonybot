from numpy import outer
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs



def getCodeList():
    df = pd.read_csv('NaverCrawling\db\kospi_list') #코스피 목록 불러오기
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
    for p in range (1, lastPage+1):
        pageUrl = '{}&page={}'.format(url, p) #이렇게 하는 이유는 p가 int인데, pageUrl은 str이라서
        pageReq = requests.get(url=pageUrl, headers= headers)
        dfFromPage = pd.read_html(pageReq.text)[0]
        df = pd.concat([df, dfFromPage])
    
    df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'}) #영문으로 컬럼명 변경
    df['date'] = pd.to_datetime(df['date']) 
    df = df.dropna()
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = \
                            df[['close','diff', 'open', 'high', 'low', 'volume']].astype(int) # int형으로 변경
    df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']] # 컬럼 순서 정렬
    # df = df.sort_values(by = 'date') # 날짜순으로 정렬

    return df

codeList = getCodeList() #주식시장 코드 불러오기

# 작업파일 불러오기
dfOpen = pd.read_csv('NaverCrawling\kospi_openPrice')
dfOpen['date'] = pd.to_datetime(dfOpen['date'])

dfClose = pd.read_csv('NaverCrawling\kospi_closePrice') 
dfClose['date'] = pd.to_datetime(dfClose['date'])

dfLow = pd.read_csv('NaverCrawling\kospi_lowestPrice')
dfLow['date'] = pd.to_datetime(dfLow['date'])

dfHigh = pd.read_csv('NaverCrawling\kospi_highestPrice') 
dfHigh['date'] = pd.to_datetime(dfHigh['date'])

dfVolume = pd.read_csv('NaverCrawling\kospi_volume')
dfVolume['date'] = pd.to_datetime(dfVolume['date'])

exit()

# #맨처음 파일 생성
# rawDf = getStockPrice(codeList[0])
# dfOpen = pd.DataFrame({'date': rawDf['date']})
# dfClose = pd.DataFrame({'date': rawDf['date']})
# dfLow = pd.DataFrame({'date': rawDf['date']})
# dfHigh = pd.DataFrame({'date': rawDf['date']})
# dfVolume = pd.DataFrame({'date': rawDf['date']})


# 이전 작업때 얼마나 작업을 햇었는지 확인
print(len(dfOpen.columns),len(dfClose.columns),len(dfLow.columns),len(dfHigh.columns),len(dfVolume.columns))

currentCodeIndex = min(len(dfOpen.columns), 
                       len(dfClose.columns),
                       len(dfLow.columns),
                       len(dfHigh.columns),
                       len(dfVolume.columns))-1
lastCodeIndex = len(codeList)


x = 0
x = currentCodeIndex
#이전에 끝났던 부분부터 다시 작업 시작
for index in range(currentCodeIndex, lastCodeIndex) :

    print("current trial is:{}, {}/{}".format(codeList[index], x, len(codeList)) )
    rawDf = getStockPrice(codeList[index]) #크롤링으로 해당 종목에 대한 가격 데이터 df
    
    #serise --> dataframe + dateframe
    dfo = pd.DataFrame({'date' : rawDf['date'], "{}".format(codeList[index]) : rawDf['open']})
    dfOpen = pd.merge(dfOpen, dfo, how = 'outer', on='date')

    dfc = pd.DataFrame({'date' : rawDf['date'],"{}".format(codeList[index]) : rawDf['close']})
    dfClose = pd.merge(dfClose, dfc, how = 'outer', on='date') 

    dfl = pd.DataFrame({'date' : rawDf['date'],"{}".format(codeList[index]) : rawDf['low']})
    dfLow = pd.merge(dfLow, dfl, how = 'outer', on='date') 

    dfh = pd.DataFrame({'date' : rawDf['date'],"{}".format(codeList[index]) : rawDf['high']})
    dfHigh = pd.merge(dfHigh, dfh, how = 'outer', on='date') 

    dfv = pd.DataFrame({'date' : rawDf['date'],"{}".format(codeList[index]) : rawDf['volume']})
    dfVolume = pd.merge(dfHigh, dfv, how = 'outer', on='date') 

    dfOpen.to_csv('NaverCrawling\kospi_openPrice')
    dfClose.to_csv('NaverCrawling\kospi_closePrice')
    dfLow.to_csv('NaverCrawling\kospi_lowestPrice')
    dfHigh.to_csv('NaverCrawling\kospi_highestPrice')
    dfVolume.to_csv('NaverCrawling\kospi_volume')
    x = x + 1

# #이건 그냥 시작
# for index in codeList:
#     print("current trial is:{}, {}/{}".format(index, x, len(codeList)) )
#     rawDf = getStockPrice(index) #크롤링으로 해당 종목에 대한 가격 데이터 df
#     #serise --> dataframe + dateframe
#     dfo = pd.DataFrame({'date' : rawDf['date'], "{}".format(index) : rawDf['open']})
#     dfOpen = pd.merge(dfOpen, dfo, how = 'outer', on='date')

#     dfc = pd.DataFrame({'date' : rawDf['date'],"{}".format(index) : rawDf['close']})
#     dfClose = pd.merge(dfClose, dfc, how = 'outer', on='date') 

#     dfl = pd.DataFrame({'date' : rawDf['date'],"{}".format(index) : rawDf['low']})
#     dfLow = pd.merge(dfLow, dfl, how = 'outer', on='date') 

#     dfh = pd.DataFrame({'date' : rawDf['date'],"{}".format(index) : rawDf['high']})
#     dfHigh = pd.merge(dfHigh, dfh, how = 'outer', on='date') 

#     dfv = pd.DataFrame({'date' : rawDf['date'],"{}".format(index) : rawDf['volume']})
#     dfVolume = pd.merge(dfHigh, dfv, how = 'outer', on='date') 

#     dfOpen.to_csv('NaverCrawling\kospi_openPrice')
#     dfClose.to_csv('NaverCrawling\kospi_closePrice')
#     dfLow.to_csv('NaverCrawling\kospi_lowestPrice')
#     dfHigh.to_csv('NaverCrawling\kospi_highestPrice')
#     dfVolume.to_csv('NaverCrawling\kospi_volume')
#     x = x + 1

print("done")
exit()