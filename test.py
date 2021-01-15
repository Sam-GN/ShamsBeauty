from app import app, db
from app.models import User, Post

if __name__ == '__main__':
    # u = User(username='john', email='john@example.com')
    # u = User(username='susan', email='susan@example.com')
    # db.session.add(u)
    # db.session.commit()
    users = User.query.all()
    print(users)
    for u in users:
        print(u.id, u.username)
    u = User.query.get(1)
    # p = Post(body='my first post!', author=u)
    # db.session.add(p)
    # db.session.commit()
    for p in u.posts:
        print(p.body)

    # users = User.query.all()
    # for u in users:
    #     db.session.delete(u)
    # posts = Post.query.all()
    # for p in posts:
    #     db.session.delete(p)
    # db.session.commit()