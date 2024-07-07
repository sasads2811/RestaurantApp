from flask import Flask, render_template, request
from models import db, FoodItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', 'all')
    size_filter = request.args.get('size', 'all')

    food_items = FoodItem.query

    if search_query:
        food_items = food_items.filter(FoodItem.name.like(f'%{search_query}%'))

    if category_filter != 'all':
        food_items = food_items.filter_by(category=category_filter)

    if size_filter != 'all':
        food_items = food_items.filter_by(size=size_filter)

    food_items = food_items.all()
    return render_template('index.html', food_items=food_items)


if __name__ == '__main__':
    app.run(debug=True)
