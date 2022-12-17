import datetime
from sqlalchemy import Column, Integer, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import config
from utils import _TIME_FORMAT_


Base = declarative_base()


class Todos(Base):
    __tablename__ = 'todos'
    # auto increment TODO: change id to 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    todo_name = Column(Text)
    # if have parent id, it would be the `key result` otherwise, it is an `objective`
    parent_id = Column(Integer)
    done = Column(Integer)
    # created_at will return UTC date string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id: int, todo_name: str, parent_id: int, done: int):
        self.user_id = user_id
        self.todo_name = todo_name
        self.parent_id = parent_id
        self.done = done

    def get_item(self):
      return {
          'id': self.id,
          'user_id': self.user_id,
          'todo_name': self.todo_name,
          'parent_id': self.parent_id,
          'done': self.done,
          'created_at': self.created_at.strftime(_TIME_FORMAT_)
        }


engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(config['DB_USER'],config['DB_PASSWORD'],config['DB_HOST'],config['DB_NAME']))
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)