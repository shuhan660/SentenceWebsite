from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(30), unique=True, nullable=False)

    name = db.Column(db.String(50), nullable=False)

    gender = db.Column(db.String(10), nullable=False)

    region = db.Column(db.String(10), nullable=False)


class Sentence(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    region = db.Column(db.String(10), nullable=False)

    gender = db.Column(db.String(10), nullable=False)

    content = db.Column(db.Text, nullable=False)

    selected = db.Column(db.Boolean, default=False)

    selected_by = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=True)


class Selection(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer,
                           db.ForeignKey("student.id"))

    sentence_id = db.Column(db.Integer,
                            db.ForeignKey("sentence.id"))

    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)