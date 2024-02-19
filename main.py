from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    {"username": "juanmanuelreal", "password":"654321"}
    
]

# post = []

# ruta home para visualizar todos los posts y poder buscar por titulo
@app.route('/') # decorator for home route
def home(): # home function
    search = request.args.get('search')
    if search:
        list_post = []
        for post in posts:
            if search.lower() in post['title'].lower():
                list_post.append(post)
        return render_template("home.html", post=list_post)
    else: 
        return render_template("home.html", post=posts) # render home.html with posts

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

#ruta profile, proximamente solo para usuarios con Login
@app.route('/profile')
def profile():
    return render_template("profile.html")

#ruta para crear post, get para visualizar form y post para procesarlo
@app.route('/post', methods=['GET', 'POST'])
def post():
    pass

# ruta para visualizar un post por id
@app.route('/post/<int:id>')
def post_id(id):
    for post in posts:
        if post["id"] == id:
            return render_template("post.html", post=post)
    return 'ok'

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