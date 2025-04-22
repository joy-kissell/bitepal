from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    score = SelectField('Score (1–5)',
                        choices=[(str(i), i) for i in range(1, 6)],
                        validators=[DataRequired()])
    review_text = TextAreaField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
    
# class LogoutForm(FlaskForm):
#     submit = SubmitField('Logout')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    calories = IntegerField('Calories', validators=[Optional(), NumberRange(min=0)], default=0)
    region_category = StringField('Region of Origin', validators = [Optional()], default = 'Unknown')
    instructions = TextAreaField('Instructions', validators = [DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Recipe')
    
class IngredientsForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    ingredient_type = SelectField('Ingredient Type', choices = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('grain', 'Grain'),
        ('protein', 'Protein'),
        ('dairy', 'Dairy'),
        ('spice', 'Spice'),
        ('herb', 'Herb'),
        ('oil', 'Oil'),
        ('sauce', 'Sauce'),
        ('condiment', 'Condiment'),
        ('sugar', 'Sugar'),
        ('sweetener', 'Sweetener'),
        ('nut', 'Nut'),
        ('seed', 'Seed'),
        ('legume', 'Legume'),
        ('seafood', 'Seafood'),
        ('meat', 'Meat'),
        ('poultry', 'Poultry'),
        ('egg', 'Egg'),
        ('dried fruit', 'Dried Fruit'),
        ('cereal', 'Cereal'),
        ('snack', 'Snack')
    ])