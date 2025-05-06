
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'


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
=======
# Ro'yxatdan o'tish sahifasi
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Bazaga ulanish
        conn = sqlite3.connect('database/bus_system.db')
        cursor = conn.cursor()

        try:
            # Foydalanuvchini bazaga qo‘shish
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            # Ro‘yxatdan o‘tgandan keyin login sahifasiga yo‘naltirish
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # Agar foydalanuvchi nomi allaqachon bo‘lsa, xato xabarini ko‘rsatish
            error_message = "Bu foydalanuvchi nomi allaqachon mavjud."
            return render_template('signup.html', error_message=error_message)
        finally:
            conn.close()

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Bazaga ulanish
        conn = sqlite3.connect('database/bus_system.db')
        cursor = conn.cursor()

        try:
            # Foydalanuvchini tekshirish
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                # Foydalanuvchi topildi, session yaratish va dashboard sahifasiga yo‘naltirish
                session['user_id'] = user[0]  # Foydalanuvchi ID sini saqlash
                session['username'] = user[1]  # Foydalanuvchi nomini saqlash
                return redirect(url_for('dashboard'))  # Dashboard sahifasiga yo‘naltirish
            else:
                # Foydalanuvchi topilmadi, xato xabarini ko‘rsatish
                error_message = "Foydalanuvchi nomi yoki parol noto‘g‘ri."
                return render_template('login.html', error_message=error_message)

        except Exception as e:
            # Agar xatolik bo‘lsa, uni loglash yoki boshqa tarzda ko‘rsatish
            error_message = "Serverda xatolik yuz berdi. Iltimos, keyinroq qaytib keling."
            return render_template('login.html', error_message=error_message)
        
        finally:
            # Ulanishni yopish
            conn.close()

    return render_template('login.html')



# @app.route('/dashboard')
# def dashboard():
#     # Agar foydalanuvchi tizimga kirgan bo'lsa, dashboard sahifasini ko'rsatish
#     if 'user_id' in session:
#         return render_template('dashboard.html', username=session['username'])
#     else:
#         return redirect(url_for('login'))  # Tizimga kirmagan foydalanuvchini kirish sahifasiga yuborish
@app.route('/logout')
def logout():
    session.clear()  # Barcha session ma'lumotlarini tozalash
    return redirect(url_for('login'))  # Login sahifasiga yo‘naltirish



# Ma'lumotlar bazasi fayli
db_path = 'database/bus.db'
os.makedirs('database', exist_ok=True)

# Ma'lumotlar bazasini yaratish va boshlash
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
    conn.commit()
    conn.close()

# Ma'lumotlar bazasini boshlash
init_db()

# Yo‘nalishlar va bekatlar
routes = [
    (1, "1", "Karvon Bozor", "Minor masjidi"),
    (2, "2", "Ark Qal'asi", "Gijduvon yo‘li"),
    (3, "3", "Buxoro Vokzal", "Bahouddin Naqshband"),
    (4, "4", "Chor Minor", "Namozgoh maydoni")
]

# Bekatlar va vaqtlari
schedules = {
    1: [
        ("Karvon Bozor", "08:00"),
        ("Markaziy Apteka", "08:10"),
        ("Labihovuz", "08:15"),
        ("Nodir Devonbegi", "08:20"),
        ("Minor masjidi", "08:30"),
    ],
    2: [
        ("Ark Qal'asi", "09:00"),
        ("Nasriddin Afandi haykali", "09:10"),
        ("Poytaxt ko‘chasi", "09:20"),
        ("Guliston ko'chasi", "09:30"),
        ("Gijduvon yo‘li", "09:40"),
    ],
    3: [
        ("Buxoro Vokzal", "07:30"),
        ("Bozori Kord", "07:40"),
        ("Markaziy Apteka", "07:50"),
        ("Sitorai Mohi Xossa Saroyi", "08:00"),
        ("Bahouddin Naqshband", "08:10"),
    ],
    4: [
        ("Chor Minor", "07:00"),
        ("Nodir Devonbegi", "07:10"),
        ("Labihovuz", "07:20"),
        ("Ko‘hna Ark", "07:25"),
        ("Namozgoh maydoni", "07:30"),
    ]
}

