import sqlite3
import os
from datetime import datetime, timedelta
import random

DATABASE = 'civicfix.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id   TEXT UNIQUE NOT NULL,
            category    TEXT NOT NULL,
            description TEXT NOT NULL,
            location    TEXT NOT NULL,
            latitude    REAL,
            longitude   REAL,
            photo       TEXT,
            name        TEXT,
            email       TEXT,
            status      TEXT DEFAULT 'Submitted',
            created_at  TEXT NOT NULL
        )
    ''')
    db.commit()

    # Insert sample data only if the table is empty
    count = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    if count == 0:
        _seed_sample_data(db)

    db.close()


def _seed_sample_data(db):
    samples = [
        ('CF-A1B2C3D4', 'Pothole',          'Large pothole on main road causing accidents',
         'MG Road, Ahmedabad',         23.0225, 72.5714, 'Resolved'),
        ('CF-E5F6G7H8', 'Broken Streetlight','3 streetlights not working near park gate',
         'Satellite Area, Ahmedabad',  23.0300, 72.5500, 'In Progress'),
        ('CF-I9J0K1L2', 'Garbage Overflow',  'Garbage bin overflowing for 5 days',
         'Navrangpura, Ahmedabad',     23.0390, 72.5600, 'Under Review'),
        ('CF-M3N4O5P6', 'Drainage Problem',  'Blocked drain causing waterlogging',
         'Paldi, Ahmedabad',           23.0100, 72.5800, 'Submitted'),
        ('CF-Q7R8S9T0', 'Road Damage',       'Broken road surface after heavy rain',
         'Bopal, Ahmedabad',           23.0450, 72.4700, 'In Progress'),
        ('CF-U1V2W3X4', 'Water Leakage',     'Water pipe burst near society gate',
         'Thaltej, Ahmedabad',         23.0550, 72.4900, 'Submitted'),
        ('CF-Y5Z6A7B8', 'Pothole',           'Deep pothole near school entrance',
         'Maninagar, Ahmedabad',       22.9900, 72.6100, 'Resolved'),
        ('CF-C9D0E1F2', 'Broken Streetlight','Entire street dark at night',
         'Gota, Ahmedabad',            23.1000, 72.5300, 'Submitted'),
    ]

    base = datetime.now()
    for i, (rid, cat, desc, loc, lat, lng, status) in enumerate(samples):
        created = (base - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            '''INSERT INTO reports
               (report_id, category, description, location, latitude, longitude,
                photo, name, email, status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (rid, cat, desc, loc, lat, lng, None,
             f'User{i+1}', f'user{i+1}@example.com', status, created)
        )
    db.commit()


if __name__ == '__main__':
    init_db()
    print('Database initialized.')
