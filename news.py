from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from pydantic import BaseModel
from fastapi import FastAPI


engine = create_engine('sqlite:///test.db', connect_args={"check_same_thread": False})
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


class NewsOut(BaseModel):
    title: str
    link: str
    desc: str
    published: str


class NewOut(BaseModel):
    title: str
    image: str
    content: list


app = FastAPI()


@app.get('/')
def read_news():
    conn = engine.connect()
    query = news.select().limit(12).order_by(-news.c.id)
    result = conn.execute(query)
    x = []
    for new in result:
        new_valid = NewsOut(
                title = new.title,
                link = new.link,
                desc = new.desc,
                published = new.published,
            )
        x.append(new_valid)
    return x


@app.get('/{new_id}')
def read_new(new_id: int):
    conn = engine.connect()
    query = news.select().where(news.c.id == new_id)
    result = conn.execute(query)
    for new in result:
        new_valid = NewOut(
                title = new.title,
                image = new.image,
                content = [new.content],
            )
    return new_valid
