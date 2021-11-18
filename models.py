from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), nullable=False)
    priority = db.Column(db.Integer)
