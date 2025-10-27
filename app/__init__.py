from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = "2758a11282b0bd09fda8271affec592f9c0abd69347e0d6b177921effbbb20b"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)
CORS(app)



from app import routes



