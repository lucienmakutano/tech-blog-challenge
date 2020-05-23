from blog_app import app
from flask import render_template
from flask_login import current_user


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('user/home.html')
