from flask import render_template, flash, redirect, url_for, send_from_directory
from app import app, helper
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User
from flask import request, abort
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.models import Post
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
from app.forms import PatientForm, PatientFormSessionList
from app.models import Patient
from app.forms import SessionsForm, UploadPicForm
from app.models import Session
import os
import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.txt', form=form)


@app.route('/patient_form/<id>', methods=['GET', 'POST'])
@login_required
def patient_form(id):
    isNew = False
    patientID = id
    if patientID != '-1':
        patient = db.session.query(Patient).get(patientID)
        sessions = Session.query.filter_by(patient_id=patientID).all()

        form = PatientForm(name=patient.name, tel=patient.tel, firstVisit=patient.firstVisit, referer=patient.referer)
        form2 = PatientFormSessionList(sessions=sessions)
        form.name.render_kw = {'readonly': True}
        form.tel.render_kw = {'readonly': True}
        form.referer.render_kw = {'readonly': True}
        form.submit.render_kw = {'readonly': True}
        form.submit.render_kw = {'disabled': True}
        for items in form2.sessions.entries:
            items.render_kw = {
                'onclick': "location.href='" + url_for('session_form', id=patientID, sid=items.data.id) + "'",
                'type': 'button'}

    else:
        form = PatientForm()
        form2 = PatientFormSessionList()
        isNew = True
        form.edit.render_kw = {'disabled': True}
        form.createSession.render_kw = {'disabled': True}

    if form.validate_on_submit():
        if form.submit.data:
            if isNew:
                patient = Patient(name=form.name.data, tel=form.tel.data,
                                  referer=form.referer.data)
                db.session.add(patient)
                db.session.flush()
                patientID = patient.id
                db.session.commit()
                return redirect(url_for('patient_form', id=patientID))
            else:
                patient = db.session.query(Patient).get(patientID)
                patient.name = form.name.data
                patient.tel = form.tel.data
                patient.referer = form.referer.data
                db.session.commit()
                flash('Patient data saved')
                return redirect(url_for('patient_form', id=patientID))

        elif form.createSession.data:
            return redirect(url_for('session_form', id=patientID, sid=-1))
        elif form.edit.data:
            form.name.render_kw = {'readonly': False}
            form.tel.render_kw = {'readonly': False}
            form.referer.render_kw = {'readonly': False}
            form.edit.render_kw = {'disabled': True}
            form.createSession.render_kw = {'disabled': True}
            form.submit.render_kw = {'disabled': False}
            if not isNew:
                form.name = 'asghar'

        # patient = db.session.query(Patient).get(patientId)
        # flash(patient.name)
    return render_template('patient_form.html', title='Patient Form', form=form, form2=form2)


@app.route('/session_form/<id>,<sid>', methods=['GET', 'POST'])
@login_required
def session_form(id, sid):
    patientID = id
    sessionID = sid
    isNew = False
    patient = db.session.query(Patient).get(patientID)
    if sessionID == '-1':
        isNew = True
        form = SessionsForm(patientName=patient.name)
    else:
        session = db.session.query(Session).get(sessionID)
        form = SessionsForm(patientName=patient.name, date=session.jalali(), time=session.sessionDate
                            , dr=session.user_id, details=session.detail)
        form.date.render_kw = {'disabled': True}
        form.time.render_kw = {'disabled': True}
        form.dr.render_kw = {'readonly': True}
        form.details.render_kw = {'readonly': True}
        form.submit.render_kw = {'disabled': True}
        form.edit.render_kw = {'disabled': False}
    form.patientName.render_kw = {'onclick': "location.href='" + url_for('patient_form', id=patientID) + "'",
                                  'type': 'button'}

    files = os.listdir(app.config['UPLOAD_PATH'])
    filesBefore = list(filter(lambda x: ((str(sessionID) + '_before') in x), files))
    filesAfter = list(filter(lambda x: ((str(sessionID) + '_after') in x), files))
    picForm = UploadPicForm()
    if picForm.validate_on_submit():
        if picForm.submit2.data:
            i = 0
            for uploaded_file in request.files.getlist('beforeFile'):
                filename = secure_filename(uploaded_file.filename)
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                            file_ext != helper.validate_image(uploaded_file.stream):
                        abort(400)
                    fileName = os.path.join(app.config['UPLOAD_PATH'],
                                                    sessionID + '_before_' + datetime.datetime.now().strftime(
                                                        "%Y-%m-%d %H-%M-%S_") + str(i) + file_ext)
                    uploaded_file.save(fileName)
                    helper.resizePic(fileName)
                    i = i + 1
                    flash('Picture added')
            for uploaded_file in request.files.getlist('afterFile'):
                filename = secure_filename(uploaded_file.filename)
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                            file_ext != helper.validate_image(uploaded_file.stream):
                        abort(400)

                    fileName = os.path.join(app.config['UPLOAD_PATH'],
                                            sessionID + '_after_' + datetime.datetime.now().strftime(
                                                "%Y-%m-%d %H-%M-%S_") + str(i) + file_ext)
                    uploaded_file.save(fileName)
                    helper.resizePic(fileName)
                    i = i + 1
                    flash('Picture added')
            return redirect(url_for('session_form', id=patientID, sid=sessionID))

    if form.validate_on_submit():
        if form.submit.data:
            if isNew:
                session = Session(patient_id=patientID, user_id=form.dr.data,
                                  detail=form.details.data,
                                  sessionDate=helper.covertJalaliToGeregorain(form.date.data, form.time.data))
                db.session.add(session)
                db.session.flush()
                sessionID = session.id
                db.session.commit()
                flash('Reservation saved')
                return redirect(url_for('session_form', id=patientID, sid=sessionID))
            else:
                session.sessionDate = helper.covertJalaliToGeregorain(form.date.data, form.time.data)
                session.user_id = form.dr.data
                session.detail = form.details.data
                db.session.commit()
                flash('Reservation Saved')

        if form.edit.data:
            form.date.render_kw = {'readonly': False}
            form.time.render_kw = {'readonly': False}
            form.dr.render_kw = {'readonly': False}
            form.details.render_kw = {'readonly': False}
            form.submit.render_kw = {'disabled': False}
            form.edit.render_kw = {'disabled': True}

    return render_template('session_form.html', title='Session Form', form=form, form2=picForm, filesBefore=filesBefore,
                           filesAfter=filesAfter)


