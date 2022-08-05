from flask import Flask,session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from flask_session import Session
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mainserver'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2a6a7ffc3bf3427d970429f02e2f0c15' 
db = SQLAlchemy(app)
migrate = Migrate(app,db)
csrf=CSRFProtect(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app) 
ckeditor = CKEditor(app)


from main import routes
from main import sellerRoutes


