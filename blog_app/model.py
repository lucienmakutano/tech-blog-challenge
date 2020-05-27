try:
    from blog_app import db, login_manager
    from flask_login import UserMixin
    from datetime import datetime
except ModuleNotFoundError:
    print('unable to load the modules')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.TEXT, nullable=False, unique=True)
    password = db.Column(db.TEXT, nullable=True)
    date_created = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    blog = db.relationship('Blog', backref='writer', lazy=True)
    like = db.relationship('Likes', backref='liker', lazy=True)

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.email})'


class Blog(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.TEXT, nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    date_posted = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    author = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    like = db.relationship('Likes', backref='liked', lazy=True)

    def __repr__(self):
        return f'{self.id}, {self.title}, {self.content}, {self.author}'


class Likes(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    like = db.Column(db.INTEGER, default=0, nullable=False)
    blog_id = db.Column(db.INTEGER, db.ForeignKey('blog.id'), nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    date_liked = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())


    def __repr__(self):
        return f'Like({self.like}, {self.blog_id}, {self.user_id})'