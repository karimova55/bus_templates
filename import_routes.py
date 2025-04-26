import sqlite3
import csv

conn = sqlite3.connect('database/bus.db')
c = conn.cursor()

with open('routes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        c.execute('INSERT INTO routes (number, start_point, end_point) VALUES (?, ?, ?)', 
                  (row['number'], row['start_point'], row['end_point']))

conn.commit()
conn.close()
print("Yo‘nalishlar muvaffaqiyatli qo‘shildi.")