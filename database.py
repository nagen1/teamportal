from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    isActive = Column(Boolean, default=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    isActive = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey(Role.id))
    role = relationship(Role)

    '''@property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }'''

class Ideas(Base):
    __tablename__ = 'ideas'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    summary = Column(String(2000), nullable=False)
    tags = Column(String(30), nullable=True)
    filename = Column(String(50), nullable=True)
    filePath = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey(User.id))
    isActive = Column(Boolean, default=True)
    usability = Column(Boolean, default=False)
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship(User)

    '''@property
    def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'id': self.id,
        'title': self.title,
        'summary': self.summary,
    }'''

class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    idea_id = Column(Integer, ForeignKey(Ideas.id))
    comment = Column(String(200), nullable=False)
    isActive = Column(Boolean, default=True)
    createdBy = Column(Integer, ForeignKey(User.id))
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", foreign_keys=[createdBy])
    idea = relationship("Ideas", foreign_keys=[idea_id])

class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    idea_id = Column(Integer, ForeignKey(Ideas.id))
    user_id = Column(Integer, ForeignKey(User.id))
    like = Column(Boolean)
    user = relationship("User", foreign_keys=[user_id])
    idea = relationship("Ideas", foreign_keys=[idea_id])

class WatchList(Base):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True)
    idea_id = Column(Integer, ForeignKey(Ideas.id))
    user_id = Column(Integer, ForeignKey(User.id))
    watchIt = Column(Boolean)
    user = relationship("User", foreign_keys=[user_id])
    idea = relationship("Ideas", foreign_keys=[idea_id])

class Campaigns(Base):
    __tablename__ = 'campaign'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    createdBy = Column(Integer, ForeignKey(User.id))
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", foreign_keys=[createdBy])

class Questions(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    createdBy = Column(Integer, ForeignKey(User.id))
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", foreign_keys=[createdBy])

class Choices(Base):
    __tablename__ = 'choice'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    createdBy = Column(Integer, ForeignKey(User.id))
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", foreign_keys=[createdBy])

class CapmaignResults(Base):
    __tablename__ = 'campaignResults'

    id = Column(Integer, primary_key=True)
    campaing_id = Column(Integer, ForeignKey(Campaigns.id))
    question_id = Column(Integer, ForeignKey(Questions.id))
    choice_id = Column(Integer, ForeignKey(Choices.id))
    createdBy = Column(Integer, ForeignKey(User.id))
    isActive = Column(Boolean, default=True)
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    campaign = relationship("Campaigns", foreign_keys=[campaing_id])
    question = relationship("Questions", foreign_keys=[question_id])
    choice = relationship("Choices", foreign_keys=[choice_id])
    user = relationship("User", foreign_keys=[createdBy])


engine = create_engine('sqlite:///teamportal_dev.db')
Base.metadata.create_all(engine)
