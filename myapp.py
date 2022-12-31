import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    apps = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    apps.db = client.microblog

    @apps.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            apps.db.entries.insert({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in apps.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return apps
