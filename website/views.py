# import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

# import database
from . import db
# import from .models user
from .models import User, Post, Comment, Like, Faq
# import from .forms
from .forms import PostForm

# set views blueprint
views = Blueprint("views", __name__)

# default/home route


@views.route("/")
@views.route("/home")
# home route function
# returns home.html
def home():
    return render_template("home.html", user=current_user)

# Sing and Dance page route


@views.route("/singdanceoff")
def singdanceoff():
    # returns singdanceoff.html
    return render_template("singdanceoff.html", user=current_user)

# Meet the Leaders page route


@views.route("/leaders")
def leaders():
    # returns leaders.html
    return render_template("leaders.html", user=current_user)

# FAQ page route


@views.route("/faq", methods=['GET', 'POST'])
def faq():
    if request.method == 'POST':
        faq = request.form.get('faq')
        email = request.form.get('email')
        if len(email) < 1:
            # Flash error if email is less than 1 character
            flash('Email is invalid!', category='error')
        else:
            if len(faq) < 1:
                # Flash error if message is less than 1 character
                flash('Message is too short!', category='error')
            else:
                new_faq = Faq(data=faq, email=email)
                db.session.add(new_faq)
                db.session.commit()
                # Flash success if message is submitted
                flash('Message submitted!', category='success')

    return render_template("faq.html", user=current_user)


# blog page route
@views.route("/blog")
@login_required
# blog route function
# returns blog.html
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)


# create post route
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
# create post route function
# returns create_post.html
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')

        if not title:
            flash('Title cannot be empty', category='error')
        elif not content:
            flash('Content cannot be empty', category='error')
        else:
            post = Post(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))

    return render_template("create_post.html", user=current_user)

# delete blog post route


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post  does not exist', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
    return redirect(url_for('views.blog'))

# update blog post route


@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.author != current_user.id:
        flash('You do not have permission to edit this post.', category='error')
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', category='success')
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(
            Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("blog.html", user=current_user, posts=posts)
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("update_post.html", form=form, user=current_user, posts=post)


# view user posts route
@views.route("/posts/<username>")
@login_required
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.blog'))
    posts = Post.query.filter_by(user=user).order_by(
        Post.date_created.desc()).paginate(page=page, per_page=4)
    # posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

# blog comment route


@views.route("/create-comment/<post_id>", methods=["POST"])
# user must be logged in to post
@login_required
def create_comment(post_id):
    text = request.form.get("text")
    if not text:
        flash("Comment cannot be empty.", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added!", category="success")
        else:
            flash("Post does not exist.", category="error")

    return redirect(url_for("views.blog"))

# delete comment route


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('comment deleted!', category='success')
    return redirect(url_for('views.blog'))

# like comment route


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


@views.route("/calendar")
def calendar():
    # returns calendar.html
    return render_template("calendar.html", user=current_user)
