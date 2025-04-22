<<<<<<< HEAD
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
=======
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # faqat bitta joyda db ni yaratamiz

class BusSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    departure = db.Column(db.String(100))
    arrival = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'departure': self.departure,
            'arrival': self.arrival
        }
>>>>>>> 24c6d7d3d28ff89761d3d6d74b54eec3126132f0
