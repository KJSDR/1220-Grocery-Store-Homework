from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app.models import GroceryStore, ItemCategory, User
from grocery_app.extensions import bcrypt

# Function to get all stores for the QuerySelectField
def get_stores():
    return GroceryStore.query.all()

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Store Title', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Store Address', validators=[DataRequired(), Length(min=3, max=200)])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Item Name', validators=[DataRequired(), Length(min=3, max=80)])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[(cat.name, cat.value) for cat in ItemCategory])
    photo_url = StringField('Photo URL', validators=[URL()])
    store = QuerySelectField('Store', query_factory=get_stores, allow_blank=False, get_label='title')
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    """Form for user signup."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        """Check if username exists."""
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        """Check if password is correct."""
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')