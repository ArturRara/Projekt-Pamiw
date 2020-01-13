import datetime
import os
import psycopg2
from flask import Flask, make_response, request, url_for, redirect, jsonify
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
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres", pw="postgres", url="localhost:5433",
                                                               db="postgres")
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://lvfufmkfbedubw:a844463ec39a52848956642ee9bb431d1b5439ef6e6a38cc6715721da4ba5787@ec2-54-247-72-30.eu-west-1.compute.amazonaws.com:5432/dciikefmk2ajh3"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
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


@app.route('/register', methods=['POST'])
def registration():
    login = request.get_json()['login']
    password = request.get_json()['password']
    email = request.get_json()['email']
    usedLogin = User.query.filter_by(login=login).first()
    if usedLogin:
        return jsonify({"error": "Invalid email"})
    usedEmail = User.query.filter_by(login=login).first()
    if usedEmail:
        return jsonify({"error": "Invalid email"})
    password = generate_password_hash(password, method='sha256')
    new_user = User(login=login, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    result = {
        'login': login,
        'email': email,
        'password': password
    }

    return jsonify({'result': result})


@app.route('/', methods=['POST'])
def login():
    login = request.get_json()['login']
    password = request.get_json()['password']

    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid login and password"})
    else:
        access_token = create_access_token(identity={'login': user.login, 'email': user.email})
        return access_token


@app.route('/upload', methods=['POST'])
def upload():
    upload_dir = 'upload_files'
    fn = ""
    file_names = []
    for key in request.files:
        file = request.files[key]
        fn = secure_filename(file.filename)
        file_names.append(fn)
        print('filename: ', fn)
        try:
            file.save(os.path.join(upload_dir, fn))
        except:
            print('save fail: ' + os.path.join(upload_dir, fn))

   # return json.dumps({'filename': [f for f in file_names]})


@jwt_required
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('app_login')))
    unset_jwt_cookies(resp)
    return resp


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
