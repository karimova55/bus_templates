from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguratsiya
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

# Modellar
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    start_point = db.Column(db.String(100), nullable=False)
    end_point = db.Column(db.String(100), nullable=False)
    stops = db.relationship('Stop', backref='route', cascade="all, delete-orphan")

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)

# Bazani yaratish
with app.app_context():
    db.create_all()

# Marshrutlar

@app.route('/')
def index():
    routes = Route.query.all()
    return render_template('index.html', routes=routes)

@app.route('/add-route', methods=['GET', 'POST'])
def add_route():
    if request.method == 'POST':
        number = request.form['number']
        start_point = request.form['start_point']
        end_point = request.form['end_point']
        route = Route(number=number, start_point=start_point, end_point=end_point)
        db.session.add(route)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_route.html')

@app.route('/edit-route/<int:route_id>', methods=['GET', 'POST'])
def edit_route(route_id):
    route = Route.query.get_or_404(route_id)
    if request.method == 'POST':
        route.number = request.form['number']
        route.start_point = request.form['start_point']
        route.end_point = request.form['end_point']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_route.html', route=route)

@app.route('/delete-route/<int:route_id>')
def delete_route(route_id):
    route = Route.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/route/<int:route_id>/stops')
def view_stops(route_id):
    route = Route.query.get_or_404(route_id)
    stops = Stop.query.filter_by(route_id=route_id).order_by(Stop.stop_order).all()
    return render_template('view_stops.html', route=route, stops=stops)

@app.route('/add-stop/<int:route_id>', methods=['GET', 'POST'])
def add_stop(route_id):
    route = Route.query.get_or_404(route_id)
    if request.method == 'POST':
        stop_name = request.form['stop_name']
        stop_order = int(request.form['stop_order'])
        stop = Stop(route_id=route_id, stop_name=stop_name, stop_order=stop_order)
        db.session.add(stop)
        db.session.commit()
        return redirect(url_for('view_stops', route_id=route_id))
    return render_template('add_stop.html', route=route)

# Dastur ishga tushishi
if __name__ == '__main__':
    app.run(debug=True)

