movie_dict = [
  {"title": "Dune", "genre": "Sci-Fi", "rating": 3},
  {"title": "Alien", "genre": "Sci-Fi", "rating": 4},
  {"title": "Batman", "genre": "Comics", "rating": 5}
 ]


def movie_stars(movie_dict):
  for movie in movie_dict:
    movie["stars"] = add_stars(movie["rating"])
  return movie_dict

def add_stars(rating):
  my_return = ""
  
  for x in range(5):
    checked = "checked" if rating > x else ""
    my_return += f"<span class=\"fa fa-star {checked}\"></span>"
  return my_return



def register_data(form_data):
  feedback = []
  for key, value in form_data.items():
    # checkboxes have [] for special handling
    if key.endswith('[]'):
      # Use getlist to get all values for the checkbox
      checkbox = request.form.getlist(key)
      key = key.replace('_', ' ').replace('[]', '')
      feedback.append(f"{key}: {', '.join(map(str, checkbox))}")
    else:
      # Handle other form elements
      key = key.replace('_', ' ')
      feedback.append(f"{key}: {value}")
  return feedback