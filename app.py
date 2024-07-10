# app.py

from flask import Flask, render_template
from __init__ import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
