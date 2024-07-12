from sqlalchemy import create_engine, Column, Integer, String, Date, SmallInteger, ForeignKey, UniqueConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    bdate = Column(Date, nullable=False)
    sex = Column(SmallInteger)
    city = Column(String(100))
    relation = Column(SmallInteger)
    smoking = Column(SmallInteger)
    alcohol = Column(SmallInteger)

    def __repr__(self):
        return f'<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>'


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    photo_url = Column(String(512), nullable=False)

    user = relationship('Users', backref='photos')

    def __repr__(self):
        return f'<Photo(id={self.id}, user_id={self.user_id}, photo_url={self.photo_url})>'


class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    favorited_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date_added = Column(TIMESTAMP, nullable=False, server_default='now()')

    user = relationship('Users', foreign_keys=[user_id])
    favorited_user = relationship('Users', foreign_keys=[favorited_user_id])

    __table_args__ = (
        UniqueConstraint('user_id', 'favorited_user_id'),
    )

    def __repr__(self):
        return f'<Favorite(id={self.id}, user_id={self.user_id}, favorited_user_id={self.favorited_user_id}, date_added={self.date_added})>'


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    blacklisted_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date_added = Column(TIMESTAMP, nullable=False, server_default='now()')

    user = relationship('Users', foreign_keys=[user_id])
    blacklisted_user = relationship('Users', foreign_keys=[blacklisted_user_id])

    __table_args__ = (
        UniqueConstraint('user_id', 'blacklisted_user_id'),
    )

    def __repr__(self):
        return f'<Blacklist(id={self.id}, user_id={self.user_id}, blacklisted_user_id={self.blacklisted_user_id}, date_added={self.date_added})>'


def create_tables(engine):
    Base.metadata.create_all(engine)
    print('Таблицы созданы')

def drop_tables(engine):
    Base.metadata.drop_all(engine)
    print('Таблицы удалены')