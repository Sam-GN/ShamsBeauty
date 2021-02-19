from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, HiddenField, \
    FieldList, FormField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import TimeField
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class PatientFormSessionList(FlaskForm):
    sessions = FieldList(StringField('Session'))

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=1, max=64)])
    tel = StringField('Tel', validators=[
        DataRequired(), Length(min=8, max=13)])
    firstVisit = StringField('First Visit Date', render_kw={'readonly': True})
    referer = StringField('Referer', validators=[
        Length(min=0, max=64)])
    hiddenField = HiddenField()
    createSession = SubmitField('Create Session')
    edit = SubmitField('Edit')
    submit = SubmitField('Save')





class SessionsForm(FlaskForm):
    patientName = StringField('Patient')
    hiddenField = HiddenField()
    date = StringField('Date', validators=[
        DataRequired()])
    time = TimeField('Time')
    dr = StringField('Dr', validators=[
        DataRequired(), Length(min=1, max=64)])
    details = TextAreaField('details', validators=[
        Length(min=0, max=240)], render_kw={'rows': 5})
    edit = SubmitField('Edit')
    submit = SubmitField('Save')

class UploadPicForm(FlaskForm):
    beforeFile = FileField('Before', render_kw={'multiple':True})
    afterFile = FileField('After', render_kw={'multiple': True})
    submit2 = SubmitField('Submit',render_kw={'class': 'btn btn-default'})
