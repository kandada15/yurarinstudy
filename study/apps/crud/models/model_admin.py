from apps.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.String(255), primary_key=True)
    admin_name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    birthday = db.Column(db.Date)
    entry_date = db.Column(db.DateTime, default=datetime.now)

    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)