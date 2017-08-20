from flask_sqlalchemy import SQLAlchemy
import datetime
from app import db
import random


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    deleted_at = db.Column(db.DateTime, default=None)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    authenticate_token = db.Column(db.String(64))

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }

class Evaluations(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    enrichment = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.Float, nullable=False)

    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def serialize(self, show_deleted_at=False):
        db.session.flush()
        db.session.commit()
        result = {
            'id': self.id,
            'course_code': self.course_code,
            'description': self.description,
            'enrichment': self.enrichment,
            'difficulty': self.difficulty,
            'author': db.session.query(Users).filter_by(id=self.author).first().serialize(),
            'post_time': self.post_time.timestamp() * 1000
        }
        if show_deleted_at:
            result['deleted_at'] = None
            if self.deleted_at is not None:
                result['deleted_at'] = self.deleted_at.timestamp() * 1000
        return result

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    solved = db.Column(db.DateTime, default=None)

    def serialize(self):
        db.session.flush()
        db.session.commit()
        return {
            'id': self.id,
            'evaluation': db.session.query(Evaluations).filter_by(id=self.evaluation_id).first().serialize(show_deleted_at=True),
            'reason': self.reason,
            'author': db.session.query(Users).filter_by(id=self.author).first().serialize(),
            'post_time': self.post_time.timestamp() * 1000,
        }

class CourseBuffer(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    chinese_name = db.Column(db.Text)
    english_name = db.Column(db.Text)
    chinese_description = db.Column(db.Text)
    english_description = db.Column(db.Text)
    credits = db.Column(db.Float)
    hours = db.Column(db.Integer)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    
    u = Users()
    u.email = 'admin@ntut.edu.tw'
    u.password = '8a7b7546e235e2a35776d2cd53ec715e8fb87a60b33d976b3dfff0ac9ba16a2888316b556a841d88076f59952a6b09616ec024cb228d083b7d11bf59d23da190'
    u.is_admin = True
    u.authenticated = True

    db.session.add(u)
    db.session.commit()

    e = Evaluations()
    e.course_code = '3003010'
    e.author = u.id
    e.description = 'Nice Hamburger'
    e.enrichment = 3.7
    e.difficulty = 2.1
    db.session.add(e)

    for i in range(100):
        e = Evaluations()
        e.course_code = '3003010'
        e.author = u.id
        e.description = 'Very Nice Hamburger No.{}'.format(i)
        e.enrichment = round(random.uniform(0, 5),1)
        e.difficulty = round(random.uniform(0, 5),1)
        db.session.add(e)
        db.session.commit()

    r = Reports()
    r.reason = 'Ha Ha\nFunny'
    r.evaluation_id = e.id
    r.author = u.id
    db.session.add(r)
    db.session.commit()
