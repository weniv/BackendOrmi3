https://paullabworkspace.notion.site/Django-SQLite3-f4adf80dcaec47759c7d4c0c838821ea?pvs=4

최종 실습 코드

## 실습 1
import sqlite3

conn = sqlite3.connect('ex1.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE books (id integer, title text, price integer)
''')

c.execute('''
    INSERT INTO books VALUES (1, 'python 가이드', 5000)
''')
c.execute('''
    INSERT INTO books VALUES (2, 'js 가이드', 5000)
''')

conn.commit()
conn.close()

conn = sqlite3.connect('ex1.db')
c = conn.cursor()

# 데이터 조회
for row in c.execute('SELECT * FROM books ORDER BY id'):
    print(row)

# 연결 종료
conn.close()

## 실습 2
import sqlite3

conn = sqlite3.connect('ex2.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE books (id integer, title text, price integer)
''')

for i in range(10):
    c.execute(f"INSERT INTO books VALUES ({i}, 'python 가이드', {i*1000})")

conn.commit()
conn.close()

conn = sqlite3.connect('ex2.db')
c = conn.cursor()

# 데이터 조회
for row in c.execute('SELECT * FROM books ORDER BY id'):
    print(row)

# 연결 종료
conn.close()

## 실습 3
import sqlite3

data = {
    'id': [1, 2, 3],
    'title': ['1', '2', '3'],
    'content': ['11', '22', '33', '44', '55']
}

# 데이터베이스에 연결
conn = sqlite3.connect('ex3.db')

# 커서 생성
cursor = conn.cursor()

# post 테이블 생성
cursor.execute('CREATE TABLE post (id INTEGER, title TEXT, content TEXT)')

# 데이터 삽입
for i in range(len(data['id'])):
    cursor.execute('INSERT INTO post VALUES (?, ?, ?)', (data['id'][i], data['title'][i], data['content'][i]))

# 커밋(변경 사항 저장)
conn.commit()

# 연결 닫기
conn.close()

conn = sqlite3.connect('ex3.db')
c = conn.cursor()

# 데이터 조회
for row in c.execute('SELECT * FROM post'):
    print(row)

# 연결 종료
conn.close()

## 실습4
# 네이버에 최신영화를 별점과 함께 DB 넣어주세요!

class Movie(models.Model):
    title = models.CharField(max_length=100)
    star = models.IntegerField()

    def __str__(self):
        return self.title


python manage.py makemigrations
python manage.py migrate

##############################

from django.contrib import admin
from .models import Post, Movie

admin.site.register(Post)
admin.site.register(Movie)

##############################

db.sqlite3를 colab에 업로드!
(실무에서 이러면 큰일납니다. '사건'에 해당합니다.)

##############################

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# 데이터 조회(데이터가 없어서 안나옵니다.)
for row in c.execute('SELECT * FROM blog_movie'):
    print(row)

# 데이터 조회(데이터가 있어 나옵니다.)
for row in c.execute('SELECT * FROM blog_post'):
    print(row)

# 연결 종료
conn.close()

##############################

import requests
from bs4 import BeautifulSoup

url = 'https://paullab.co.kr/bookservice/'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')
data = []

book_list = soup.select('.book_name')        # lecture 클래스 탐색
for lecture in book_list:
    data.append([lecture.text, 10])

data

##############################

import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')

# 커서 생성
cursor = conn.cursor()

# 데이터 삽입
for i in range(len(data)):
    cursor.execute(f'INSERT INTO blog_movie VALUES ({i+1}, "{data[i][0]}", {data[i][1]})')

# 커밋(변경 사항 저장)
conn.commit()

# 연결 닫기
conn.close()

##############################

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# 데이터 조회
for row in c.execute('SELECT * FROM blog_movie'):
    print(row)

# 연결 종료
conn.close()

##############################

db.sqlite3다운로드 하고 django db에 덮어쓰기