import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('motion.db')
    cursor = conn.cursor()
    return conn, cursor

# False data base of posts
posts = [
    {"id": 1, "author": "Motion", "title": "1", "text": "start writing here"},
    {"id": 2, "author": "Motion", "title": "2", "text": "start writing here"},
    {"id": 3, "author": "Motion", "title": "3", "text": "start writing here"},
    {"id": 4, "author": "Motion", "title": "4", "text": "start writing here"},
    {"id": 5, "author": "Motion", "title": "5", "text": "start writing here"},
    {"id": 6, "author": "Motion", "title": "6", "text": "start writing here"}
]

# False data base of users
users = [
    {"username": "juanmreal1", "password":"123456"},
    {"username": "juanmanuelreal", "password":"654321"},
    
]

# post = []

# ruta home para visualizar todos los posts y poder buscar por titulo
@app.route('/') # decorator for home route
def home(): # home function
    # funciona con la db en variable
    # search = request.args.get('search')
    # if search:
    #     list_post = []
    #     for post in posts:
    #         if search.lower() in post['title'].lower():
    #             list_post.append(post)
    #     return render_template("home.html", post=list_post)
    # else: 
    #     return render_template("home.html", post=posts) # render home.html with posts
    
    #funciona con db sqlite:
    conn, cursor = get_db_connection()
    
    search = request.args.get('search')
    if search:
        cursor.execute("SELECT * FROM posts WHERE posts.title LIKE ?", (f"%{search}%",))
        posts = cursor.fetchall()
        conn.close()
        return render_template("home.html", post=posts )
    
    
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template("home.html", post=posts)

#ruta estatica pag contact
@app.route('/contact')
def contact():
    return render_template("contact.html")

# ruta para login, ger para obtener form y post para porcesar los datos de usuario
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif  request.method == "POST":
         for user in users:
             if user['username'] == request.form['username'] and user['password'] == request.form['password']:
                 return redirect('/profile')
         else:
            return render_template("login.html", error="Invalid Username or Password")
        
# ruta para registro,  get para mostrar el form y post para procesar los datos del nuevo usuario y guardarlos
# solo en memoria
# @app.route("/register",methods=["GET","POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#     elif request.method == "POST":
#             user_exist = list(filter(lambda user: user["username"] == request.form["username"], users))
#             if user_exist:
#                 return render_template( "register.html", error="Username already exists!")
#             new_id = users[-1]["id"] + 1
#             new_user = {"id": new_id, "username": request.form["username"], "password": request.form["password"]}
#             users.append(new_user)
#             return "ok"

# ruta para registro,  get para mostrar el form y post para procesar los datos del nuevo usuario y guardarlos
# en db
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return render_template( "register.html", error="Username and  Password are required.")
        # Verificamos que no exista un usuario con este nombre
        
        if len(password) < 5:
            return render_template( "register.html", error="Password must be at least 5 characters long.")
        
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE users.username == ?", (username,))
        user_exists = cursor.fetchone()
        if user_exists:
            return render_template( "register.html", error="Username already exists!") 
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()
        return "ok"

#ruta profile, proximamente solo para usuarios con Loginpy
@app.route('/profile')
def profile():
    return render_template("profile.html")

#ruta para crear post, get para visualizar form y post para procesarlo
@app.route('/post', methods=['GET', 'POST'])
def create_post():
    if request.method == "GET":
        return render_template("create_post.html")
    elif request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        text = request.form["text"]
        conn, cursor = get_db_connection()
        cursor.execute("INSERT INTO posts (author, title, text) VALUES (?,?,?)", (title, author, text))
        conn.commit()
        conn.close()
        return redirect('/')

# ruta para visualizar un post por id
@app.route('/post/<id>')
def post_id(id):
    # for post in posts:
    #     if post["id"] == id:
    #         return render_template("post.html", post=post)
    # return 'ok'
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM posts WHERE posts.id == ?", id)
    post = cursor.fetchone()
    return render_template("post.html", post=post)

# ruta para probar el cast de tipo path 
@app.route('/otros/<path:url>')
def path_url(url):
    print(url)
    list_post = []
    return render_template("home.html, posts=list_post")

# ruta para probar parametros dinamicos por url y ademas hacer el cast directo en url
@app.route('/otros/calculator/<int:numa>/<int:numb>')
def calculator(numa, numb):
    suma = numa+numb
    return render_template("calcu.html", resultado=suma)

# # ruta ejemplo de redirect y url_for
# # @app.route('/algo/<algo>')
# # def algo(algo):
# #     if algo.isnumeric():
#           # return redirect(url_for('search_post, id=algo))
#           return redirect(f'/post/{algo}')
#       else: 
#           return render_template("home.html, posts=posts")

app.run(debug=True)