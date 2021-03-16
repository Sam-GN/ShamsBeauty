from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, HiddenField, \
    FieldList, FormField, FileField, SelectField
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
    myChoices = 'Receptionist', 'Technician','Doctor'
    level = SelectField('Level', choices=myChoices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



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
    location = StringField('Location',validators=[
        DataRequired()])
    referer = StringField('Referer', validators=[
        Length(min=0, max=64)])
    hiddenField = HiddenField()
    createSession = SubmitField('Create Session')
    edit = SubmitField('Edit')
    submit = SubmitField('Save')
    delete = SubmitField('Delete',render_kw={'id':'deletePatient', 'data-toggle':'modal',
                                             'data-target':'#deletePatientModal', 'type':'button',
                                             'style': 'color:#fff; background-color:#d9534f; border-color:#d43f3a'})


class SessionsForm(FlaskForm):
    patientName = StringField('Patient')
    hiddenField = HiddenField()
    date = StringField('Date', validators=[
        DataRequired()])
    time = TimeField('Time')
    dr = SelectField('Dr', validators=[DataRequired()], render_kw={'class':'form-control'})
    price = StringField('Price')
    details = TextAreaField('details', validators=[
        ], render_kw={'rows': 5})
    edit = SubmitField('Edit')
    submit = SubmitField('Save')
    delete = SubmitField('Delete', render_kw={'id': 'deleteSession', 'data-toggle': 'modal',
                                              'data-target': '#deleteSessionModal', 'type': 'button',
                                              'style': 'color:#fff; background-color:#d9534f; border-color:#d43f3a'})


class UploadPicForm(FlaskForm):
    beforeFile = FileField('Before', render_kw={'multiple': True})
    afterFile = FileField('After', render_kw={'multiple': True})
    submit2 = SubmitField('Submit', render_kw={'class': 'btn btn-default'})

class UserList(FlaskForm):
    myChoices = 'Admin','Doctor','Technician','Receptionist'
    username = StringField('Username', render_kw={'readonly': True, 'class': 'form-control','style':'margin:3px'})
    email = StringField('Email', render_kw={'readonly': True, 'class': 'form-control'})
    level = SelectField('Level', choices=myChoices, validators=[DataRequired()], render_kw={'class':'form-control'})
    delete = SubmitField('Delete', render_kw={'data-toggle': 'modal',
                                              'data-target': '#deleteUserModal', 'type': 'button',
                                              'class': 'btn btn-danger'})


class UserPanel(FlaskForm):
    username = StringField('Username', render_kw={'readonly': True, 'class': 'form-control'})
    users = FieldList(FormField(UserList))




