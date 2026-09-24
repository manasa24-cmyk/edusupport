import sqlite3
from datetime import datetime, timedelta

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
            updated_at TEXT,
            pending_reason TEXT,
            resolution_note TEXT,
            due_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            action TEXT,
            details TEXT,
            created_at TEXT
        )
    """)

    # Add columns if an older database already exists
    columns = [
        row[1]
        for row in cursor.execute(
            "PRAGMA table_info(tickets)"
        ).fetchall()
    ]

    new_columns = {
        "pending_reason": "TEXT",
        "resolution_note": "TEXT",
        "due_at": "TEXT"
    }

    for column, data_type in new_columns.items():
        if column not in columns:
            cursor.execute(
                f"ALTER TABLE tickets ADD COLUMN {column} {data_type}"
            )

    conn.commit()
    conn.close()


def create_ticket(
    student_name,
    student_id,
    category,
    priority,
    subject,
    description
):
    conn = connect_db()
    cursor = conn.cursor()

    created_at = datetime.now()

    sla_hours = {
        "Low": 72,
        "Medium": 48,
        "High": 24,
        "Urgent": 8
    }

    due_at = created_at + timedelta(
        hours=sla_hours.get(priority, 48)
    )

    created_text = created_at.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    due_text = due_at.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO tickets (
            student_name,
            student_id,
            category,
            priority,
            subject,
            description,
            status,
            created_at,
            updated_at,
            due_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        student_id,
        category,
        priority,
        subject,
        description,
        "NEW",
        created_text,
        created_text,
        due_text
    ))

    ticket_number = cursor.lastrowid
    ticket_id = f"TKT{ticket_number:04d}"

    cursor.execute("""
        UPDATE tickets
        SET ticket_id = ?
        WHERE id = ?
    """, (
        ticket_id,
        ticket_number
    ))

    cursor.execute("""
        INSERT INTO ticket_history (
            ticket_id,
            action,
            details,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        ticket_id,
        "Ticket Created",
        f"Ticket created with {priority} priority",
        created_text
    ))

    conn.commit()
    conn.close()

    return ticket_id


def get_all_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ticket_id,
            student_name,
            student_id,
            category,
            priority,
            subject,
            description,
            status,
            assigned_to,
            created_at,
            updated_at,
            pending_reason,
            resolution_note,
            due_at
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    conn.close()

    return tickets


def update_ticket(
    ticket_id,
    assigned_to,
    status,
    pending_reason="",
    resolution_note=""
):
    conn = connect_db()
    cursor = conn.cursor()

    updated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        UPDATE tickets
        SET assigned_to = ?,
            status = ?,
            updated_at = ?,
            pending_reason = ?,
            resolution_note = ?
        WHERE ticket_id = ?
    """, (
        assigned_to,
        status,
        updated_at,
        pending_reason,
        resolution_note,
        ticket_id
    ))

    cursor.execute("""
        INSERT INTO ticket_history (
            ticket_id,
            action,
            details,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        ticket_id,
        "Ticket Updated",
        f"Assigned to: {assigned_to}; Status: {status}",
        updated_at
    ))

    conn.commit()
    conn.close()


def get_ticket_history(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT action, details, created_at
        FROM ticket_history
        WHERE ticket_id = ?
        ORDER BY id DESC
    """, (ticket_id,))

    history = cursor.fetchall()

    conn.close()

    return history
