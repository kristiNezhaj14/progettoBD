from sqlalchemy import text
from app import db
from app.models import User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem, Review
from datetime import datetime

# Dati di esempio
users = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123', 
     'nazione': 'Italia', 'citta': 'Roma', 'indirizzo': 'Via Appia 1', 'cap': '00100'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'securepass456', 
     'nazione': 'Italia', 'citta': 'Milano', 'indirizzo': 'Corso Buenos Aires 5', 'cap': '20100'},
    {'username': 'alice_jones', 'email': 'alice@example.com', 'password': 'passalice', 
     'nazione': 'USA', 'citta': 'New York', 'indirizzo': '123 Broadway', 'cap': '10001'},
    {'username': 'bob_lee', 'email': 'bob@example.com', 'password': 'passbob', 
     'nazione': 'Italia', 'citta': 'Napoli', 'indirizzo': 'Piazza del Plebiscito 10', 'cap': '80100'},
    {'username': 'charlie_brown', 'email': 'charlie@example.com', 'password': 'passcharlie', 
     'nazione': 'Francia', 'citta': 'Parigi', 'indirizzo': 'Champs-Élysées 50', 'cap': '75000'},
    {'username': 'diana_wong', 'email': 'diana@example.com', 'password': 'passdiana', 
     'nazione': 'Regno Unito', 'citta': 'Londra', 'indirizzo': 'Oxford Street 77', 'cap': 'W1D 1BS'},
    {'username': 'eric_clark', 'email': 'eric@example.com', 'password': 'passeric', 
     'nazione': 'Italia', 'citta': 'Torino', 'indirizzo': 'Via Roma 12', 'cap': '10121'},
    {'username': 'frank_woods', 'email': 'frank@example.com', 'password': 'passfrank', 
     'nazione': 'Canada', 'citta': 'Toronto', 'indirizzo': 'Bay Street 300', 'cap': 'M5H 2S8'},
    {'username': 'grace_yang', 'email': 'grace@example.com', 'password': 'passgrace', 
     'nazione': 'Australia', 'citta': 'Sydney', 'indirizzo': 'George Street 42', 'cap': '2000'},
    {'username': 'harry_potter', 'email': 'harry@example.com', 'password': 'passharry', 
     'nazione': 'Italia', 'citta': 'Firenze', 'indirizzo': 'Piazza della Signoria 8', 'cap': '50122'}
]


vendors = [
    {'username': 'vendor_one', 'email': 'vendor1@example.com', 'password': 'vendorpw789', 'piva': '12345678901', 'nome_azienda': 'Vendor One Inc.', 'indirizzo': '123 Vendor St.', 'città': 'Vendor City', 'nazione': 'Vendorland'},
    {'username': 'vendor_two', 'email': 'vendor2@example.com', 'password': 'vendorpw789', 'piva': '22345678902', 'nome_azienda': 'Vendor Two Ltd.', 'indirizzo': '456 Vendor Blvd.', 'città': 'Vendor City', 'nazione': 'Vendorland'},
    {'username': 'vendor_three', 'email': 'vendor3@example.com', 'password': 'vendorpw789', 'piva': '32345678903', 'nome_azienda': 'Vendor Three LLC', 'indirizzo': '789 Vendor Rd.', 'città': 'Vendor City', 'nazione': 'Vendorland'}
]

categories = [
    {'name': 'Electronics', 'image_url': 'phone.jpeg'},
    {'name': 'Books', 'image_url': 'phone.jpeg'},
    {'name': 'Clothing', 'image_url': 'phone.jpeg'}
]

