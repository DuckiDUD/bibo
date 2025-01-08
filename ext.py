from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

UPLOAD_FOLDER = '/productIMGS/'

app = Flask(__name__)
app.config["SECRET_KEY"] = "«$±ª޽뱲%ʋ¬¥w®מj+zíz"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
lm = LoginManager(app)