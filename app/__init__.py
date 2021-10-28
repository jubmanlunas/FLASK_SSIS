from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['SECRET_KEY'] = '6db52b5de40105e38bb4f3951b7c3303'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gigatt02'
app.config['MYSQL_DB'] = 'ssis_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

from app import ssis_app