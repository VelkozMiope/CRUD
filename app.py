from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Book
app = Flask(__name__)

if not os.path.isfile('books.db'):
    db.connect()

@app.route('/')
def index():
    return render_template('index.html')
def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()