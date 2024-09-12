<<<<<<< HEAD
# app.py

from flask import Flask, render_template
from __init__ import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
=======
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
>>>>>>> 43afbf85f11838e078d4aa3734a285593be438b3
