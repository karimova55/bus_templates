# 🚌 Avtobuslar Jadvali - Flask Web Ilova

**Muallif:** Muslima  
**Jamoa a'zolari:**  
- Muslima – Backend (Flask ilova, routing, API yozish)  
- Dilnoza – Frontend (HTML/CSS/JS bilan sahifa dizayni)  
- Shaxrizoda – Ma'lumotlar (Yo'nalishlar va jadval ma'lumotlarini tayyorlash)  
- Sabina – Admin panel va test mas'uli (CRUD, testlar, interfeys dizayni)

---

## 📌 Loyiha tavsifi

Ushbu loyiha — shahardagi **avtobuslar yo‘nalishlari va ularning jadvalini** ko‘rsatadigan web ilovadir. Flask asosida ishlab chiqilgan va foydalanuvchilarga qulay, oddiy interfeys orqali kerakli yo‘nalish va vaqt ma'lumotlarini izlash imkonini beradi.

---

## 🚀 Ishga tushirish

1. Loyihani yuklab oling:
```bash
git clone https://github.com/username/bus_templates.git
cd bus_templates
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

3. Talab qilinadigan kutubxonalarni o‘rnatish:
```bash
pip install -r requirements.txt
```

4. Dastur bazasini yaratish:
```bash
python create_db.py
```

5. Ilovani ishga tushurish:
```bash
python app.py
```

---

## 🔍 Asosiy imkoniyatlar

- Yo‘nalishlar ro‘yxati ( `/routes` )
- Har bir yo‘nalish uchun jadval ( `/timetable/<id>` )
- Qidiruv ( `/search?q=...` )
- Admin panel orqali CRUD amallar (yo‘nalish va jadval qo‘shish/o‘chirish)

---

## 🌐 Texnologiyalar

- Python (Flask)
- HTML, CSS, JavaScript
- SQLite (SQLAlchemy bilan)
- Bootstrap (Admin interfeys)

---

## 📄 Litsenziya

Ushbu loyiha ochiq manbali bo‘lib, **MIT** litsenziyasi asosida tarqatiladi.

---

Agar savollar bo‘lsa yoki loyiha haqida fikr bildirmoqchi bo‘lsangiz, GitHub Issues bo‘limida qoldiring. 😊

