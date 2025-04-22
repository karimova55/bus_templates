from flask import Flask
from routes import register_routes
from models import db  # db importini faqat bitta joyda amalga oshiramiz

app = Flask(__name__)

# Ma’lumotlar bazasi sozlamalari
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Marshrutlarni ro‘yxatdan o‘tkazamiz
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
