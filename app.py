import os
from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '260694'  
db = SQLAlchemy(app)

# путь к папке, где будут сохраняться загруженные файлы
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')




class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'


@app.before_request
def create_tables():
    db.create_all()  # Создание таблиц при первом запросе



# Главная страница
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('primary.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form.get('description', '')

        # Обработка загрузки изображения
        image_file = request.files.get('image')
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = f'images/{filename}' 
        
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 

        new_product = Product(name=name, image=image_path, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('add_product'))  # Перенаправляем обратно на страницу добавления

    return render_template('add_product.html')



@app.route('/store', methods=['GET'])
def store():
    # Получаем номер страницы из параметров запроса, по умолчанию 1
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Количество товаров на странице

    # Получаем товары с пагинацией
    products = Product.query.paginate(page=page, per_page=per_page)

    return render_template('store.html', products=products)

# Страница продукта
@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

# Функция для добавления товара в корзину
@app.route('/buy/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    product = Product.query.get_or_404(product_id)

    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product.id)
    session.modified = True
    return redirect('/cart')  # Перенаправление на страницу корзины

# Страница корзины
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    total_cost = sum(product.price for product in products)
    return render_template('cart.html', products=products, total_cost=total_cost)

# Очистка корзины
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)  # Очищаем корзину
    return redirect('/cart')  # Перенаправляем обратно в корзину

if __name__ == '__main__':
    with app.app_context():  # Создаем контекст приложения
        db.create_all() 
    app.run(debug=True)

# Добавление нового продукта (раскомментируйте, если нужно)
# new_product = Product(name='Продукт 1', price=100.0, description='Описание продукта 1')
# db.session.add(new_product)
# db.session.commit()
