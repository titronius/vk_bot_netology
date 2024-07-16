<<<<<<< HEAD
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
=======
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
        if status_id in [3,4]:
            q = session.query(Relationship)\
                .join(User, User.id == Relationship.related_id)\
                .filter(Relationship.user_id == vk_id, Relationship.status_id == status_id)
            if q:
                users = []
                for user in q.all():
                    users.append(user.related_user.vk_id)
                return users
        else:
            q = session.query(Relationship).filter(Relationship.user_id == vk_id, Relationship.status_id == status_id).first()
            if q:
                return q.related_id
        if not q:
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
>>>>>>> a3db3e38e38238f0d04f3e01910199b868b6e553
