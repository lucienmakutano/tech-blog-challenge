try:
    from blog_app import app, db
    from flask import render_template, request, redirect, url_for
    from flask_login import current_user, login_required
    from blog_app.forms import BlogForm
    from blog_app.model import Blog
    from datetime import datetime
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
