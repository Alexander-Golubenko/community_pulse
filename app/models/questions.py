from app.models import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    responses = db.relationship("Response", back_populates='question', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, default=1)

    def __repr__(self):
        return f'Question: {self.text}'


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    question = db.relationship('Question', backref=db.backref('statistic', lazy=True))

    def __repr__(self):
        return f'Statistic for Question {self.question_id} : {self.agree_count} agree, {self.disagree_count} disagree>'