from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from flask_login import UserMixin

from FlaskRTBCTF import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Table


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(88), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    logs = db.relationship("Logs", backref="user", lazy=True, uselist=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'))"


# Logging Table


class Logs(db.Model):
    __tablename__ = "logs"
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True
    )
    accountCreationTime = db.Column(db.DateTime, nullable=False)
    visitedMachine = db.Column(db.Boolean, default=False)
    machineVisitTime = db.Column(db.DateTime, nullable=True)
    userSubmissionTime = db.Column(db.DateTime, nullable=True)
    rootSubmissionTime = db.Column(db.DateTime, nullable=True)
    userOwnTime = db.Column(db.String, nullable=True)
    rootOwnTime = db.Column(db.String, nullable=True)
    userSubmissionIP = db.Column(db.String, nullable=True)
    rootSubmissionIP = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"Logs('{self.user_id}','{self.visitedMachine}'"