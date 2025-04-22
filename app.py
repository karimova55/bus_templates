from flask import Flask
<<<<<<< HEAD
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
=======
from routes import register_routes
from models import db  # db importini faqat bitta joyda amalga oshiramiz

app = Flask(__name__)

# Ma’lumotlar bazasi sozlamalari
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Marshrutlarni ro‘yxatdan o‘tkazamiz
register_routes(app)
>>>>>>> 24c6d7d3d28ff89761d3d6d74b54eec3126132f0

if __name__ == '__main__':
    app.run(debug=True)
