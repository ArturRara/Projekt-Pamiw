import os
import psycopg2
from flask import Flask, jsonify, make_response, request, render_template, url_for, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from jwt import encode, decode
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, set_access_cookies, JWTManager, unset_jwt_cookies)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="name", pw="password", url="localhost", db="users")

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    _tablename_ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(500), unique=True)



    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email


jwt = JWTManager(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@jwt_required
def upload(self):
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploadPage.html')


@jwt_required
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/registration', methods=['POST'])
def registration():
    userLogin = request.form['login']
    password = request.form['password']
    email = request.form['email']
#password=generate_password_hash(password, method='sha256')
    new_user = User(login=userLogin, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return render_template("loginPage.html")


@app.route('/login', methods=['POST'])
def login():
    userLogin = request.form['login']
    password = request.form['password']

    user = User.query.filter_by(login=userLogin).first()
    #check_password_hash()
    if not user or not user.password == password:
        render_template("loginPage.html")

    access_token = create_access_token(identity=user)
    resp = make_response(redirect(url_for('main.index')))
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


# @jwt_required
@app.route('/upload')
def app_upload():
    return render_template("uploadPage.html")


class UserLogout(Resource):
    @jwt_required
    def post(self):
        resp = make_response(redirect(url_for('.signin')))
        unset_jwt_cookies(resp)
        return resp


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