products = [
    # Electronics
    {'name': 'Smartphone', 'description': 'Latest model smartphone', 'category_id': 1, 'price': 699.99, 'quantity': 10, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Laptop', 'description': 'High-performance laptop', 'category_id': 1, 'price': 1299.99, 'quantity': 5, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Tablet', 'description': 'Portable touchscreen tablet', 'category_id': 1, 'price': 499.99, 'quantity': 8, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Smartwatch', 'description': 'Wearable smart device', 'category_id': 1, 'price': 199.99, 'quantity': 20, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Camera', 'description': 'Digital camera with high resolution', 'category_id': 1, 'price': 899.99, 'quantity': 15, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Headphones', 'description': 'Noise-cancelling headphones', 'category_id': 1, 'price': 149.99, 'quantity': 30, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Smart TV', 'description': '4K Ultra HD Smart TV', 'category_id': 1, 'price': 999.99, 'quantity': 3, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Bluetooth Speaker', 'description': 'Wireless portable speaker', 'category_id': 1, 'price': 79.99, 'quantity': 25, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Drone', 'description': 'Quadcopter with 4K camera', 'category_id': 1, 'price': 599.99, 'quantity': 7, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Game Console', 'description': 'Next-gen gaming console', 'category_id': 1, 'price': 499.99, 'quantity': 12, 'seller_id': 3, 'image_url': 'phone.jpeg'},

    # Books
    {'name': 'Novel', 'description': 'Bestselling novel', 'category_id': 2, 'price': 19.99, 'quantity': 20, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'History Book', 'description': 'Comprehensive history book', 'category_id': 2, 'price': 29.99, 'quantity': 12, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Science Book', 'description': 'Advanced science textbook', 'category_id': 2, 'price': 39.99, 'quantity': 10, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Cookbook', 'description': 'Recipes from around the world', 'category_id': 2, 'price': 24.99, 'quantity': 15, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Biography', 'description': 'Biography of a famous figure', 'category_id': 2, 'price': 18.99, 'quantity': 18, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Fantasy Book', 'description': 'Epic fantasy novel', 'category_id': 2, 'price': 25.99, 'quantity': 25, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Children\'s Book', 'description': 'Illustrated children\'s story', 'category_id': 2, 'price': 14.99, 'quantity': 30, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Self-help Book', 'description': 'Book on personal development', 'category_id': 2, 'price': 19.99, 'quantity': 22, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Thriller Book', 'description': 'Suspenseful thriller', 'category_id': 2, 'price': 21.99, 'quantity': 10, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Art Book', 'description': 'Artistic techniques and history', 'category_id': 2, 'price': 49.99, 'quantity': 8, 'seller_id': 3, 'image_url': 'phone.jpeg'},

    # Clothing
    {'name': 'T-Shirt', 'description': 'Comfortable cotton t-shirt', 'category_id': 3, 'price': 9.99, 'quantity': 100, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Jeans', 'description': 'Denim jeans for everyday wear', 'category_id': 3, 'price': 39.99, 'quantity': 50, 'seller_id': 1, 'image_url': 'phone.jpeg'},
    {'name': 'Jacket', 'description': 'Warm and stylish jacket', 'category_id': 3, 'price': 89.99, 'quantity': 25, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Sneakers', 'description': 'Casual shoes for everyday wear', 'category_id': 3, 'price': 59.99, 'quantity': 40, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Dress', 'description': 'Elegant evening dress', 'category_id': 3, 'price': 79.99, 'quantity': 30, 'seller_id': 2, 'image_url': 'phone.jpeg'},
    {'name': 'Sweater', 'description': 'Warm wool sweater', 'category_id': 3, 'price': 49.99, 'quantity': 60, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Shorts', 'description': 'Casual shorts for summer', 'category_id': 3, 'price': 19.99, 'quantity': 80, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Hat', 'description': 'Stylish sun hat', 'category_id': 3, 'price': 15.99, 'quantity': 70, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Scarf', 'description': 'Cozy winter scarf', 'category_id': 3, 'price': 12.99, 'quantity': 50, 'seller_id': 3, 'image_url': 'phone.jpeg'},
    {'name': 'Belt', 'description': 'Leather belt for men', 'category_id': 3, 'price': 25.99, 'quantity': 30, 'seller_id': 3, 'image_url': 'phone.jpeg'}
]

orders = [
    {'user_id': 1, 'status': 'completed', 'total_price': 719.98},
    {'user_id': 2, 'status': 'pending', 'total_price': 1299.99},
    {'user_id': 3, 'status': 'completed', 'total_price': 99.99},
    {'user_id': 4, 'status': 'completed', 'total_price': 200.00},
    {'user_id': 5, 'status': 'pending', 'total_price': 499.99},
    {'user_id': 6, 'status': 'completed', 'total_price': 899.99},
    {'user_id': 7, 'status': 'pending', 'total_price': 59.99},
    {'user_id': 8, 'status': 'completed', 'total_price': 150.00},
    {'user_id': 9, 'status': 'completed', 'total_price': 300.00},
    {'user_id': 10, 'status': 'pending', 'total_price': 450.00}
]

order_items = [
    {'order_id': 1, 'product_id': 1, 'quantity': 1, 'unit_price': 699.99},
    {'order_id': 1, 'product_id': 3, 'quantity': 1, 'unit_price': 19.99},
    {'order_id': 2, 'product_id': 2, 'quantity': 1, 'unit_price': 1299.99},
    {'order_id': 3, 'product_id': 4, 'quantity': 1, 'unit_price': 99.99},
    {'order_id': 4, 'product_id': 5, 'quantity': 1, 'unit_price': 200.00},
    {'order_id': 5, 'product_id': 6, 'quantity': 1, 'unit_price': 499.99},
    {'order_id': 6, 'product_id': 7, 'quantity': 1, 'unit_price': 899.99},
    {'order_id': 7, 'product_id': 8, 'quantity': 1, 'unit_price': 59.99},
    {'order_id': 8, 'product_id': 9, 'quantity': 1, 'unit_price': 150.00},
    {'order_id': 9, 'product_id': 10, 'quantity': 1, 'unit_price': 300.00},
    {'order_id': 10, 'product_id': 11, 'quantity': 1, 'unit_price': 450.00}
]

carts = [
    {'user_id': 1},
    {'user_id': 2},
    {'user_id': 3},
    {'user_id': 4},
    {'user_id': 5},
    {'user_id': 6},
    {'user_id': 7},
    {'user_id': 8},
    {'user_id': 9},
    {'user_id': 10}
]

cart_items = [
    {'cart_id': 1, 'product_id': 1, 'quantity': 1},
    {'cart_id': 1, 'product_id': 4, 'quantity': 2},
    {'cart_id': 1, 'product_id': 6, 'quantity': 1},
    {'cart_id': 2, 'product_id': 2, 'quantity': 1},
    {'cart_id': 2, 'product_id': 5, 'quantity': 1},
    {'cart_id': 2, 'product_id': 3, 'quantity': 1},
    {'cart_id': 3, 'product_id': 4, 'quantity': 3},
    {'cart_id': 3, 'product_id': 2, 'quantity': 1},
    {'cart_id': 3, 'product_id': 7, 'quantity': 1},
    {'cart_id': 4, 'product_id': 8, 'quantity': 3},
    {'cart_id': 4, 'product_id': 9, 'quantity': 3},
    {'cart_id': 4, 'product_id': 10, 'quantity': 3},
    {'cart_id': 5, 'product_id': 11, 'quantity': 3},
    {'cart_id': 5, 'product_id': 12, 'quantity': 3},
    {'cart_id': 6, 'product_id': 13, 'quantity': 3},
    {'cart_id': 7, 'product_id': 14, 'quantity': 3},
    {'cart_id': 7, 'product_id': 15, 'quantity': 3},
    {'cart_id': 8, 'product_id': 16, 'quantity': 3},
    {'cart_id': 8, 'product_id': 17, 'quantity': 3},
    {'cart_id': 9, 'product_id': 18, 'quantity': 3},
    {'cart_id': 9, 'product_id': 19, 'quantity': 3},
    {'cart_id': 10, 'product_id': 20, 'quantity': 3},


]

reviews = [
    {'user_id': 1, 'product_id': 1, 'rating': 5, 'comment': 'Excellent phone!'},
    {'user_id': 2, 'product_id': 2, 'rating': 4, 'comment': 'Great laptop, but expensive.'},
    {'user_id': 3, 'product_id': 3, 'rating': 5, 'comment': 'Best tablet I\'ve ever used.'},
    {'user_id': 4, 'product_id': 4, 'rating': 4, 'comment': 'Good smartwatch, but battery life could be better.'},
    {'user_id': 5, 'product_id': 5, 'rating': 3, 'comment': 'Camera quality is average.'},
    {'user_id': 6, 'product_id': 6, 'rating': 5, 'comment': 'Excellent headphones for the price!'},
    {'user_id': 7, 'product_id': 7, 'rating': 5, 'comment': 'Smart TV with stunning visuals.'},
    {'user_id': 8, 'product_id': 8, 'rating': 4, 'comment': 'Good speaker, but could be louder.'},
    {'user_id': 9, 'product_id': 9, 'rating': 5, 'comment': 'Amazing drone with great camera.'},
    {'user_id': 10, 'product_id': 10, 'rating': 5, 'comment': 'Best game console on the market.'}
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
            user = User(username=user_data['username'],
            email=user_data['email'],
            nazione=user_data['nazione'], 
            città=user_data['citta'], 
            cap=user_data['cap'], 
            indirizzo=user_data['indirizzo'])
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

        # Aggiungi le categorie con image_url
        for category_data in categories:
            category = Category(name=category_data['name'], image_url=category_data['image_url'])
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
                image_url=product_data['image_url']
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
