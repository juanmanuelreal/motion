from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {"author":"Motion", "text": "start writing here"},
    {"author":"Juan Manuel", "text": "start writing heres"}
]

@app.route('/')
def home():
    return render_template("home.html", name="Motion 2024", posts=posts)

@app.route('/contact')
def contact():
    return render_template("contact.html", name="Motion 2024", posts=posts)

@app.route('/login')
def login():
    return render_template("login.html", name="Motion 2024", posts=posts)

app.run(debug=True)