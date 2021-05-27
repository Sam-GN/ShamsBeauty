from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from time import time
import jwt
from app import app, helper


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    level = db.Column(db.String(64))
    sessions = db.relationship('Session', backref='dr', lazy='dynamic')
    removed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)





class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    tel = db.Column(db.Integer, index=True)
    location = db.Column(db.String(64), index=True)
    referer = db.Column(db.String(64))
    sessions = db.relationship('Session', backref='name', lazy='dynamic')

    def __repr__(self):
        return '<Patient {}>'.format(self.name, self.tel)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    sessionDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    nextSessionDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Integer)
    detail = db.Column(db.Text)
    imageString = db.Column(db.Text)


    def jalali(self):
        return helper.convertGregorianToJalali(self.sessionDate)

    def jalaliNext(self):
        return helper.convertGregorianToJalali(self.nextSessionDate)

    def __repr__(self):
        date = self.jalali()
        value = str(date.year)+'/'+str(date.month).zfill(2)+'/'+str(date.day).zfill(2)+'  '+str(self.sessionDate.hour).zfill(2)+':'+str(self.sessionDate.minute).zfill(2)
        return value

