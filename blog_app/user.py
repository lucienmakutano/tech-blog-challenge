try:
    from blog_app import app, db, login_manager
    from flask_login import login_required, current_user
    from blog_app.model import Blog
    from flask import render_template, request, redirect, url_for, flash
    from blog_app.forms import UpdateBlogForm
except ModuleNotFoundError:
    print('module not found')


@app.route('/dashboard/<int:user_id>')
@login_required
def dashboard(user_id):
    page = request.args.get('page')

    blogs = Blog.query.filter_by(author=user_id).paginate(page=page, per_page=5)

    return render_template('user/dashboard.html', blogs=blogs)


@app.route('/dashboard/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit(blog_id):
    blog = Blog.query.get(int(blog_id))
    form = UpdateBlogForm()

    if request.method == 'GET':
        if blog:
            form.title.data = blog.title
            form.content.data = blog.content

            return render_template('user/edit.html', form=form, blog_id=blog_id)

    if form.validate_on_submit():

        blog.title = form.title.data
        blog.content = form.content.data

        db.session.commit()

        flash('your update was successful', 'success')

        return redirect(url_for('edit', blog_id=blog_id))

    return render_template('user/edit.html', form=form, blog_id=blog_id)


@app.route('/dashboard/delete/<int:blog_id>', methods=['GET'])
@login_required
def delete(blog_id):

    blog = Blog.query.get(int(blog_id))

    if blog:
        db.session.delete(blog)

        db.session.commit()

        return redirect(url_for('dashboard', user_id=current_user.id))

    return redirect(url_for('dashboard', user_id=current_user.id))
