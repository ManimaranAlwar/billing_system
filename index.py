import os
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///alwar_stores.db")
engine = create_engine(DATABASE_URL)
Base = automap_base()

@app.before_request
def prepare_db():
    # This reflects the tables from the DB on the first request
    if not Base.classes:
        Base.prepare(autoload_with=engine)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "store": "Alwar Stores",
        "tables_detected": list(Base.classes.keys())
    })

if __name__ == "__main__":
    app.run()