# Avtobusga chiqishni belgilash
@app.route('/select-bus', methods=['GET', 'POST'])
def select_bus():
    if 'user_id' not in session:
        flash('Avval ro‘yxatdan o‘ting yoki kiring.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        bus_number = request.form['bus_number']
        estimated_minutes = int(request.form['estimated_minutes'])

        conn = sqlite3.connect('database/bus_system.db')
        c = conn.cursor()
        c.execute('INSERT INTO user_bus_tracking (username, bus_number, estimated_arrival_minutes) VALUES (?, ?, ?)',
                  (session['username'], bus_number, estimated_minutes))
        conn.commit()
        conn.close()

        flash(f'{bus_number} raqamli avtobus tanlandi. Manzilga {estimated_minutes} daqiqada yetasiz.', 'success')
        return redirect(url_for('track_journey'))

    # Barcha avtobuslar ro'yxatini olish uchun
    conn = sqlite3.connect('database/bus_system.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT number FROM routes')
    buses = [row[0] for row in c.fetchall()]
    conn.close()

    return render_template('select_bus.html', buses=buses)

# Avtobusdagi safarni kuzatish
@app.route('/track-journey')
def track_journey():
    if 'user_id' not in session:
        flash('Avval ro‘yxatdan o‘ting yoki kiring.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('database/bus_system.db')
    c = conn.cursor()
    c.execute('SELECT bus_number, start_time, estimated_arrival_minutes FROM user_bus_tracking WHERE username = ? ORDER BY id DESC LIMIT 1', (session['username'],))
    data = c.fetchone()
    conn.close()

    if not data:
        flash('Siz hali hech qanday avtobusni tanlamagansiz.', 'info')
        return redirect(url_for('select_bus'))

    bus_number, start_time, estimated_arrival_minutes = data

    # Hozirgi vaqt
    start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    elapsed_minutes = int((datetime.now() - start_time_dt).total_seconds() // 60)
    remaining_minutes = max(estimated_arrival_minutes - elapsed_minutes, 0)

    arrived = remaining_minutes == 0

    return render_template('track_journey.html', bus_number=bus_number, remaining_minutes=remaining_minutes, arrived=arrived)

@app.route('/choose-bus', methods=['GET', 'POST'])
def choose_bus():
    conn = sqlite3.connect('database/bus.db')
    c = conn.cursor()
    c.execute('SELECT * FROM routes')
    routes = c.fetchall()
    conn.close()

    estimated_time = None

    if request.method == 'POST':
        bus_number = request.form['bus_number']
        # Demak, har bir safar uchun bazaviy vaqt (masalan, 20 daqiqa) o'ylab topamiz
        base_minutes = random.randint(15, 30)  # Realistik vaqt oralig'i
        estimated_time = simulate_traffic_delay(base_minutes)

    return render_template('choose_bus.html', routes=routes, estimated_time=estimated_time)


def simulate_traffic_delay(base_minutes):
    """Safar vaqtini tirbandlik sharoitida realdek o'zgartiradi."""
    delay = random.randint(-3, 10)  # -3 daqiqa tezroq, 10 daqiqa sekinroq bo'lishi mumkin
    updated_time = max(base_minutes + delay, 1)  # Vaqt hech qachon 0 dan kichik bo'lmaydi
    return updated_time


@app.route('/track/<int:route_id>')
def track(route_id):
    conn = sqlite3.connect('database/bus.db')
    c = conn.cursor()

    c.execute("SELECT number FROM routes WHERE id = ?", (route_id,))
    route = c.fetchone()

    c.execute("SELECT name FROM stops WHERE route_id = ? ORDER BY stop_order", (route_id,))
    stops = [s[0] for s in c.fetchall()]
    conn.close()

    import random
    current_idx = random.randint(0, len(stops) - 2)
    next_idx = current_idx + 1
    time_left = random.randint(3, 15)
    progress = int((current_idx / len(stops)) * 100)

    return render_template('bus_status.html',
                           route_number=route[0],
                           current_stop=stops[current_idx],
                           next_stop=stops[next_idx],
                           time_left=time_left,
                           progress=progress)


@app.route('/feedback', methods=['POST'])
def feedback():
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    print(f"Foydalanuvchi bahosi: {rating}, Izohi: {comment}")
    flash("Fikringiz uchun rahmat!", "success")
    return redirect(url_for('index'))



# Aniq yo‘nalishlarni ko‘rsatish
@app.route('/')
def index():
    return render_template('index.html', routes=routes)

# Yo‘nalish qo‘shish
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        destination = request.form.get('destination')
        
        # Qidiruvni amalga oshirish
        results = find_routes(destination)  # find_routes - bu qidiruv funktsiyasi
        return render_template('search.html', results=results)
    
    return render_template('search.html', results=None)

def find_routes(destination):
    # Bu erda manzillarni qidirish uchun kerakli logika bo'ladi.
    # Misol uchun, qidiruv natijalarini hardkodlash:
    routes = [
        ("12", "Karvon Bozor", "10:30"),
        ("24", "Markaziy Apteka", "10:45"),
        ("18", "Moxi Xossa", "11:00"),
    ]
    
    # Faqat mos keluvchi natijalarni qaytarish
    return [route for route in routes if destination.lower() in route[1].lower()]

@app.route('/tracking')
def bus_tracking():
    return render_template('bus_tracking.html')

@app.route('/api/tracking-data')
def tracking_data():
    conn = sqlite3.connect('bus.db')
    c = conn.cursor()

    c.execute('SELECT id, number, start_point, end_point FROM routes')
    routes = c.fetchall()

    avtobuslar = []
    for route in routes:
        route_id, number, start_point, end_point = route
        c.execute('SELECT name FROM stops WHERE route_id = ?', (route_id,))
        stops = [row[0] for row in c.fetchall()]

        if stops:
            current_stop = random.choice(stops)
            traffic_status = random.choice(['Normal', 'Tirbandlik'])
            now = datetime.now()
            delay_minutes = random.choice([0, 3, 5]) if traffic_status == 'Tirbandlik' else 0
            arrival_time = (now + timedelta(minutes=delay_minutes)).strftime('%H:%M')

            avtobuslar.append({
                'number': number,
                'current_stop': current_stop,
                'traffic_status': traffic_status,
                'arrival_time': arrival_time,
                'start_point': start_point,
                'end_point': end_point
            })

    conn.close()
    return jsonify(avtobuslar)
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

# Yo‘nalish va bekatlar ro‘yxati
@app.route('/route/<int:route_id>/stops')
def view_route_stops(route_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM stops WHERE route_id = ? ORDER BY stop_order', (route_id,))
    stops = c.fetchall()
    conn.close()
    return render_template('view_stops.html', stops=stops, route_id=route_id)

# Bekatlar va vaqtlari
@app.route('/route/<int:route_id>/schedule')
def view_route_schedule(route_id):
    schedule_list = schedules.get(route_id, [])
    return render_template('view_schedule.html', schedule_list=schedule_list, route_id=route_id)

@app.route('/submit-feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        satisfaction = request.form['satisfaction']
        driver_rating = request.form['driver_rating']
        bus_condition = request.form['bus_condition']
        comments = request.form['comments']

        # Fikrlarni bazaga saqlash (sqlite)
        conn = sqlite3.connect('bus_database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                satisfaction TEXT,
                driver_rating TEXT,
                bus_condition TEXT,
                comments TEXT
            )
        ''')
        c.execute('''
            INSERT INTO feedback (satisfaction, driver_rating, bus_condition, comments)
            VALUES (?, ?, ?, ?)
        ''', (satisfaction, driver_rating, bus_condition, comments))
        conn.commit()
        conn.close()

        return redirect(url_for('thank_you'))  # Fikr yuborilgandan keyin "Rahmat" sahifasiga yo‘naltiramiz

    return render_template('feedback.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/view-feedback')
def view_feedback():
    conn = sqlite3.connect('bus_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    feedbacks = c.fetchall()
    conn.close()

    return render_template('view_feedback.html', feedbacks=feedbacks)



# Saytdan chiqish
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

if __name__ == '__main__':
    app.run(debug=True)

