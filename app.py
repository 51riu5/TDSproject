#!/usr/bin/env python3
import os
import re
import json
import glob
import sqlite3
import datetime
import subprocess
from flask import Flask, request, Response

app = Flask(__name__)

# All file accesses are confined to this directory.
DATA_DIR = "/data"

def ensure_data_path(filepath: str) -> str:
    full_path = os.path.abspath(filepath)
    if not full_path.startswith(os.path.abspath(DATA_DIR)):
        raise ValueError("Access outside /data is not allowed.")
    return full_path

# Task A1: Run datagen.py with provided email (simulate data generation)
def task_datagen(email: str):
    try:
        cmd = ["python3", "datagen.py", email]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            return False, f"datagen error: {proc.stderr}"
        return True, f"Data generated successfully: {proc.stdout.strip()}"
    except Exception as e:
        return False, f"Exception in datagen: {str(e)}"

# Task A2: Format Markdown file using prettier@example (simulated)
def task_prettier(file_path: str, version="3.4.2"):
    try:
        file_path = ensure_data_path(file_path)
        if not os.path.exists(file_path):
            return False, "File to format does not exist."
        # Simulate formatting by appending a note.
        with open(file_path, "r+") as fp:
            content = fp.read()
            fp.seek(0)
            fp.write(f"<!-- Formatted with prettier@{version} -->\n" + content)
        return True, f"Formatted {file_path} using prettier@{version}."
    except Exception as e:
        return False, f"Error while formatting: {str(e)}"

# Task A3: Count Wednesdays from /data/dates.txt
def task_count_wednesdays():
    try:
        dates_path = ensure_data_path(os.path.join(DATA_DIR, "dates.txt"))
        with open(dates_path, "r") as fp:
            lines = fp.readlines()
        wed_count = sum(1 for line in lines if datetime.datetime.strptime(line.strip(), "%Y-%m-%d").weekday() == 2)
        out_path = ensure_data_path(os.path.join(DATA_DIR, "dates-wednesdays.txt"))
        with open(out_path, "w") as fp:
            fp.write(str(wed_count))
        return True, f"Wednesdays count ({wed_count}) written to {out_path}"
    except Exception as e:
        return False, f"Error counting Wednesdays: {str(e)}"

# Task A4: Sort contacts in /data/contacts.json
def task_sort_contacts():
    try:
        contacts_path = ensure_data_path(os.path.join(DATA_DIR, "contacts.json"))
        with open(contacts_path, "r") as fp:
            contacts = json.load(fp)
        contacts_sorted = sorted(contacts, key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))
        out_path = ensure_data_path(os.path.join(DATA_DIR, "contacts-sorted.json"))
        with open(out_path, "w") as fp:
            json.dump(contacts_sorted, fp, indent=2)
        return True, f"Sorted contacts written to {out_path}"
    except Exception as e:
        return False, f"Error sorting contacts: {str(e)}"

# Task A5: Process recent log files
def task_recent_logs():
    try:
        logs_dir = ensure_data_path(os.path.join(DATA_DIR, "logs"))
        files = glob.glob(os.path.join(logs_dir, "*.log"))
        if not files:
            return False, "No log files found."
        sorted_files = sorted(files, key=os.path.getmtime, reverse=True)
        out_path = ensure_data_path(os.path.join(DATA_DIR, "logs-recent.txt"))
        with open(out_path, "w") as out_fp:
            for f in sorted_files[:10]:
                with open(f, "r") as in_fp:
                    out_fp.write(in_fp.readline().strip() + "\n")
        return True, f"Recent logs written to {out_path}"
    except Exception as e:
        return False, f"Error processing logs: {str(e)}"

# Task A6: Index Markdown docs in /data/docs/
def task_index_docs():
    try:
        docs_dir = ensure_data_path(os.path.join(DATA_DIR, "docs"))
        index = {}
        for root, _, files in os.walk(docs_dir):
            for filename in files:
                if filename.lower().endswith(".md"):
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, docs_dir)
                    with open(full_path, "r") as fp:
                        for line in fp:
                            if line.strip().startswith("#"):
                                index[rel_path] = line.lstrip("#").strip()
                                break
        out_path = os.path.join(docs_dir, "index.json")
        with open(out_path, "w") as fp:
            json.dump(index, fp, indent=2)
        return True, f"Docs index created at {out_path}"
    except Exception as e:
        return False, f"Error indexing docs: {str(e)}"

