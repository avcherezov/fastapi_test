from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, insert, select


engine = create_engine('sqlite:///test.db', echo = True)
meta = MetaData()

news = Table(
    'news', meta,
    Column('id', Integer, primary_key = True),
    Column('title', String),
    Column('link', String),
    Column('desc', String),
    Column('published', String),
)

s = news.select()
conn = engine.connect()
result = conn.execute(s)

for row in result:
    print (row)