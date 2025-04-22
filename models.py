# models.py
from flask_sqlalchemy import SQLAlchemy

# db ni yaratish
db = SQLAlchemy()

# Misol uchun bitta model
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

# Flask ishlayotganini tekshirish uchun
if __name__ == "__main__":
    print("db object initialized successfully")
