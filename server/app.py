#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Route to get all bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    response = [bakery.to_dict() for bakery in all_bakeries]
    return make_response(jsonify(response), 200)

# Route to get a bakery by ID, including its baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        response = bakery.to_dict_with_baked_goods()
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
# Route to get baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(response), 200)

# Route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return make_response(jsonify(baked_good.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
