from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, insert
import feedparser


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

meta.create_all(engine)


NEWS_SITE = [
    'http://lenta.ru/rss',
    'http://www.interfax.ru/rss.asp',
    'http://www.kommersant.ru/RSS/news.xml',
    'http://www.m24.ru/rss.xml'
]

with engine.connect() as conn:
    for x in NEWS_SITE:
        d = feedparser.parse(x)
        y = d.entries

        z = 0

        for new in y:
            conn.execute(
                insert(news),
                [
                    {
                        'title': new.title,
                        'link': new.link,
                        'desc': new.description,
                        'published': new.published,
                    }
                ]  
                    )
            z += 1
            if z == 3:
                break

    conn.commit()



