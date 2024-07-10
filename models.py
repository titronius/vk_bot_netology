from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    profile_url = Column(Text)
    city = Column(String(50))
    age = Column(Integer)
    gender = Column(String(1))


class Photo(Base):
    __tablename__ = 'photos'
    photo_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    photo_url = Column(Text)
    likes = Column(Integer)
    user = relationship("User")


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    favorite_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    user = relationship("User", foreign_keys=[user_vk_id])
    favorite_user = relationship("User", foreign_keys=[favorite_vk_id])


class Blacklist(Base):
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True)
    user_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    blocked_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    user = relationship("User", foreign_keys=[user_vk_id])
    blocked_user = relationship("User", foreign_keys=[blocked_vk_id])


# Подключение к базе данных
engine = create_engine('postgresql://your_username:your_password@localhost:5432/vkinder_db')
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с БД
Session = sessionmaker(bind=engine)
session = Session()
