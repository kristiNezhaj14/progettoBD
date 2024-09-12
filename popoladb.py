from sqlalchemy import text
from app import db
from app.models import User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem, Review
from datetime import datetime

# Dati di esempio
users = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'securepass456'}
]

vendors = [
    {'username': 'vendor_one', 'email': 'vendor1@example.com', 'password': 'vendorpw789', 'piva': '12345678901', 'nome_azienda': 'Vendor One Inc.', 'indirizzo': '123 Vendor St.', 'città': 'Vendor City', 'nazione': 'Vendorland'}
]

categories = [
    {'name': 'Electronics'},
    {'name': 'Books'},
    {'name': 'Clothing'}
]

products = [
    {'name': 'Smartphone', 'description': 'Latest model smartphone', 'category_id': 1, 'price': 699.99, 'quantity': 10, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Laptop', 'description': 'High-performance laptop', 'category_id': 1, 'price': 1299.99, 'quantity': 5, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Novel', 'description': 'Bestselling novel', 'category_id': 2, 'price': 19.99, 'quantity': 20, 'seller_id': 1, 'image_url': 'phone.jpeg'}
]

orders = [
    {'user_id': 1, 'status': 'completed', 'total_price': 719.98},
    {'user_id': 2, 'status': 'pending', 'total_price': 1299.99}
]

order_items = [
    {'order_id': 1, 'product_id': 1, 'quantity': 1, 'unit_price': 699.99},
    {'order_id': 1, 'product_id': 3, 'quantity': 1, 'unit_price': 19.99},
    {'order_id': 2, 'product_id': 2, 'quantity': 1, 'unit_price': 1299.99}
]

carts = [
    {'user_id': 1},
    {'user_id': 2}
]

cart_items = [
    {'cart_id': 1, 'product_id': 2, 'quantity': 1},
    {'cart_id': 2, 'product_id': 3, 'quantity': 2}
]

reviews = [
    {'user_id': 1, 'product_id': 1, 'rating': 5, 'comment': 'Excellent phone!'},
    {'user_id': 2, 'product_id': 2, 'rating': 4, 'comment': 'Great laptop, but expensive.'}
]

def populate_db():
    with app.app_context():
        # Svuota tutte le tabelle
        db.session.execute(text('TRUNCATE TABLE "user" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "vendor" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "category" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "product" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "order" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "order_item" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "cart" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "cart_item" RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE "review" RESTART IDENTITY CASCADE;'))

        # Aggiungi gli utenti
        for user_data in users:
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            db.session.add(user)
        db.session.commit()

        # Aggiungi i vendor
        for vendor_data in vendors:
            vendor = Vendor(username=vendor_data['username'], email=vendor_data['email'])
            vendor.set_password(vendor_data['password'])
            vendor.piva = vendor_data['piva']
            vendor.nome_azienda = vendor_data['nome_azienda']
            vendor.indirizzo = vendor_data['indirizzo']
            vendor.città = vendor_data['città']
            vendor.nazione = vendor_data['nazione']
            db.session.add(vendor)
        db.session.commit()

        # Aggiungi le categorie
        for category_data in categories:
            category = Category(name=category_data['name'])
            db.session.add(category)
        db.session.commit()

        # Aggiungi i prodotti
        for product_data in products:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                category_id=product_data['category_id'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                seller_id=product_data['seller_id'],
                image_url=product_data['image_url']  # Aggiungi imageurl
            )
            db.session.add(product)
        db.session.commit()

        # Aggiungi gli ordini
        for order_data in orders:
            order = Order(user_id=order_data['user_id'], status=order_data['status'], total_price=order_data['total_price'])
            db.session.add(order)
        db.session.commit()

        # Aggiungi gli articoli degli ordini
        for item_data in order_items:
            item = OrderItem(order_id=item_data['order_id'], product_id=item_data['product_id'], quantity=item_data['quantity'], unit_price=item_data['unit_price'])
            db.session.add(item)
        db.session.commit()

        # Aggiungi i carrelli
        for cart_data in carts:
            cart = Cart(user_id=cart_data['user_id'])
            db.session.add(cart)
        db.session.commit()

        # Aggiungi gli articoli dei carrelli
        for item_data in cart_items:
            item = CartItem(cart_id=item_data['cart_id'], product_id=item_data['product_id'], quantity=item_data['quantity'])
            db.session.add(item)
        db.session.commit()

        # Aggiungi le recensioni
        for review_data in reviews:
            review = Review(user_id=review_data['user_id'], product_id=review_data['product_id'], rating=review_data['rating'], comment=review_data['comment'])
            db.session.add(review)
        db.session.commit()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    populate_db()
