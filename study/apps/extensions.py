from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# db と csrf をここで作ります
db = SQLAlchemy()
csrf = CSRFProtect()