@app.route('/delete_pic')
@login_required
def delete_pic():
    filename = request.args.get('filename', "", type=str)
    print(filename[9:])
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename[9:]))
    flash('Picture deleted')
    return " "


@app.route('/uploads/<filename>')
@login_required
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)


@app.route('/patient_list', methods=['GET', 'POST'])
@login_required
def patient_list():
    return getPatients('general')


@app.route('/patient_list_ajax', methods=['GET', 'POST'])
@login_required
def patient_list_ajax():
    return getPatients('ajax')


def getPatients(mode):
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', "", type=str)

    if search != '':
        patients = Patient.query.filter(Patient.name.like("%{}%".format(search))).order_by(
            Patient.name.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    else:
        patients = Patient.query.order_by(
            Patient.name.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('patient_list', page=patients.next_num, search=search) \
        if patients.has_next else None
    prev_url = url_for('patient_list', page=patients.prev_num, search=search) \
        if patients.has_prev else None

    if mode == 'general':
        return render_template('patient_list.html', title='Patients',
                               patients=patients.items, next_url=next_url,
                               prev_url=prev_url, search=search)
    elif mode == 'ajax':
        return render_template('patient_list_ajax.html', title='Patients',
                               patients=patients.items, next_url=next_url,
                               prev_url=prev_url, search=search)


@app.route('/session_list', methods=['GET', 'POST'])
@login_required
def session_list():
    return getSessions('general')


@app.route('/session_list_ajax', methods=['GET', 'POST'])
@login_required
def session_list_ajax():
    return getSessions('ajax')


def getSessions(mode):
    search = request.args.get('search', "", type=str)
    page = request.args.get('page', 1, type=int)
    print(search)
    if search != '':
        sessions = db.session.query(Session).join(Session.name).filter(Patient.name.like("%{}%".format(search))). \
            order_by(Session.sessionDate.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
        # sessions = Session.query(Session).filter(Session.detail.like("%{}%".format(search))).order_by(
        #     Session.sessionDate.desc()).paginate(
        #     page, app.config['POSTS_PER_PAGE'], False)
    else:
        sessions = Session.query.order_by(
            Session.sessionDate.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('session_list', page=sessions.next_num) \
        if sessions.has_next else None
    prev_url = url_for('session_list', page=sessions.prev_num) \
        if sessions.has_prev else None
    if mode == 'general':
        return render_template('session_list.html', title='Sessions',
                               sessions=sessions.items, next_url=next_url,
                               prev_url=prev_url, search=search)
    elif mode == 'ajax':
        return render_template('session_list_ajax.html', title='Sessions',
                               sessions=sessions.items, next_url=next_url,
                               prev_url=prev_url, search=search)
