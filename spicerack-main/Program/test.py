from flask import Flask, render_template, request
import requests

api_key = '9055e1d64e41436d9944aadde529cc59'
base_url = 'https://api.spoonacular.com/recipes/'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Get user input for ingredients from the HTML form
    user_ingredients = request.form.get('ingredients').split(',')

    # Make a request to the Spoonacular API to generate recipes
    generated_recipes = generate_recipes(api_key, user_ingredients)

    if generated_recipes:
        # Get detailed recipe information for each recipe
        recipe_details = []
        for recipe in generated_recipes:
            details = get_recipe_details(api_key, recipe['id'])
            if details:
                recipe_details.append(details)

        if recipe_details:
            # Pass recipe details to the HTML template
            return render_template('recipe.html', recipes=recipe_details)

    # Handle the case where no recipe details are available
    return render_template('error.html')

def generate_recipes(api_key, ingredients, number=3):
    # Prepare parameters for the API request
    params = {'apiKey': api_key, 'ingredients': ','.join(ingredients), 'number': number}
    
    # Make a request to the Spoonacular API
    response = requests.get(base_url + 'findByIngredients', params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        recipes_data = response.json()
        
        # Extract relevant information (customize as needed)
        recipes = recipes_data
        return recipes
    else:
        print(f"Error: {response.status_code}")
        return None
    
def get_recipe_details(api_key, recipe_id):
    # Prepare parameters for the API request
    url = f'{base_url}{recipe_id}/information'
    params = {'apiKey': api_key}
    
    # Make a request to the Spoonacular API
    response = requests.get(url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        recipe_data = response.json()
        
        # Extract relevant information (customize as needed)
        recipe_details = recipe_data
        return recipe_details
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
