import urllib
import time
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup

df = pd.read_csv('kospi_list') #코스피 목록 불러오기
stockList = df['종목코드'].values.tolist() #코스피 종목코드 리스트

for i in stockList:
    url = 'http://finance.naver.com/item/sise_day.nhn?code=' + i
    html = urlopen(url)
    source = BeautifulSoup(html.read(), 'html.parser')
    
    #페이지 최대값 구하기
    maxPage = source.find_all("table", align="center") 
    mp = maxPage[0].find_all("td", class_="pgRR")
    mpNum = int(mp[0].a.get('href')[-3:])

    #각 페이지에서의 작업
    for currentPage in range(1, mpNum+1):
        urlAtPage = 'http://finance.naver.com/item/sise_day.nhn?code=' + i + '&page=' + str(currentPage)
        htmlAtPage = urlopen(urlAtPage)
        sourceAtPage = BeautifulSoup(htmlAtPage.read(), 'html.parser')
        sourceList = sourceAtPage.findAll('tr')
        isNone = None

        if((currentPage % 1) == 0):
            time.sleep(2)
        
        for i in range(1, len(sourceList)-1):
            if(sourceList[i].span != isNone):
                sourceList[i].td.text
                print(sourceList[i].find_all('td', align='center')[0].text, sourceList[i].find_all('td', class_='num')[0].text)

print(stockList)
