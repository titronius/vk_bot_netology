from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, CheckConstraint, TIMESTAMP, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

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
    bdate = Column(Date)
    relation = Column(String(50))
    smoking = Column(String(50))
    alcohol = Column(String(50))


class Photo(Base):
    __tablename__ = 'photos'
    photo_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    photo_url = Column(Text)
    likes = Column(Integer)
    user = relationship("User")


class Relationship(Base):
    __tablename__ = 'relationships'
    id = Column(Integer, primary_key=True)
    user_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    related_vk_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False)
    status = Column(String(10), nullable=False)
    date_added = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    user = relationship("User", foreign_keys=[user_vk_id])
    related_user = relationship("User", foreign_keys=[related_vk_id])

    __table_args__ = (
        CheckConstraint(status.in_(['favorite', 'blacklisted']), name='status_check'),
    )

# Подключение к базе данных
engine = create_engine('postgresql://your_username:your_password@localhost:5432/vkinder_db')
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с БД
Session = sessionmaker(bind=engine)
session = Session()

