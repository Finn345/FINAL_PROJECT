from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable=False, default='')
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(), unique=True, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project = db.relationship('Project', backref='owner', lazy=True)
    
    def __init__(self, email='', first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.token = self.set_token(10)
        self.g_auth_verify = g_auth_verify
        
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"Thanks for signing up {self.first_name}! Welcome to my website! - {self.date_created}"
    
class Project(db.Model):
    id = db.Column(db.String, primary_key=True)
    name=db.Column(db.String(150), nullable=False, default='')
    description = db.Column(db.String(150), nullable=False, default='')
    lang_to_use = db.Column(db.String(150), nullable=False, default='')
    nums_of_lines_allowed = db.Column(db.Integer, nullable=False, default=0)
    user_token = db.Column(db.String, db.ForeignKey(User.token), nullable=False)
    
    def __init__(self, name, description, lang_to_use, num_of_lines_allowed, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.lang_to_use = lang_to_use
        self.num_of_lines_allowed = num_of_lines_allowed
        self.user_token = user_token
        
    def __repr__(self):
        return f"You added the following project: {self.name}"
        
    def set_id(self):
        return(secrets.token_urlsafe())

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'lang_to_use', 'num_of_lines_allowed']
        
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)