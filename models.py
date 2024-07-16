import sqlalchemy as sq
import settings
# from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, Date, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import json

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True, nullable=False)

    def user_add(vk_id):
        user = User(vk_id = vk_id)
        session = BdInstruments.get_session()
        session.add(user)
        session.flush()
        session.commit()
        return user.id

    def user_check(vk_id):
        session = BdInstruments.get_session()
        q = session.query(User).filter(User.vk_id == vk_id)
        if q.one_or_none():
            return q.one_or_none()
        else:
            return False
    
    def user_get(user_id):
        session = BdInstruments.get_session()
        q = session.query(User).filter(User.id == user_id)
        if q.one_or_none():
            return q.one_or_none()
        else:
            return False


class RelationshipStatus(Base):
    __tablename__ = 'relationship_status'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)
    

class Relationship(Base):
    __tablename__ = 'relationship'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'), nullable=False)
    related_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'), nullable=False)
    status_id = sq.Column(sq.Integer, sq.ForeignKey('relationship_status.id'), nullable=False)

    user = relationship(User, foreign_keys=[user_id], backref='relationship_user')
    related_user = relationship(User, foreign_keys=[related_id], backref='relationship_users')
    status = relationship(RelationshipStatus, backref='relationship_status')

    def get_users(vk_id, status_id):
        session = BdInstruments.get_session()
        q = session.query(Relationship).filter(Relationship.user_id == vk_id, Relationship.status_id == status_id).first()
        if q:
            return q.related_id
        else:
            return False
        
    def relationship_add(user_id, related_id, status_id):
        session = BdInstruments.get_session()
        relationship = Relationship(user_id = user_id, related_id = related_id, status_id = status_id)
        session.add(relationship)
        session.commit()
        
    def status_set(user_vk_id, related_id, status_id):
        session = BdInstruments.get_session()
        user_id = User.user_check(user_vk_id).id
        session.query(Relationship).filter(Relationship.user_id == user_id,Relationship.related_id == related_id,).update({"status_id": status_id})
        session.commit()


class BdInstruments():
    engine = sq.create_engine(settings.DSN, pool_size=40, max_overflow=0)
    def get_session():
        Session = sessionmaker(bind=BdInstruments.engine)
        session = Session()
        return session
    
    def create_tables():
        Base.metadata.create_all(BdInstruments.engine)

    def drop_tables():
        Base.metadata.drop_all(BdInstruments.engine)

    def data_add():
        session = BdInstruments.get_session()
        with open('/var/bots/vk_bot_netology/data_for_bd/data.json', 'r') as fd:
            data = json.load(fd)

        for record in data:
            model = {
                'relationship_status': RelationshipStatus
            }[record.get('model')]
            session.add(model(**record.get('fields')))
        session.commit()
