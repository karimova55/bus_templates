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
from flask import Flask, render_template, request, redirect, url_for 
import sqlite3 
import os
app=Flask(__name__)

db_path = 'database/bus.db'
os.makedirs('database', exist_ok=True)
    
def init_db(): 
    conn = sqlite3.connect(db_path) 
    c = conn.cursor() 
    
    # 1. routes jadvali – avtobus yo‘nalishlari
    c.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            start_point TEXT,
            end_point TEXT
        )
    ''')
    # Stop schedules table
    c.execute('''CREATE TABLE IF NOT EXISTS stop_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        stop_id INTEGER,
        arrival_time TEXT,
        FOREIGN KEY(route_id) REFERENCES routes(id),
        FOREIGN KEY(stop_id) REFERENCES stops(id)
    )''')

    # 2. stops jadvali – har bir yo‘nalishdagi bekatlar
    c.execute('''
        CREATE TABLE IF NOT EXISTS stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER,
            stop_name TEXT,
            stop_order INTEGER,
            FOREIGN KEY(route_id) REFERENCES routes(id)
        )
    ''')

    # 3. schedules jadvali – har bir yo‘nalishning vaqt jadvali
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            interval INTEGER,
            FOREIGN KEY(route_id) REFERENCES routes(id)
        )
    ''')

    conn.commit()
    conn.close()
#Run database init on start
init_db()

#---- ROUTES: MAIN -----
@app.route('/') 
def index(): 
    conn = sqlite3.connect(db_path) 
    c = conn.cursor() 
    c.execute('SELECT * FROM routes') 
    routes = c.fetchall() 
    conn.close() 
    return render_template('index.html', routes=routes)

@app.route('/add-route', methods=['GET', 'POST']) 
def add_route(): 
    if request.method == 'POST': 
        number = request.form['number'] 
        start_point = request.form['start_point'] 
        end_point = request.form['end_point'] 
        conn = sqlite3.connect(db_path) 
        c = conn.cursor() 
        c.execute('INSERT INTO routes (number, start_point, end_point) VALUES (?, ?, ?)', (number, start_point, end_point)) 
        conn.commit() 
        conn.close() 
        return redirect(url_for('index')) 
    return render_template('add_route.html')

@app.route('/edit-route/<int:route_id>', methods=['GET', 'POST']) 
def edit_route(route_id): 
    conn = sqlite3.connect(db_path) 
    c = conn.cursor() 
    if request.method == 'POST': 
        number = request.form['number'] 
        start_point = request.form['start_point'] 
        end_point = request.form['end_point'] 
        c.execute('UPDATE routes SET number=?, start_point=?, end_point=? WHERE id=?', (number, start_point, end_point, route_id)) 
        conn.commit() 
        conn.close() 
        return redirect(url_for('index'))
    c.execute('SELECT * FROM routes WHERE id=?', (route_id,)) 
    route = c.fetchone() 
    conn.close() 
    return render_template('edit_route.html', route=route)


@app.route('/add-stop/<int:route_id>', methods=['GET', 'POST'])
def add_stop(route_id):
    if request.method == 'POST':
        stop_name = request.form['stop_name']
        stop_order = request.form['stop_order']
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO stops (route_id, stop_name, stop_order) VALUES (?, ?, ?)',
                  (route_id, stop_name, stop_order))
        conn.commit()
        conn.close()
        return redirect(url_for('view_route_stops', route_id=route_id))
    return render_template('add_stop.html', route_id=route_id)


@app.route('/route/<int:route_id>/stops')
def view_route_stops(route_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM stops WHERE route_id = ? ORDER BY stop_order', (route_id,))
    stops = c.fetchall()
    conn.close()
    return render_template('view_stops.html', stops=stops, route_id=route_id)


@app.route('/route/<int:route_id>/stop-schedules', methods=['GET', 'POST'])
def view_stop_schedule(route_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if request.method == 'POST':
        stop_id = request.form['stop_id']
        arrival_time = request.form['arrival_time']
        c.execute('INSERT INTO stop_schedules (route_id, stop_id, arrival_time) VALUES (?, ?, ?)',
                  (route_id, stop_id, arrival_time))
        conn.commit()

    # Bekatlar va vaqtlar
    c.execute('SELECT stops.id, stops.stop_name, ss.arrival_time FROM stops LEFT JOIN stop_schedules ss ON stops.id = ss.stop_id AND ss.route_id = ? WHERE stops.route_id = ?', (route_id, route_id))
    stops = c.fetchall()

    conn.close()
    return render_template('stop_schedule.html', route_id=route_id, stops=stops)


@app.route('/delete-route/<int:route_id>') 
def delete_route(route_id): 
    conn = sqlite3.connect(db_path) 
    c = conn.cursor() 
    c.execute('DELETE FROM routes WHERE id=?', (route_id,)) 
    c.execute('DELETE FROM stops WHERE route_id=?', (route_id,)) 
    c.execute('DELETE FROM schedules WHERE route_id=?', (route_id,)) 
    conn.commit() 
    conn.close() 
    return redirect(url_for('index'))

@app.route('/stops/<int:route_id>')
def stops(route_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM stops WHERE route_id = ? ORDER BY stop_order', (route_id,))
    stops = c.fetchall()
    conn.close()
    return render_template('stops.html', stops=stops, route_id=route_id)

@app.route('/')
def index():
    return render_template('index.html')


if __name__=='__main__': 
    app.run(debug=True)
