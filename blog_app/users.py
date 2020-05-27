try:
    from blog_app import app, db
    from flask import render_template, request, redirect, url_for
    from flask_login import current_user, login_required
    from blog_app.forms import BlogForm
    from blog_app.model import Blog, Likes
    from datetime import datetime
    import json
except ModuleNotFoundError:
    print('module not found')


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    page = request.args.get('page', type=int, default=1)

    blogs = Blog.query.order_by(Blog.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('user/home.html', blogs=blogs)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogForm()
    if request.method == 'GET':
        return render_template('user/blog.html', form=form)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        blog = Blog(title=title, content=content, author=current_user.id)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('user/blog.html', form=form)


@app.route('/post/<int:blog_id>', methods=['GET'])
def view_blog(blog_id):

    if request.method == 'GET':
        blog = Blog.query.get(int(blog_id))

        if current_user.is_authenticated:

            like = Likes.query.filter_by(user_id=current_user.id, blog_id=blog_id).first()

            return render_template('user/view_blog.html', blog=blog, like=like)

        return render_template('user/view_blog.html', blog=blog)


@app.route('/like-dislike', methods=['POST'])
def like():
    
    if request.method == 'POST':
        blog_id = request.form.get('blog_id')
        like = Likes.query.filter_by(blog_id=blog_id, user_id=current_user.id).first()

        if like:
            db.session.delete(like)
        else:
            like = Likes(like=1, blog_id=blog_id, user_id=current_user.id)

            db.session.add(like)

        db.session.commit()

        return json.dumps({"status": "success"})


