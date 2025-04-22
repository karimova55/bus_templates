from flask import request, jsonify
from models import db, BusSchedule

def register_routes(app):
    @app.route('/')
    def home():
        return "Avtobus jadvali API ishlayapti"

    @app.route('/routes')
    def all_routes():
        routes = BusSchedule.query.all()
        return jsonify([r.to_dict() for r in routes])

    @app.route('/timetable/<int:route_id>')
    def timetable(route_id):
        route = BusSchedule.query.get(route_id)
        if route:
            return jsonify(route.to_dict())
        return jsonify({'error': 'Topilmadi'}), 404

    @app.route('/search')
    def search():
        q = request.args.get('q')
        results = BusSchedule.query.filter(BusSchedule.name.contains(q)).all()
        return jsonify([r.to_dict() for r in results])
