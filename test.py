from app import app, db, jdatetime
from app.models import User, Patient, Session

if __name__ == '__main__':
    # u = User(username='john', email='john@example.com')
    # u = User(username='susan', email='susan@example.com')
    # db.session.add(u)
    # db.session.commit()
     sessions = Session.query.all()


     for u in sessions:
         print(u.imageString)
    # u = User.query.get(1)
    # p = Post(body='my first post!', author=u)
    # db.session.add(p)
    # db.session.commit()
    # for p in u.posts:
    #     print(p.body)

    # users = User.query.all()
    # for u in users:
    #     db.session.delete(u)
    # posts = Post.query.all()
    # for p in posts:
    #     db.session.delete(p)
    # db.session.commit()

    # patient = Patient(name='Sam', tel='123456789')
    # patient2 = Patient(name='Sam2', tel='123456789', referer='Sam')
    # patient3 = Patient(name='Sam3', tel='123456789', referer='Sam2')
    # patient4 = Patient(name='Sam4', tel='123456789', referer='Sam3')
    # patient5 = Patient(name='Sam5', tel='123456789', referer='Sam4')
    # patient6 = Patient(name='Sam6', tel='123456789', referer='Sam5')
    # patient7 = Patient(name='Sam7', tel='123456789', referer='Sam5')
    # db.session.add(patient)
    # db.session.add(patient2)
    # db.session.add(patient3)
    # db.session.add(patient4)
    # db.session.add(patient5)
    # db.session.add(patient6)
    # db.session.add(patient7)
    # db.session.commit()
    # patients = Patient.query.all()
    # print(patients)

    # print(jdatetime.datetime.now())
    # session = Session.query.first()
    # print(session.time)
    # print(jdatetime.date.fromgregorian(date= session.sessionDate))
    # print(jdatetime.date.togregorian(jdatetime.datetime.now()))
