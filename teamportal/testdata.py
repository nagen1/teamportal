from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import create_engine, func
from database import User, Role, Ideas, Comments, Likes, CampaignCreate, Campaigns, Choices, Questions
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///teamportal_dev2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

'''role1 = Role(name='Admin')
dbsession.add(role1)
dbsession.commit()

role1 = Role(name='teamMember')
dbsession.add(role1)
dbsession.commit()

roles = dbsession.query(Role)
for role in roles:
    print(role.name)

user1 = User(name='Tester1 QA', email='tester1@email.com', password='welcome', role_id='1')
dbsession.add(user1)
dbsession.commit()

user2 = User(name='Tester2 QA', email='tester2@email.com', password='welcome', role_id='2')
dbsession.add(user2)
dbsession.commit()

user3 = User(name='Tester3 QA', email='tester3@email.com', password='welcome', role_id='2')
dbsession.add(user3)
dbsession.commit()

idea1 = Ideas(title='Auto Framework', summary='Test Data folder contains the Test Data files for the each screen which need to be tested against the Automation framework. All the Test Data files will be placed unde', tags='Automation', user_id='1')
dbsession.add(idea1)
dbsession.commit()

idea2 = Ideas(title='TC Download from QC', summary="Isn't it simple if we where able to download test cases in to excel from QC using a simple Excel Macro. Enter basic details like user QC URL, USER ID, PWD download", tags='Manual', user_id='2')
dbsession.add(idea2)
dbsession.commit()

idea3 = Ideas(title='Performance Framework', summary='Test Data folder contains the Test Data files for the each screen which need to be tested against the Automation framework. All the Test Data files will be placed unde', tags='Automation', user_id='1')
dbsession.add(idea3)
dbsession.commit()

idea4 = Ideas(title='JIRA Zephyr', summary="Isn't it simple if we where able to download test cases in to excel from QC using a simple Excel Macro. Enter basic details like user QC URL, USER ID, PWD download", tags='Manual', user_id='1')
dbsession.add(idea4)
dbsession.commit()

roles = dbsession.query(Role)
for role in roles:
    print(role.name)

users = dbsession.query(User)
for user in users:
    print(user.name, " role:" ,user.role_id)

ideas = dbsession.query(Ideas)
for idea in ideas:
    print(idea.title)

#dbsession.commit()
email = "tester1@email.com"
users = dbsession.query(User).filter(User.email == email).first()
search = dbsession.query(Ideas).filter(Ideas.user_id == '1').all()

comment = dbsession.query(Comments).filter(Comments.idea_id == '1').all()

for each in comment:
    print(each.user.email)
    print(each.idea.id)

count = dbsession.query(Likes).filter(and_(Likes.idea_id == 1, Likes.like == True)).count()'''

#campaign = dbsession.query(Campaigns).filter(Campaigns.id == 2).one()
question = dbsession.query(CampaignCreate).filter(CampaignCreate.campaign_id == 2).all()

for quest in question:
    print(quest.question_id)