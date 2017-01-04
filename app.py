from flask import Flask, render_template, request, session, url_for, flash, redirect, send_file, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, and_, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database import Base, User, Ideas, Comments, Likes, WatchList, \
    Campaigns, Choices, Questions, CampaignCreate, CampaignResults
from functools import wraps
from flask_login import LoginManager
import os

app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ppt', 'zip', 'pptx', 'doc', 'docx'])
engine = create_engine('sqlite:///teamportal_dev2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#------------------------- LOGIN Functionality-----------------------------------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("you need to login first:")
            return redirect(url_for('login'))

    return wrap

@login_manager.user_loader
def load_user(user_id):
    return user_id

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    if session['user_id']:
        loggedUser = session['user_id']
        return render_template("index.html", user=loggedUser)
    else:
        return "username doesn't exists"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'hotmail' in request.form['email']:
            newUser = User()
            newUser.name = request.form['name']
            newUser.email = request.form['email']
            newUser.password = request.form['password']
            newUser.role_id = '2'
            dbsession.add(newUser)
            dbsession.commit()
            flash("User Registration Successful!")
            return redirect(url_for('login'), code=302)

        else:
            flash("Invalid email Address!")
            return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        loginId = request.form['username']
        lookup = dbsession.query(User).filter(User.email == loginId).first()
        if lookup:
            if lookup.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = loginId

                return redirect(url_for('index'))
        else:
            error = 'Invalid user Credentials'
            return render_template('auth/login.html', error=error), 400

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return render_template('auth/logout.html')

#------------------------- LOGIN Functionality Ends-----------------------------------


#------------------------- Ideas Functionality----------------------------------------

@app.route('/ideas/new', methods=['GET', 'POST'])
def newIdea():

    idea = Ideas()
    if request.method == 'POST':
        idea.title = request.form['title']
        idea.summary = request.form['summary']
        idea.tags = request.form['tags']
        loggedInUser = session['user_id']
        user = dbsession.query(User).filter(User.email == loggedInUser).first()
        idea.user_id = user.id
        dbsession.add(idea)
        dbsession.commit()

        file = request.files['file']
        id = str(idea.id)
        if file.filename != '':
            if file and allowed_file(file.filename):
                filename = id + secure_filename(file.filename)
                idea.filename = filename
                filepath = app.config['UPLOAD_FOLDER'] + os.sep + filename
                file.save(os.path.abspath(filepath))
                idea.filePath = filepath
                dbsession.add(idea)
                dbsession.commit()

        flash('Idea Posted Successfully!')
        return redirect(url_for('ideas'), code=302)
    else:
        return render_template('ideas/newIdea.html')


@app.route('/ideas')
def ideas():
    ideasList = dbsession.query(Ideas).order_by(Ideas.title).all()

    return render_template('ideas/index.html', ideas=ideasList)


@app.route('/ideas/details/<int:idea_id>')
def ideaDetails(idea_id):
    try:
        details = dbsession.query(Ideas).filter(Ideas.id == idea_id).one()
        comment = dbsession.query(Comments).filter(Comments.idea_id == idea_id).all()
        like = dbsession.query(Likes).filter(and_(Likes.idea_id == idea_id, Likes.like == True)).count()
        dislike = dbsession.query(Likes).filter(and_(Likes.idea_id == idea_id, Likes.like == False)).count()
        return render_template('ideas/ideaDetails.html', detail=details, comments=comment, likes=like, dislikes=dislike)

    except NoResultFound:
        flash('No ideas found with this Title/ID!')
        return redirect(url_for('ideas'), code=302)


@app.route('/ideas/delete/<int:idea_id>', methods=['GET', 'POST'])
def deleteIdea(idea_id):

    if request.method == 'POST':
        details = dbsession.query(Ideas).filter(Ideas.id == idea_id).one()
        if details.user.email == session['user_id']:
            dbsession.delete(details)
            dbsession.commit()

            flash('Idea Deleted Successfully!')
            return redirect(url_for('ideas'), code=302)
        else:
            flash('You are not Authorized to Delete this Idea!')
            return redirect(url_for('ideas'), code=302)
    else:
        details = dbsession.query(Ideas).filter(Ideas.id == idea_id).one()
        return render_template('ideas/deleteIdea.html', detail=details)


@app.route('/ideas/edit/<int:idea_id>', methods=['GET', 'POST'])
def editIdea(idea_id):
    try:
        details = dbsession.query(Ideas).filter(Ideas.id == idea_id).one()
    except NoResultFound:
        flash('No idea found with this Title/ID!')
        return redirect(url_for('ideas'), code=302)

    if request.method == 'POST':
        if details.user.email == session['user_id']:
            details.title = request.form['title']
            details.summary = request.form['summary']
            details.tags = request.form['tags']
            loggedInUser = session['user_id']
            user = dbsession.query(User).filter(User.email == loggedInUser).first()
            details.user_id = user.id
            dbsession.add(details)
            dbsession.commit()

            flash("Idea Edited Successfully!")
            return redirect(url_for('ideas'), code=302)
        else:
            flash('You are not Authorized to Edit this Idea!')
            return redirect(url_for('ideas'), code=302)
    else:
        return render_template('/ideas/editIdea.html', idea=details)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        if request.form['search']:
            term = request.form['search']
            try:
                results = dbsession.query(Ideas).filter(Ideas.title.like('%'+term+'%'))
                return render_template('ideas/search.html', ideas=results)
            except NoResultFound:
                error = 'No Results found!'
                return render_template('ideas/search.html', error=error)


@app.route('/ideas/me')
def myIdeas():
    me = session['user_id']
    try:
        users = dbsession.query(User).filter(User.email == me).first()
        myideas = dbsession.query(Ideas).filter(Ideas.user_id == users.id).all()
        return render_template('/ideas/myIdeas.html', ideas=myideas)

    except NoResultFound:
        error = "You haven't posted any Ideas yet! try doing it now"
        return render_template('/ideas/myIdeas.html', error=error)


@app.route('/ideas/me/watchlist')
def myWatch():
    me = session['user_id']
    try:
        users = dbsession.query(User).filter(User.email == me).first()
        mywatchlist = dbsession.query(WatchList).filter(WatchList.user_id == users.id).all()
        return render_template('/ideas/myWatch.html', watchlist=mywatchlist)

    except NoResultFound:
        error = "You haven't posted any Ideas yet! try doing it now"
        return render_template('/ideas/myIdeas.html', error=error)


@app.route('/ideas/me/comments')
def myComments():
    me = session['user_id']
    try:
        users = dbsession.query(User).filter(User.email == me).first()
        mycomments = dbsession.query(Comments).filter(Comments.createdBy == users.id).all()

        return render_template('/ideas/myComments.html', comments=mycomments)

    except NoResultFound:
        error = "You haven't commented on any Ideas yet! try doing it now"
        return render_template('/ideas/myIdeas.html', error=error)


@app.route('/ideas/watchlist')
def watchlist():
    watchlist = WatchList()
    idea_id = int(request.args.get('idea_id'))
    temp = request.args.get('watchIt')
    loggedUser = session['user_id']  # Need to add an other condition to validate same user is not vote/like one idea many times
    user = dbsession.query(User).filter(User.email == loggedUser).one()
    try:
        checkpoint = dbsession.query(WatchList).filter(and_(WatchList.idea_id == idea_id, WatchList.user_id == user.id)).one()
    except NoResultFound or MultipleResultsFound:
        if temp == 'watchit':
            watchlist.watchIt = True
            watchlist.idea_id = idea_id
            watchlist.user_id = user.id
            dbsession.add(watchlist)
            dbsession.commit()
            return jsonify(watch='Added to your Watch List')
    if checkpoint:
        return jsonify(watch='Already added to your Watch List')


@app.route('/ideas/comments', methods=['POST'])
def comments():
    if request.method == 'POST':
        if request.form['comment']:
            comment = Comments()
            comment.comment = request.form['comment']
            comment.idea_id = request.form['idea_id']
            email = session["user_id"]
            user = dbsession.query(User).filter(User.email == email).one()
            comment.createdBy = user.id
            dbsession.add(comment)
            dbsession.commit()

            flash("Comment posted Successfully!", "comment")
            return redirect(url_for('ideaDetails', idea_id=comment.idea_id))
    else:
        return None


@app.route('/ideas/download/<int:idea_id>', methods=['GET'])
def download(idea_id):
    try:
        idea = dbsession.query(Ideas).filter(Ideas.id == idea_id).one()
        #split = idea.filePath.split('\\')
        filename = idea.filename

        return send_file(idea.filePath, attachment_filename=filename)
    except Exception as e:
        return str(e)


@app.route('/ideas/likes')
def likes():
    likes = Likes()
    idea_id = int(request.args.get('idea_id'))
    temp = request.args.get('likez')
    if temp == 'like':
        likes.like = True
    else:
        likes.like = False

    likes.idea_id = idea_id
    loggedUser = session['user_id'] #Need to add an other condition to validate same user is not vote/like one idea many times
    user = dbsession.query(User).filter(User.email == loggedUser).one()
    likes.user_id = user.id
    dbsession.add(likes)
    dbsession.commit()

    if likes.like is True:
        count = dbsession.query(Likes).filter(and_(Likes.idea_id == idea_id, Likes.like == True)).count()
    else:
        count = dbsession.query(Likes).filter(and_(Likes.idea_id == idea_id, Likes.like == False)).count()

    return jsonify(result=count)


@app.route('/tools')
def tools():

    try:
        tools = dbsession.query(Ideas).filter(Ideas.usability == True).all()

    except NoResultFound:
        flash("NO results found!")
        None

    return render_template('tools/index.html', ideas=tools)


#------------------------- Poll/Survey/Announcements Functionality ------------------------------------

@app.route('/campaigns/new', methods=['GET', 'POST'])
def newCampaign():

    if request.method == 'POST':
        campaign = Campaigns()

        if 'newCampaign' in request.form:
            campaign.name = request.form['newCampaign']
            try:
                campaign = dbsession.query(Campaigns).filter(Campaigns.name == campaign.name).one()
            except NoResultFound:
                None
                dbsession.add(campaign)
                dbsession.commit()

            x = 1
            while x <= 5:
                temp = 'question' + str(x)
                if temp in request.form:
                    questionName = request.form[temp]
                    if questionName is not '':
                        question = Questions()
                        question.name = questionName
                        dbsession.add(question)
                        dbsession.commit()
                y = 1
                while y <= 4:
                    chTemp = temp + 'choice' + str(y)
                    if chTemp in request.form:
                        choiceName = request.form[chTemp]
                        if choiceName is not '':
                            try:
                                choice = dbsession.query(Choices).filter(Choices.name == choiceName).one()
                            except NoResultFound:
                                choice = Choices()
                                choice.name = request.form[chTemp]
                                dbsession.add(choice)
                                dbsession.commit()

                            campaignCreate = CampaignCreate()
                            campaignCreate.campaign_id = campaign.id
                            campaignCreate.question_id = question.id
                            campaignCreate.choice_id = choice.id
                            dbsession.add(campaignCreate)
                            dbsession.commit()
                    y += 1
                x += 1

        return redirect(url_for('campaigns'))

    else:
        return render_template('/campaigns/newCampaign.html')


@app.route('/campaigns')
def campaigns():
    try:
        campaign = dbsession.query(Campaigns).order_by(Campaigns.name).all()
    except NoResultFound:
        flash("No Campaigns Created Yet!")

    return render_template('/campaigns/index.html', campaigns=campaign)


@app.route('/campaigns/<int:campaign_id>')
def campaignDetails(campaign_id):

    try:
        campaign = dbsession.query(Campaigns).filter(Campaigns.id == campaign_id).one()
        questions = dbsession.query(CampaignCreate).group_by(CampaignCreate.question_id). \
            filter(CampaignCreate.campaign_id == campaign_id).all()
        choices = dbsession.query(CampaignCreate).filter(CampaignCreate.campaign_id == campaign_id).all()
    except NoResultFound:
        flash('No Campaign Exists!')

    return render_template('/campaigns/campaignDetails.html', campaign=campaign, questions=questions, choices=choices)


#------------------------- App Launch ------------------------------------
if __name__ == '__main__':
    app.secret_key = 'super_secret_key_230742'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))   #for cloud9
