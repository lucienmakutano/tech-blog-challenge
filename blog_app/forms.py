try:
    from flask_wtf import FlaskForm
    from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
    from wtforms import StringField, PasswordField, SubmitField, TextAreaField
    from blog_app.model import Users
    import email_validator
except ModuleNotFoundError:
    print('unable to load the modules')


class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Register(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', 'passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("This email is already taken")


class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('create')


class UpdateBlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('save')
