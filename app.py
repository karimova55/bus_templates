from flask import Flask
from models import db  # db ni import qilish
from admin_routes import admin_bp  # Admin paneli uchun Blueprint

app = Flask(__name__)

# Flask sozlamalarini kiritish
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///routes.db'  # SQLite ma'lumotlar bazasi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db ni Flask ilovasiga ulash
db.init_app(app)

# Blueprint (admin paneli) ni ro‘yxatdan o‘tkazish
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()  # Ma'lumotlar bazasini yaratish

if __name__ == '__main__':
    app.run(debug=True)
