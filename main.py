from flask import Flask, render_template, request, url_for


#create a secret key for security
import os

#store functions here
import utils as util

#needed to read json files
import json

# loads default recipe data
from default_data import create_default_data

#Recipe data
from models import db
from models.category import Category
from models.recipe import Recipe

#Flask Admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)

#secret key for form security
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db.init_app(app)

# Custom Jinja filter function
def thumbs_filter(rating):
    if rating >= 4:
        return '<i class="fa fa-thumbs-up"></i>'
    elif rating <= 2:
        return '<i class="fa fa-thumbs-down"></i>'
    else:
        return ''

# Register the filter with Jinja environment
app.jinja_env.filters['thumbs'] = thumbs_filter



@app.route("/recipes")
def recipes():
    all_recipes = Recipe.query.all()
    title = "Recipes"
    context = {
      "title": title,
      "recipes": all_recipes
    }
    return render_template("recipes.html", **context)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    this_recipe = Recipe.query.get(recipe_id)
    title = "Recipe"
    context = {
      "title": "Recipe",
      "recipe": this_recipe
    }
    if this_recipe:
        return render_template('recipe.html', **context)
    else:
        return render_template("404.html",title="404"), 404





@app.route('/user/<int:user_number>')
def user(user_number):
    return f'Content for User {user_number}'




#user list
@app.route('/users')
def users():

  # Read project data from JSON file
  with open('test.json') as json_file:
      user_data = json.load(json_file)
      #print(user_data)

  context = {
    "title": "Users",
    "users": user_data
  }

  return render_template("users.html",**context)




# Route for the form page
@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Register"
    feedback = None
    if request.method == 'POST':
        feedback = util.register_data(request.form)

    context = {
        "title": title,
        "feedback": feedback
    }
    return render_template('register.html', **context)

@app.route('/')
def index():
    title = "Home"
    return render_template("index.html",title=title)

@app.route('/about')
def about():
    title = "About"
    return render_template("about.html",title=title)

@app.route('/movies')
def movies():
  
  movie_dict = util.movie_stars(util.movie_dict)

  context = {
    "title": "Movies",
    "movies": movie_dict
  }  
  return render_template("movies.html",**context)

#Flask Admin
class RecipeView(ModelView):
  column_searchable_list = ['name', 'author']


admin = Admin(app)
admin.url = '/admin/' #would not work on repl w/o this!
admin.add_view(RecipeView(Recipe, db.session))
admin.add_view(ModelView(Category, db.session))


with app.app_context():
  db.create_all()

  #removes all data and loads defaults:
  create_default_data(db,Recipe,Category)



app.run(host='0.0.0.0', port=81)
