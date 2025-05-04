from flask_sqlalchemy import SQLAlchemy

# db ni yaratish
db = SQLAlchemy()

# Misol uchun bitta model
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Route(id={self.id}, name='{self.name}')>"


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

    def __repr__(self):
        return f"<BusSchedule(id={self.id}, name='{self.name}', departure='{self.departure}', arrival='{self.arrival}')>"



# Flask ishlayotganini tekshirish uchun
if __name__ == "__main__":
    print("models.py loaded successfully")


