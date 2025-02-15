import subprocess
import os
import json
import sqlite3
import requests
import datetime
import markdown
import openai
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
import torch
import torchaudio
from transformers import pipeline
import cv2
import numpy as np
import hashlib

openai.api_key = os.getenv("AIPROXY_TOKEN")

def execute_task(task_description):
    """Parses a natural language task description and executes the corresponding function"""
    if "install uv" in task_description or "datagen.py" in task_description:
        return task_a1(task_description)
    elif "format.md" in task_description and "prettier" in task_description:
        return task_a2()
    elif "dates.txt" in task_description and "Wednesdays" in task_description:
        return task_a3()
    elif "contacts.json" in task_description and "sort" in task_description:
        return task_a4()
    elif "logs" in task_description and "recent" in task_description:
        return task_a5()
    elif "docs" in task_description and "index.json" in task_description:
        return task_a6()
    elif "email.txt" in task_description and "sender" in task_description:
        return task_a7()
    elif "credit-card.png" in task_description:
        return task_a8()
    elif "comments.txt" in task_description:
        return task_a9()
    elif "ticket-sales.db" in task_description and "Gold" in task_description:
        return task_a10()
    elif "fetch API data" in task_description:
        return task_b3()
    elif "clone a git repo" in task_description:
        return task_b4()
    elif "run a SQL query" in task_description:
        return task_b5()
    elif "scrape a website" in task_description:
        return task_b6()
    elif "compress an image" in task_description:
        return task_b7()
    elif "transcribe an audio file" in task_description:
        return task_b8()
    elif "convert Markdown to HTML" in task_description:
        return task_b9()
    elif "filter a CSV file" in task_description:
        return task_b10()
    else:
        raise Exception("Unknown task description.")

# **Task Implementations**

def task_a1(task_description):
    """Install uv and run datagen.py with user email"""
    user_email = task_description.split(" ")[-1]
    subprocess.run(["python", "datagen.py", user_email])
    return f"Data generated for {user_email}."

def task_a2():
    """Format /data/format.md using Prettier"""
    subprocess.run(["prettier", "--write", "/data/format.md"])
    return "File formatted."

def task_a3():
    """Count the number of Wednesdays in /data/dates.txt"""
    with open("/data/dates.txt") as f:
        dates = f.readlines()
    count = sum(1 for date in dates if datetime.datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)
    with open("/data/dates-wednesdays.txt", "w") as f:
        f.write(str(count))
    return "Wednesdays counted."

def task_a4():
    """Sort contacts.json by last_name, then first_name"""
    with open("/data/contacts.json") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))
    with open("/data/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=4)
    return "Contacts sorted."

def task_a5():
    """Get first line of 10 most recent .log files"""
    logs = sorted(os.listdir("/data/logs"), key=lambda f: os.path.getmtime(f), reverse=True)[:10]
    with open("/data/logs-recent.txt", "w") as f:
        for log in logs:
            with open(f"/data/logs/{log}") as lf:
                f.write(lf.readline())
    return "Recent logs saved."

def task_a6():
    """Extract H1 titles from Markdown files"""
    index = {}
    for file in os.listdir("/data/docs"):
        if file.endswith(".md"):
            with open(f"/data/docs/{file}") as f:
                for line in f:
                    if line.startswith("# "):
                        index[file] = line[2:].strip()
                        break
    with open("/data/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "Index created."

def task_a7():
    """Extract email sender from email.txt"""
    with open("/data/email.txt") as f:
        email_content = f.read()
    response = openai.Completion.create(
        engine="davinci", prompt=f"Extract sender email: {email_content}", max_tokens=20
    )
    sender = response.choices[0].text.strip()
    with open("/data/email-sender.txt", "w") as f:
        f.write(sender)
    return "Sender extracted."

def task_a8():
    """Extract credit card number from image"""
    img = cv2.imread("/data/credit-card.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(bin_img).replace(" ", "")
    with open("/data/credit-card.txt", "w") as f:
        f.write(text)
    return "Credit card extracted."

def task_b3():
    """Fetch API data"""
    response = requests.get("https://api.example.com/data")
    with open("/data/api-data.json", "w") as f:
        json.dump(response.json(), f, indent=4)
    return "API data saved."

def task_b5():
    """Run a SQL query on SQLite"""
    conn = sqlite3.connect("/data/database.db")
    df = pd.read_sql_query("SELECT * FROM users;", conn)
    df.to_csv("/data/query-result.csv", index=False)
    return "SQL query executed."

def task_b9():
    """Convert Markdown to HTML"""
    with open("/data/docs/sample.md") as f:
        html = markdown.markdown(f.read())
    with open("/data/docs/sample.html", "w") as f:
        f.write(html)
    return "Markdown converted."

