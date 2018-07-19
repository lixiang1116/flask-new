
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os

basedir=os.path.abspath(os.path.dirname(__file__))

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config.update(dict(
     DEBUG=True,
     SECRET_KEY='development key',
     USERNAME='admin',
     PASSWORD='default'
 ))


db=SQLAlchemy(app)

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(64))
    text=db.Column(db.String(1000))

    #def __init__(self,title,text):

        #self.title= title
        #self.text = text

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()



@app.route('/')
def show_entries():
    entries = Role.query.all()

    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    role=Role(title=request.form['title'],text=request.form['text'])
    db.session.add(role)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)