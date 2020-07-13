# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)

@app.route("/")
def index():
    result = mongo.db.users.find_one()
    return render_template("index.html", mission_to_mars=result)

@app.route("/scrape")
def scrapper():
    try:
        d = mongo.db.users.find_one()
        mongo.db.users.update({'_id': d['_id']}, scrape_mars.scrape())
    except:
        mongo.db.users.insert(scrape_mars.scrape())
    return redirect("/")

if __name__ == "__main__":
   app.run()