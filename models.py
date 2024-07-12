from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, Date, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    profile_url = Column(Text)
    city = Column(String(50))
    age = Column(Integer)
    gender = Column(CHAR(1))
    bdate = Column(Date)
    relation = Column(String(50))
    smoking = Column(String(50))
    alcohol = Column(String(50))
    date_added = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    photos = relationship("Photo", back_populates="user")
    relationships = relationship("Relationship", foreign_keys="[Relationship.user_id]")
    related_relationships = relationship("Relationship", foreign_keys="[Relationship.related_id]")

class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    photo_url = Column(Text)
    photo_vk_id = Column(Integer)
    likes = Column(Integer)

    user = relationship("User", back_populates="photos")

class RelationshipStatus(Base):
    __tablename__ = 'relationship_status'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    relationships = relationship("Relationship", back_populates="status")

class Relationship(Base):
    __tablename__ = 'relationship'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    related_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('relationship_status.id'), nullable=False)
    date_added = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="relationships")
    related_user = relationship("User", foreign_keys=[related_id], back_populates="related_relationships")
    status = relationship("RelationshipStatus", back_populates="relationships")

# Подключение к базе данных
engine = create_engine('postgresql://your_username:your_password@localhost:5432/vkinder_db')
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с БД
Session = sessionmaker(bind=engine)
session = Session()
