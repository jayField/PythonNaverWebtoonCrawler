# 제목,작가,내용,장르,연령정보추출

import requests
import lxml.html
import re
import sqlite3

con = sqlite3.connect("./testing.db")
cur = con.cursor()
cur.execute('drop table if exists webtoon;')
cur.execute('create table webtoon(title text, auther text, contents text, genre text, age text)')

session = requests.Session()
res = requests.get("https://comic.naver.com/index.nhn")

root = lxml.html.fromstring(res.content)

root.make_links_absolute(res.url)

for a in root.cssselect('.genreRecomInfo2 .title  a'):  # cssselect에서 . = 클래스명
    url = a.get('href')  # 옵션이 href인 값을 가져와라

    # print(url)
    res = session.get(url)
    root = lxml.html.fromstring(res.content)
    title = root.cssselect('.detail h2')[0].text
    # print(title)# 제목 성공

    auther = root.cssselect('.detail span')[0].text
    # print(auther)

    content = root.cssselect('.detail p')[0].text
    # print(content)

    genre = root.cssselect('.detail_info span')[0].text
    # print(genre)

    age = root.cssselect('.detail_info span')[1].text
    # print(age)

    contents = ''
    for p in root.cssselect('.detail h2'):
        title2 = p.text

        if title2 != None:
            title2 = re.sub('\s+', '', title2)
    title = title2

    for q in root.cssselect('.detail h2 span'):

        auther2 = q.text

        if auther2 != None:
            auther2 = re.sub('\s+', '', auther2)
    auther = auther2

    cur.execute('insert into webtoon values(:title, :auther, :contents, :genre, :age)',
                {'title': title, 'auther': auther, 'contents': content, 'genre': genre, 'age': age})

con.commit()
con.close()

con = sqlite3.connect('./testing.db')
cur = con.cursor()
cur.execute('select * from webtoon')

while True:
    row = cur.fetchone()
    if row == None:
        break;

    data1 = row[0]
    data2 = row[1]
    data3 = row[2]
    data4 = row[3]
    data5 = row[4]

    print("제목: ", data1)
    print("작가: ", data2)
    print("내용: ", data3)
    print("장르: ", data4)
    print("연렁정보: ", data5)
    print("==================================")


