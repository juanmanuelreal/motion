from flask import render_template, request, redirect, g, Blueprint, url_for
from orm import Post


routes = Blueprint('posts', __name__, template_folder='templates', url_prefix="/posts")


# route to create post, get to vizualise form and post to process it
@routes.route('/create', methods=["GET", "POST"])
def create_post():
    try:
        if request.method == "GET":
            # username = session.get("username")
            if not g.user:
                return render_template("login.html", error="Have to login first!")
            return render_template("create_post.html")
        elif request.method == "POST":
            # username = session.get("username")
            if not g.user:
                return render_template("login.html", error="Have to login first!")
            
            
            author = g.user
            title = request.form["title"]
            text = request.form["text"]
            
            if author and title and text:

                orm_posts = Post("motion.db")
                orm_posts.create_post(author=author, title=title, text=text)
                return redirect('/')


            else:
                return render_template("create_post.html", error="All fields are required.")
    except Exception as e:
        return render_template("create_post.html", error="In this moment we can not process your enqury, try again later!")


# ruta para visualizar un post por id
@routes.route('/post/<id>')
def post_id(id):
    orm_posts = Post("motion.db")
    post = orm_posts.get_posts_by_id(id=id)

    if post:
        return render_template("home.html", post=post[0])
    return redirect('/')