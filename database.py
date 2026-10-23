import sqlite3

def get_connection():
    connection = sqlite3.connect("patient_vitals.db")
    return connection

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            age INTEGER NOT NULL,
            systolic INTEGER NOT NULL,
            diastolic INTEGER NOT NULL,
            glucose_level REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def save_vitals(vitals):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO vitals (
            patient_id, age, systolic, diastolic, glucose_level
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        vitals.patient_id,
        vitals.age,
        vitals.blood_pressure.systolic,
        vitals.blood_pressure.diastolic,
        vitals.glucose_level
    ))

    connection.commit()
    connection.close()

def get_patient_vitals(patient_id):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM vitals WHERE patient_id = ? ORDER BY id DESC",
        (patient_id,)
    )

    records = cursor.fetchall()
    connection.close()

    return [dict(record) for record in records]

def get_patient_summary(patient_id):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            AVG(systolic) AS avg_systolic,
            AVG(diastolic) AS avg_diastolic,
            AVG(glucose_level) AS avg_glucose,
            COUNT(*) AS total_records
        FROM vitals
        WHERE patient_id = ?
    """, (patient_id,))

    summary = cursor.fetchone()
    connection.close()

    return dict(summary)