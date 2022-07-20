import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3


# 기사 데이터 추출
def crawling(link):
    link_req = requests.get(link).text
    soup = BeautifulSoup(link_req, "html.parser")
    div_title = soup.find("div", class_= "article_info").h3
    div_contents = soup.find("div", class_= "articleCont")
    span = soup.find("span", class_= "article_date")

    id = link.split("article_id=")[1].split("&")[0]
    title = div_title.get_text().strip()
    contents = div_contents.get_text().replace("\t","").replace("\n","").strip()
    date = span.get_text()
    print(id, date, title, contents)
    return (id, date, title, contents)

# 현재 페이지의 모든 기사 링크를 리스트로 추출
def get_link(url):
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')
    links = []
    for tag in soup.select('.articleSubject'):
        links.append("https://finance.naver.com/" + tag.select_one('a')["href"].split('§')[0])
    return links


# 실시간 속보
def breaking_news():
    print("- 실시간 속보 -")

    base_url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258"

    links = []
    result = []
    page = int(input("몇번째 페이지까지 크롤링하시겠습니까? "))
    for current_page in range(1, page + 1):
        url = base_url + "&page=" + str(current_page)
        links += get_link(url)

    for link in links:
        result.append(crawling(link))
    return result

# 주요뉴스
def main_news():
    print("- 주요뉴스 -")

    base_url = "https://finance.naver.com/news/mainnews.naver"
    links = []
    result = []

    day = int(input(("며칠 전 뉴스까지 크롤링 하시겠습니까? (0입력 시 오늘의 주요뉴스만): ")))
    today = datetime.datetime.now()

    for d in range(day+1):
        target_day = (today - datetime.timedelta(days=d)).strftime('%Y-%m-%d')
        url = base_url + "?date=" + str(target_day)
        links += get_link(url)

    for link in links:
        result.append(crawling(link))
    return result

# 많이 본 뉴스
def most_viewed_news():
    print("- 많이 본 뉴스 -")
    base_url = "https://finance.naver.com/news/news_list.naver?mode=RANK"
    links = []
    result = []

    day = int(input(("며칠 전 뉴스까지 크롤링 하시겠습니까? (0입력 시 오늘의 많이 본 뉴스만): ")))
    today = datetime.datetime.now()

    for d in range(day+1):
        for page in range(1,5): # 4페이지까지
            target_day = (today - datetime.timedelta(days=d)).strftime('%Y%m%d')
            url = base_url + "&date=" + str(target_day) + "&page=" +str(page)
            req = requests.get(url).text
            soup = BeautifulSoup(req, 'html.parser')
            for tag in soup.select('.simpleNewsList'):
                for li in tag.select('li'):
                    links.append("https://finance.naver.com/" + li.select_one('a')["href"].split('§')[0])

    for link in links:
        result.append(crawling(link))
    return result

# 데이터 베이스 테이블 생성
def creatDB():
    con = sqlite3.connect("./news_data.db")
    cur = con.cursor()
    sql = "CREATE TABLE newsTable (id INTEGER PRIMARY KEY, date text, title text, contents text)"
    try:
        cur.execute(sql)
        print("The table has been created successfully!")
    except:
        print("table newsTable already exists!")
    finally:
        con.close()

def main():
    data = []
    # creatDB()
    try:
        con = sqlite3.connect("./news_data.db")
        cursor = con.cursor()
        print("Successfully connected to the database!")
    except:
        print("Connection failed!")

    while True:
        print("---------------------------------------")
        category = int(input("1. 실시간 속보\n2. 주요뉴스\n3. 많이 본 뉴스\n4. 종료\n원하는 카테고리 번호를 입력하세요: "))
        print("---------------------------------------")

        if category==1:
            data += breaking_news()
        elif category == 2:
            data += main_news()
        elif category == 3:
            data += most_viewed_news()
        elif category == 4:
            break

    try:
        INSERT_SQL = "INSERT INTO newsTable(id, date, title, contents) VALUES (?, ?, ?, ?);"
        cursor.executemany(INSERT_SQL, data)
        print("The Data has been inserted Successfully!")
    except Exception as e:
        print(e)

    con.commit()
    con.close()


if __name__ == "__main__":
    main()