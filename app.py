"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '123456'
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context(): db.create_all()

@app.route('/')
def home():
    """Redirects to users."""
    return redirect('/users')

@app.route('/users')
def users_list():
    users = Users.query.order_by(Users.last_name, Users.first_name).all()
    return render_template("user_list.html", users = users)

@app.route('/users/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        new_user = Users(first_name = first_name, last_name = last_name, image_url = image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<int:user_id>', methods = ['GET'])
def show_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('user_details.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('edit_user.html', user = user)
    else: 
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    
@app.route('/users/<int:user_id>/delete', methods=['POST', 'GET'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """User can make a new post"""
    user = Users.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Form Submission"""
    user = Users.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    # user=user,
                    tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('show_posts.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_posts.html', post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"'{post.title}' edited.")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"'{post.title}' deleted.")
    return redirect(f"/users/{post.user_id}")

@app.route('/tags')
def tags_index():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/new')
def tags_new_form():
    posts = Post.query.all()
    return render_template('new_tags.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def tags_new():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")
    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tags.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tags.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")

if __name__ == '__main__':
    app.run()