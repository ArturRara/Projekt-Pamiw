import datetime
import os
import psycopg2
from flask import Flask, make_response, request, render_template, url_for, redirect, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (create_access_token, jwt_required, set_access_cookies, JWTManager, unset_jwt_cookies)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_SECRET_KEY'] = 'longsecret'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
jwt = JWTManager(app)

app.config['SECRET_KEY'] = "secret"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres", pw="password", url="postgres",
                                                               db="users")
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://lvfufmkfbedubw:a844463ec39a52848956642ee9bb431d1b5439ef6e6a38cc6715721da4ba5787@ec2-54-247-72-30.eu-west-1.compute.amazonaws.com:5432/dciikefmk2ajh3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    _tablename_ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email


class Files(db.Model):
    _tablename_ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), unique=True)
    filePdf = db.Column(db.LargeBinary)

    def __init__(self, filename, filePdf):
        self.filename = filename
        self.filePdf = filePdf


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['GET', 'POST'])
@jwt_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploadPage.html')


@jwt_required
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/registration', methods=['POST'])
def registration():
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    usedLogin = User.query.filter_by(login=login).first()
    if usedLogin:
        flash("That username is already taken, please choose another")
        return redirect(url_for('registration'))
    usedEmail = User.query.filter_by(login=login).first()
    if usedEmail:
        flash("That email is already used")
        return redirect(url_for('registration'))
    password = generate_password_hash(password, method='sha256')
    new_user = User(login=login, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return render_template("loginPage.html")


@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        flash("Login or password is incorrect")
        return render_template("loginPage.html")
    else:
        access_token = create_access_token(identity=login)
        resp = make_response(redirect(url_for('upload')))
        set_access_cookies(resp, access_token)
        return resp


@app.route('/')
def app_default():
    return render_template("loginPage.html")


@app.route('/loginPage')
def app_login():
    return make_response(render_template('loginPage.html'))


@app.route('/registration/')
def app_register():
    return render_template("registrationPage.html")


@jwt_required
@app.route('/api/upload')
def app_upload():
    return render_template("uploadPage.html")


@jwt_required
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('app_login')))
    unset_jwt_cookies(resp)
    return resp


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
