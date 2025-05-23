from . import db
from flask_login import UserMixin
from sqlalchemy import (
    CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint,
    Integer, Text, Identity
)
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)  # Matches the schema
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)  # Plain-text password
    is_admin = db.Column(db.Boolean, default = False)
    def get_id(self):
        return str(self.user_id)

    reviews = db.relationship('Reviews', back_populates='user', cascade='all, delete-orphan')
    saved_recipes = db.relationship('SavedRecipeList', back_populates='user', cascade='all, delete-orphan')


class Reviews(db.Model):
    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint('score >= 1 AND score <= 5', name='reviews_score_check'),
        ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], name='reviews_recipe_id_fkey', ondelete='CASCADE'),
        PrimaryKeyConstraint('review_id', name='reviews_pkey')
    )

    review_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)

    user = db.relationship('Users', back_populates='reviews')
    recipe = db.relationship('Recipes', back_populates='reviews')


class Recipes(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable = False, default = 0)
    region_category = db.Column(db.String(50), nullable = False, default = 'Unknown')
    instructions = db.Column(db.Text, nullable = False)
    servings = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

    reviews = db.relationship('Reviews', back_populates='recipe', lazy=True)
    author = db.relationship('Users', backref='recipes')
    saved_by = db.relationship('SavedRecipeList', back_populates='recipe', cascade='all, delete-orphan')

    recipe_ingredients = db.relationship('RecipeIngredients', backref='recipe', lazy=True)
    image_path = db.Column(db.String(255))
    
    
class Ingredients(db.Model):
    __tablename__='ingredients'
    name = db.Column(db.Text, nullable = False)
    ingredient_id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Text, nullable = False)
    
    
class RecipeIngredients(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete = 'CASCADE'), nullable = False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id', ondelete = 'CASCADE'), nullable = False)
    amount = db.Column(db.Numeric, nullable = False)
    unit = db.Column(db.Text, nullable = False)
    ingredient = db.relationship('Ingredients', backref='recipe_ingredients')
    __table_args__=(
        PrimaryKeyConstraint('recipe_id', 'ingredient_id', name = 'recipe_ingredients_pkey'),
    )
    

class DietaryRestrictions(db.Model):
    __tablename__ = 'dietary_restrictions'
    dietary_restriction_id = db.Column(db.Integer, primary_key = True)
    dietary_preference = db.Column(db.String, nullable = False)
    name = db.Column(db.Text, nullable = False)
    __table_args__ = (CheckConstraint("dietary_preference IN ('allergy', 'preference')", name = 'dietary_preference_check'),)

    
class UserRestrictions(db.Model):
    __tablename__ = 'user_restrictions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete = 'CASCADE'), nullable = False)
    restriction_id = db.Column(db.Integer, db.ForeignKey('dietary_restrictions.dietary_restriction_id'), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'restriction_id', name = 'user_restrictions_pkey'), )


class AvgRecipeRating(db.Model):
    __tablename__ = 'recipe_score'
    __table_args__ = {'extend_existing': True}

    recipe_id = db.Column(db.Integer, primary_key=True)
    average_score = db.Column(db.Numeric(3, 2))

class SavedRecipeList(db.Model):
    __tablename__ = 'saved_recipe_lists'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete = 'CASCADE'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete = 'CASCADE'), primary_key=True)

    user = db.relationship('Users', back_populates='saved_recipes')
    recipe = db.relationship('Recipes', back_populates='saved_by')

