from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamportal.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    isActive = Column(Boolean, default=True)

class User(db.Model):
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

class Ideas(db.Model):
    __tablename__ = 'ideas'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    summary = Column(String(2000), nullable=False)
    tags = Column(String(30), nullable=True)
    user_id = Column(Integer, ForeignKey(User.id))
    filePath = Column(String(100), nullable=True)
    isActive = Column(Boolean, default=True)
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

class Comments(db.Model):
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

engine = create_engine('sqlite:///teamportal.db')
db.metadata.create_all(engine)

if __name__ == '__main__':
    manager.run()

'''to activate virtual environment and run migration using Flask-Migrate
activate vitural env
--- $ source venv/teamportal/bin/activate teamportal

Run migration
--- $ python database-migration_setup.py db migrate

run upgrade database to apply migration scripts
--- $ python database-migration_setup.py db upgrade

test commit '''
