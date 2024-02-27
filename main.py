# import time
# import request
from flask import Flask, render_template, request, redirect, session, g, abort, Request, Blueprint

from orm import User, Post
from valid_register import valid_form
from routes_posts import routes


app = Flask(__name__)
app.secret_key = "motion_key"

app.register_blueprint(routes)

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session["username"]

@app.after_request
def after_request(response):
    return response


# route to vizualice all posts and to search by title
@app.route('/') # decorator for home route
def home():
    orm_posts = Post("motion.db")

    title_search = request.args.get('search')
    if title_search:
        posts = orm_posts.get_posts_by_title(title=title_search)
        return render_template("home.html", posts=posts)
        
    posts = orm_posts.get_all_posts()
    return render_template("home.html", posts=posts)
    


#static route for contact page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# ruta para login, get para obtener form y post para porcesar los datos de usuario
@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == "GET":
        return render_template("login.html")
    
    if  request.method == "POST":
        username =  request.form["username"]
        password = request.form["password"]


        orm_user = User("motion.db")
        user_exist = orm_user.get_user_by_username(username=username)
        if  user_exist and user_exist[0]['password'] == password:
            session['username'] = username
            return redirect('/profile')

        return render_template("login.html", error="Invalid Username or Password")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        orm_user = User("motion.db")

        result, message = valid_form(orm_user=orm_user, username=username, password=password)
        if  not result:
            return render_template("register.html", error="Username  already exists.")
        
        #with orm
        orm_user.create_user(username=username, password=password)
        
        return redirect('/login')

# ruta perfil, proximamente solo para usuarios con login
@app.route('/logout')
def logout():
    if not g.user:
        return render_template("login.html", error="Need to Login!")
    session.pop("username", None)
    return redirect('/')

#ruta profile, proximamente solo para usuarios con Login
@app.route('/profile')
def perfil():
    if not g.user:
        return redirect('/login')
    return render_template("profile.html", username=g.user)

app.run(debug=True)