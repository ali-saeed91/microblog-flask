import os
import sys
import datetime
from tkinter import *
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# def create_app():
app = Flask(__name__)
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.microblog
entries=[]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        # app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        entries.append({"content": entry_content, "date": formatted_date})
        
    entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            # for entry in app.db.entries.find({})
            for entry in entries
        ]
    if len(entries) > 5:
        entries=[]
         # Initialising Popup prompt for Error
        root = Tk()
        root.geometry("300x200")
        
        w = Label(root, text ='MAX Limit Reached', font = "90",fg="Navyblue") 
        w.pack()
            
        msg = Message( root, text = "Refreshing Database")  
            
        msg.pack()  
        
        root.mainloop() 
        sys.exit()
    return render_template("home.html", entries=entries_with_date)
    
    # return app
