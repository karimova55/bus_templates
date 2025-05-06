import sqlite3
import os

# Papkani yaratish (agar mavjud bo'lmasa)
os.makedirs('database', exist_ok=True)

# Barcha ishlar uchun 1 ta baza faylidan foydalanamiz
conn = sqlite3.connect('database/bus_system.db')
c = conn.cursor()

# --- ✅ users jadvali ---
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# --- 1. user_bus_tracking jadvali ---
c.execute('''
CREATE TABLE IF NOT EXISTS user_bus_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    bus_number TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_arrival_minutes INTEGER
)
''')

# --- 2. feedback jadvali ---
c.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL,
    comment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# --- 3. routes jadvali ---
c.execute('DROP TABLE IF EXISTS routes')
c.execute('''
CREATE TABLE routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    start_point TEXT NOT NULL,
    end_point TEXT NOT NULL
)
''')

# --- 4. stops jadvali ---
c.execute('DROP TABLE IF EXISTS stops')
c.execute('''
CREATE TABLE stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    FOREIGN KEY(route_id) REFERENCES routes(id)
)
''')

# --- 5. Yo‘nalishlar qo‘shish ---
routes = [
    ('10', 'Karvon Bozor', 'Poyi Kalon'),
    ('21', 'Bahouddin Naqshband', 'Moxi Xossa'),
    ('35', 'Sitorai Mohi Xossa', 'Markaziy Apteka'),
    ('7', 'Ark Saroyi', 'Kogon Tumani'),
    ('15', 'Gijduvon', 'Karvon Bozor'),
    ('5', 'Samarqand Darvoza', 'Xorazm Ko‘chasi'),
    ('8', 'Kogon Tumani', 'Buxoro Vokzali'),
    ('13', 'Nodir Devonbegi', 'Buxoro Arena'),
    ('2', 'Buxoro Arena', 'Paxtakor ko‘chasi'),
    ('27', 'Buxoro markazi', 'Gulbozor mahallasi')
]
c.executemany('INSERT INTO routes (number, start_point, end_point) VALUES (?, ?, ?)', routes)

# --- 6. route_ids olish ---
conn.commit()
route_ids = {}
for row in c.execute('SELECT id, number FROM routes'):
    route_ids[row[1]] = row[0]

# --- 7. Bekatlar va vaqtlari ---
stops = [
    (route_ids['10'], 'Karvon Bozor', '08:00'),
    (route_ids['10'], 'Lyabi Xovuz', '08:10'),
    (route_ids['10'], 'Poyi Kalon', '08:20'),

    (route_ids['21'], 'Bahouddin Naqshband', '09:00'),
    (route_ids['21'], 'Ark Saroyi', '09:15'),
    (route_ids['21'], 'Moxi Xossa', '09:30'),

    (route_ids['35'], 'Sitorai Mohi Xossa', '07:30'),
    (route_ids['35'], 'Gulbozor', '07:45'),
    (route_ids['35'], 'Markaziy Apteka', '08:00'),

    (route_ids['7'], 'Ark Saroyi', '06:50'),
    (route_ids['7'], "Xo'ja Zayniddin", '07:05'),
    (route_ids['7'], 'Kogon Tumani', '07:20'),

    (route_ids['15'], 'Gijduvon', '06:30'),
    (route_ids['15'], 'Karvon Bozor', '07:00'),

    (route_ids['5'], 'Samarqand Darvoza', '07:10'),
    (route_ids['5'], 'Xorazm Ko‘chasi', '07:30'),

    (route_ids['8'], 'Kogon Tumani', '08:00'),
    (route_ids['8'], 'Paxtakor Ko‘chasi', '08:15'),
    (route_ids['8'], 'Buxoro Vokzali', '08:30'),

    (route_ids['13'], 'Nodir Devonbegi', '09:00'),
    (route_ids['13'], 'Ark Saroyi', '09:15'),
    (route_ids['13'], 'Buxoro Arena', '09:30'),

    (route_ids['2'], 'Buxoro Arena', '06:50'),
    (route_ids['2'], 'Paxtakor ko‘chasi', '07:00'),

    (route_ids['27'], 'Buxoro markazi', '07:40'),
    (route_ids['27'], 'Samarqand darvoza', '07:50'),
    (route_ids['27'], 'Gulbozor mahallasi', '08:05')
]
c.executemany('INSERT INTO stops (route_id, name, arrival_time) VALUES (?, ?, ?)', stops)

# --- Yakunlash ---
conn.commit()
conn.close()

print("✅ Barcha jadvallar (shu jumladan users) yaratildi va maʼlumotlar qo‘shildi.")
