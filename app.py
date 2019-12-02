import os
from flask import Flask, jsonify, make_response, request, render_template, url_for, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from jwt import encode, decode
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.before_first_request
# def create_tables():
#    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.aemailge = email



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

    new_user = User(login=userLogin, password=generate_password_hash(password, method='sha256'), email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    userLogin = request.form['login']
    password = request.form['password']

    user = User.query.filter_by(login=userLogin).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('app.login'))

    access_token = create_access_token(identity=User['username'])
    return {
        'access_token': access_token
        # redirect(url_for('app.loginPage'))
    }



@app.route('/')
def app_default():
    return render_template("loginPage.html")


@app.route('/loginPage')
def app_login():
    return make_response(render_template('loginPage.html'))


@app.route('/registration/')
def app_register():
    return render_template("registrationPage.html")


@app.route('/upload')
#@jwt_required
def app_upload():
    return render_template("uploadPage.html")


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            # revoked_token = RevokedTokenModel(jti=jti)
            # revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


if __name__ == '__main__':
    db.create_all()
    app.run()
