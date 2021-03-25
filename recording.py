from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
import feedparser
from pydantic import BaseModel


engine = create_engine('sqlite:///test.db', echo = True)
meta = MetaData()


news = Table(
    'news', meta,
    Column('id', Integer, primary_key = True),
    Column('title', String),
    Column('link', String),
    Column('desc', String),
    Column('published', String),
    Column('image', String, nullable=True),
    Column('content', String),
)


meta.create_all(engine)


class New(BaseModel):
    title: str
    link: str
    desc: str
    published: str
    image: str
    content: str


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
            if len(new['links']) == 2:
                new_valid = New(
                    title = new.title,
                    link = new.link,
                    desc = new.description,
                    published = new.published,
                    image = new.links[1]['href'],
                    content = new.summary,
                )
            else:
                new_valid = New(
                    title = new.title,
                    link = new.link,
                    desc = new.description,
                    published = new.published,
                    image = 'None',
                    content = new.summary,
                )

            conn.execute(
                insert(news),
                [
                    {
                        'title': new_valid.title,
                        'link': new_valid.link,
                        'desc': new_valid.desc,
                        'published': new_valid.published,
                        'image': new_valid.image,
                        'content': new_valid.content,
                    }
                ]  
                    )
            z += 1
            if z == 3:
                break

    conn.commit()