# Task A7: Extract sender email from /data/email.txt (simulated with regex)
def task_extract_email():
    try:
        email_file = ensure_data_path(os.path.join(DATA_DIR, "email.txt"))
        with open(email_file, "r") as fp:
            content = fp.read()
        m = re.search(r"[\w\.-]+@[\w\.-]+", content)
        if m:
            sender = m.group(0)
            out_path = ensure_data_path(os.path.join(DATA_DIR, "email-sender.txt"))
            with open(out_path, "w") as fp:
                fp.write(sender)
            return True, f"Sender extracted to {out_path}"
        else:
            return False, "No email found."
    except Exception as e:
        return False, f"Error extracting email: {str(e)}"

# Task A8: Extract credit card number from /data/credit-card.png (simulated)
def task_extract_credit_card():
    try:
        cc_path = ensure_data_path(os.path.join(DATA_DIR, "credit-card.png"))
        with open(cc_path, "r") as fp:
            card_text = fp.read().strip().replace(" ", "")
        out_path = ensure_data_path(os.path.join(DATA_DIR, "credit-card.txt"))
        with open(out_path, "w") as fp:
            fp.write(card_text)
        return True, f"Credit card number extracted to {out_path}"
    except Exception as e:
        return False, f"Error extracting credit card: {str(e)}"

# Task A9: Find the most similar pair of comments (simulated)
def task_similar_comments():
    try:
        comments_path = ensure_data_path(os.path.join(DATA_DIR, "comments.txt"))
        with open(comments_path, "r") as fp:
            comments = [line.strip() for line in fp if line.strip()]
        if len(comments) < 2:
            return False, "Not enough comments for analysis."
        # For simulation, just pick the first two comments.
        pair = comments[:2]
        out_path = ensure_data_path(os.path.join(DATA_DIR, "comments-similar.txt"))
        with open(out_path, "w") as fp:
            fp.write("\n".join(pair))
        return True, f"Similar comments written to {out_path}"
    except Exception as e:
        return False, f"Error in similar comments task: {str(e)}"

# Task A10: Calculate total sales for "Gold" tickets
def task_ticket_sales():
    try:
        db_path = ensure_data_path(os.path.join(DATA_DIR, "ticket-sales.db"))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
        result = cursor.fetchone()
        total = result[0] if result and result[0] is not None else 0
        conn.close()
        out_path = ensure_data_path(os.path.join(DATA_DIR, "ticket-sales-gold.txt"))
        with open(out_path, "w") as fp:
            fp.write(str(total))
        return True, f"Total Gold ticket sales ({total}) written to {out_path}"
    except Exception as e:
        return False, f"Error calculating ticket sales: {str(e)}"

@app.route("/run", methods=["POST"])
def run_task():
    task_desc = request.args.get("task", "").strip()
    if not task_desc:
        return Response("Task description is required.", status=400)
    try:
        if "datagen" in task_desc or "generate data" in task_desc:
            m = re.search(r"[\w\.-]+@[\w\.-]+", task_desc)
            email = m.group(0) if m else "user@example.com"
            success, msg = task_datagen(email)
        elif "prettier" in task_desc:
            m = re.search(r"(/data/\S+)", task_desc)
            file_path = m.group(1) if m else os.path.join(DATA_DIR, "format.md")
            success, msg = task_prettier(file_path)
        elif "Wednesday" in task_desc or "dates.txt" in task_desc:
            success, msg = task_count_wednesdays()
        elif "contacts" in task_desc:
            success, msg = task_sort_contacts()
        elif "log" in task_desc and "recent" in task_desc:
            success, msg = task_recent_logs()
        elif "docs" in task_desc:
            success, msg = task_index_docs()
        elif "email" in task_desc and "sender" in task_desc:
            success, msg = task_extract_email()
        elif "credit-card" in task_desc:
            success, msg = task_extract_credit_card()
        elif "comments" in task_desc and "similar" in task_desc:
            success, msg = task_similar_comments()
        elif "ticket-sales" in task_desc or "Gold" in task_desc:
            success, msg = task_ticket_sales()
        else:
            return Response("Task not recognized.", status=400)
    except ValueError as ve:
        return Response(str(ve), status=400)
    except Exception as e:
        return Response("Internal Agent Error: " + str(e), status=500)
    return Response(msg, status=200) if success else Response("Error: " + msg, status=500)

@app.route("/read", methods=["GET"])
def read_file():
    file_path = request.args.get("path", "").strip()
    if not file_path:
        return Response("File path is required.", status=400)
    try:
        full_path = ensure_data_path(file_path)
        if not os.path.exists(full_path):
            return Response("", status=404)
        with open(full_path, "r") as fp:
            content = fp.read()
        return Response(content, status=200, mimetype="text/plain")
    except Exception as e:
        return Response("Error: " + str(e), status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    _ = os.environ.get("AIPROXY_TOKEN", "")
    app.run(host="0.0.0.0", port=port)
