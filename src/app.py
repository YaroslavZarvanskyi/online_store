import sys
import os
# Додаємо шлях до src, щоб Python бачив всі свої файли
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for
from repository import ProductRepository, CartRepository

app = Flask(__name__)
repo = ProductRepository()
cart = CartRepository()

@app.route('/')
def index():
    return render_template('index.html', products=repo.get_all())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = repo.get_by_id(product_id)
    if product:
        cart.add(product)
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart.remove(product_id)
    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():
    return render_template('cart.html', items=cart.get_all(), total=cart.get_total())

if __name__ == '__main__':
    app.run(debug=True)