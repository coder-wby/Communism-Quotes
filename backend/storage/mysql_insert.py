# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import sessionmaker

from backend.util.html_parser import bulk_doc_json

""" 前置工作

1. 创建数据库
CREATE DATABASE marxism;
USE marxism;

2. 创建新用户
CREATE USER 'marxist'@'localhost' IDENTIFIED BY 'marx';
GRANT ALL privileges on marxism.* to marxist@localhost;
FLUSH privileges;

3. 创建数据表

CREATE TABLE IF NOT EXISTS articles(
   doc_id INT UNSIGNED AUTO_INCREMENT,
   doc_title VARCHAR(128) NOT NULL,
   doc_author VARCHAR(32) NOT NULL,
   doc_date_text VARCHAR(64),
   doc_date DATE,
   doc_source VARCHAR(64),
   doc_content TEXT, 
   PRIMARY KEY ( doc_id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

DROP TABLE articles;
truncate table articles;

4. 连接数据库

"mysql+pymysql://marxist:marx@127.0.0.1/marxism?charset=utf8MB4",

ElasticSearch会为doc自动配置id

"""

engine = create_engine(
    # 如果你在使用MySQL或MariaDB 不要用utf8编码 改用“utf8mb4
    "mysql://marxist:marx@127.0.0.1/marxism?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收(重置)
)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Article(Base):
    __tablename__ = 'articles'

    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_title = Column(String, nullable=False)
    doc_author = Column(String, nullable=False)
    doc_date_text = Column(String, nullable=True)
    doc_date = Column(Date, nullable=True)
    doc_source = Column(String, nullable=True)
    doc_content = Column(String, nullable=True)

    def __repr__(self):
        return "<Article(title='%s', author='%s', para id='%s')>" % (
            self.doc_title, self.doc_author, self.doc_id)


def json_2_object(json: dict):
    return Article(
        doc_title=json["title"],
        doc_author=json["author"],
        doc_date_text=json["date_text"],
        doc_date=json["date"],
        doc_source=json["source"],
        doc_content=json["content"]
    )


def batch_insert(author):
    for para_json_list in bulk_doc_json(author):
        object_list = [json_2_object(json) for json in para_json_list]
        try:
            response = session.bulk_save_objects(object_list, return_defaults=True)
            session.commit()
            print(f"得到反馈结果 {response}.")
        except Exception as e:
            print("\nERROR:", e)


if __name__ == '__main__':
    batch_insert(["maozedong", "lenin-cworks"])
