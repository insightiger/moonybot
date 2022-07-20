import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs



def getCodeList():
    df = pd.read_csv('kospi_list') #코스피 목록 불러오기
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
        df = df.append(pd.read_html(pageReq.text)[0])
    
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

codeList = getCodeList()
data = getStockPrice(codeList[1])
data.to_csv('db/kospi_price_{}'.format(codeList[1]))
print("done")



# for i in stockList:

    #페이지 최대값 구하기
    # maxPage = 655
    # maxPage = source.find_all("table", class_="Nnavi") 
    # mp = maxPage[0].find_all("td", class_="pgRR")
    # mpNum = int(mp[0].a.get('href')[-3:])

    # 각 페이지에서의 작업
    # for currentPage in range(1, maxPage+1):
    #     urlAtPage = 'http://finance.naver.com/item/sise_day.nhn?code=' + i + '&page=' + str(currentPage)
    #     htmlAtPage = urlopen(urlAtPage)
    #     sourceAtPage = BeautifulSoup(htmlAtPage.read(), 'html.parser')
    #     sourceList = sourceAtPage.find_all('tr')
    #     isNone = None

    #     if((currentPage % 1) == 0):
    #         time.sleep(2)
        
    #     for i in range(1, len(sourceList)-1):
    #         if(sourceList[i].span != isNone):
    #             sourceList[i].td.text
    #             print(sourceList[i].find_all('td', align='center')[0].text, sourceList[i].find_all('td', class_='num')[0].text)

