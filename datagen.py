#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta

DATA_DIR = "data"  # In Docker, /data is used

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_format_md():
    path = os.path.join(DATA_DIR, "format.md")
    with open(path, "w") as f:
        f.write("# Heading\nSome content that requires formatting.")

def create_dates_txt():
    path = os.path.join(DATA_DIR, "dates.txt")
    with open(path, "w") as f:
        base = datetime.now()
        for i in range(10):
            day = base - timedelta(days=i)
            f.write(day.strftime("%Y-%m-%d") + "\n")

def create_contacts_json():
    path = os.path.join(DATA_DIR, "contacts.json")
    contacts = [
        {"first_name": "Alice", "last_name": "Zephyr"},
        {"first_name": "Bob", "last_name": "Yellow"},
        {"first_name": "Charlie", "last_name": "Xavier"}
    ]
    with open(path, "w") as f:
        json.dump(contacts, f)

def create_logs():
    logs_dir = os.path.join(DATA_DIR, "logs")
    ensure_dir(logs_dir)
    for i in range(12):
        log_path = os.path.join(logs_dir, f"log_{i}.log")
        with open(log_path, "w") as f:
            f.write(f"Log file {i} first line\nAdditional log details.")

def create_docs():
    docs_dir = os.path.join(DATA_DIR, "docs")
    ensure_dir(docs_dir)
    docs = {
        "README.md": "# Home\nDocumentation contents.",
        "large-language-models.md": "# Large Language Models\nDetailed info about LLMs."
    }
    for filename, content in docs.items():
        path = os.path.join(docs_dir, filename)
        with open(path, "w") as f:
            f.write(content)

def create_email_txt(sender_email):
    path = os.path.join(DATA_DIR, "email.txt")
    with open(path, "w") as f:
        f.write(f"From: {sender_email}\nSubject: Sample Email\nBody: Hello!")

def create_credit_card():
    path = os.path.join(DATA_DIR, "credit-card.png")
    # Simulate an image file with a dummy card number.
    with open(path, "w") as f:
        f.write("4111 1111 1111 1111")

def create_comments_txt():
    path = os.path.join(DATA_DIR, "comments.txt")
    comments = [
        "This is comment one",
        "This is comment two",
        "This is similar comment two",
        "Another different comment"
    ]
    with open(path, "w") as f:
        for comment in comments:
            f.write(comment + "\n")

def create_ticket_sales_db():
    db_path = os.path.join(DATA_DIR, "ticket-sales.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tickets (type TEXT, units INTEGER, price REAL)")
    tickets = [
        ("Gold", 2, 150.0),
        ("Gold", 3, 150.0),
        ("Silver", 5, 100.0)
    ]
    cursor.executemany("INSERT INTO tickets (type, units, price) VALUES (?, ?, ?)", tickets)
    conn.commit()
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: datagen.py <email>")
        sys.exit(1)
    sender_email = sys.argv[1]
    ensure_dir(DATA_DIR)
    create_format_md()
    create_dates_txt()
    create_contacts_json()
    create_logs()
    create_docs()
    create_email_txt(sender_email)
    create_credit_card()
    create_comments_txt()
    create_ticket_sales_db()
    print("Data generation complete.")

if __name__ == "__main__":
    main()
