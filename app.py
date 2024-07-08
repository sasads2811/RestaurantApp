from flask import Flask, render_template, request, jsonify, redirect
from models import db, FoodItem, Contact, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', 'all')

    food_items = FoodItem.query

    if search_query:
        food_items = food_items.filter(FoodItem.name.like(f'%{search_query}%'))

    if category_filter != 'all':
        food_items = food_items.filter_by(category=category_filter)

    food_items = food_items.all()

    reviews = Review.query.all()
    return render_template('index.html', food_items=food_items, reviews=reviews)


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not name or not email or not subject or not message:
        return jsonify({'error': 'All fields are required'}), 400

    new_contact = Contact(name=name, email=email, subject=subject, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return redirect('/')


@app.route('/submit_review', methods=['POST'])
def submit_review():
    name = request.form.get('name')
    review = request.form.get('review')


    if not name or not review:
        return jsonify({'error': 'All fields are required'}), 400

    new_review = Review(name=name, review=review)
    db.session.add(new_review)
    db.session.commit()

    return redirect('/#review')


def populate_db():
    food_items = [
        FoodItem(name='Pepperoni Pizza', category='Pizza', size='Small', price=9.99,
                 image_url='https://www.pizzeriavictoria.es/wp-content/uploads/2020/02/PepperoniCO.jpg.webp'),
        FoodItem(name='Neapolitan Pizza', category='Pizza', size='Medium', price=12.99,
                 image_url='https://caputoflour.com/cdn/shop/articles/NeapolitanPizza.jpg?v=1695313385'),
        FoodItem(name='Margherita Pizza', category='Pizza', size='Large', price=15.99,
                 image_url='https://images.prismic.io/eataly-us/ed3fcec7-7994-426d-a5e4-a24be5a95afd_pizza-recipe-main.jpg?auto=compress,format'),
        FoodItem(name='Tomato Pasta', category='Pasta', size='Small', price=8.99,
                 image_url='https://www.allrecipes.com/thmb/5SdUVhHTMs-rta5sOblJESXThEE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/11691-tomato-and-garlic-pasta-ddmfs-3x4-1-bf607984a23541f4ad936b33b22c9074.jpg'),
        FoodItem(name='Garlic Tomato', category='Pasta', size='Medium', price=10.99,
                 image_url='https://i0.wp.com/spainonafork.com/wp-content/uploads/2022/07/image6-2022-07-03T030621-11.png?fit=750%2C750&ssl=1'),
        FoodItem(name='Vegan Pasta', category='Pasta', size='Large', price=12.99,
                 image_url='https://images.immediate.co.uk/production/volatile/sites/30/2018/03/Vegan-creamy-spinach-and-mushroom-penne-e2817d1.jpg?quality=90&resize=440,400'),
        FoodItem(name='Pistachio Gelato', category='Gelato', size='1 Scoop', price=4.99,
                 image_url='https://www.thedeliciouscrescent.com/wp-content/uploads/2023/05/Pistachio-Gelato-5.jpg'),
        FoodItem(name='Raspberry Crisp Gelato', category='Gelato', size='1 Scoop', price=4.99,
                 image_url='https://thesweetandsimplekitchen.com/wp-content/uploads/2017/06/IMG_8558.jpg'),
        FoodItem(name='Brownie Fudge Gelato', category='Gelato', size='1 Scoop', price=4.99,
                 image_url='https://i1.wp.com/www.certifiedpastryaficionado.com/wp-content/uploads/2019/07/Fudge-Brownie-Ice-Cream_IMG_5270.jpg?resize=800%2C1200'),
    ]

    db.session.bulk_save_objects(food_items)
    db.session.commit()


def check_and_populate_db():
    if not FoodItem.query.first():
        print('Database is empty')
        print('Populating database')
        populate_db()
    else:
        print('Database is populated')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        check_and_populate_db()
        app.run(debug=True)
