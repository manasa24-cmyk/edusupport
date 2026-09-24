import sqlite3
from datetime import datetime

DB_NAME = "edusupport.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE,
            student_name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'NEW',
            assigned_to TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_ticket(student_name, student_id, category,
                  priority, subject, description):

    conn = connect_db()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO tickets
        (student_name, student_id, category, priority,
         subject, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        student_id,
        category,
        priority,
        subject,
        description,
        "NEW",
        created_at,
        created_at
    ))

    ticket_number = cursor.lastrowid
    ticket_id = f"TKT{ticket_number:04d}"

    cursor.execute("""
        UPDATE tickets
        SET ticket_id = ?
        WHERE id = ?
    """, (ticket_id, ticket_number))

    conn.commit()
    conn.close()

    return ticket_id


def get_all_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticket_id, student_name, student_id,
               category, priority, subject,
               status, assigned_to, created_at
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    conn.close()

    return tickets


def update_ticket(ticket_id, assigned_to, status):
    conn = connect_db()
    cursor = conn.cursor()

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE tickets
        SET assigned_to = ?,
            status = ?,
            updated_at = ?
        WHERE ticket_id = ?
    """, (
        assigned_to,
        status,
        updated_at,
        ticket_id
    ))

    conn.commit()
    conn.close()