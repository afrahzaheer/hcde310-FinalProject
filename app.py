from flask import Flask, render_template, request, redirect, url_for
import requests
import urllib.parse
import urllib.request
import json
import random

app = Flask(__name__)

API_BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

MEAL_CATEGORIES = {
    "breakfast": "Breakfast",
    "starter": "Starter",
    "vegetarian": "Vegetarian",
    "vegan": "Vegan",
    "pasta": "Pasta",
    "beef": "Beef",
    "chicken": "Chicken",
    "seafood": "Seafood",
    "side": "Side",
    "dessert": "Dessert"

}

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_categories = request.form.getlist('category')
        return redirect(url_for('generate_meal_plan', categories=selected_categories))
    return render_template('index.html', meal_categories=MEAL_CATEGORIES)

@app.route('/meal-plan', methods=['GET'])
def generate_meal_plan():
    selected_categories = request.args.getlist('categories')
    meal_plan = {}
    for day in DAYS_OF_WEEK:
        meal_plan[day] = {}
        for category in selected_categories:
            meal_plan[day][category] = get_random_meal(category)
    return render_template('meal_plan.html', meal_plan=meal_plan)

@app.route('/meal-detail/<meal_id>', methods=['GET'])
def meal_detail(meal_id):
    meal = get_meal_detail(meal_id)
    return render_template('meal_detail.html', meal=meal)

def get_random_meal(category):
    base_url = 'https://www.themealdb.com/api/json/v1/1/filter.php'
    paramstr = urllib.parse.urlencode({'c': category})
    url = base_url + "?" + paramstr

    try:
        response = requests.get(url)
        data = response.json()
        meals = data.get('meals', [])
        if meals:
            return random.choice(meals)
        else:
            return None
    except requests.exceptions.RequestException as error:
        print("Error retrieving data:", error)
        return None

def get_meal_detail(meal_id):
    base_url = 'https://www.themealdb.com/api/json/v1/1/lookup.php'
    params = {'i': meal_id}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        meals = data.get('meals', [])
        if meals:
            meal = meals[0]
        else:
            meal = None
        return meal
    except requests.exceptions.RequestException as error:
        print("Error retrieving data:", error)
        return None

if __name__ == '__main__':
    app.run(debug=True)