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
