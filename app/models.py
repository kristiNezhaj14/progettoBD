from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import event
from sqlalchemy import DDL

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    indirizzo = db.Column(db.String(200))
    città = db.Column(db.String(100))
    nazione = db.Column(db.String(100))
    cap = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))

    __table_args__ = (
        db.CheckConstraint("id > 0", name='id_positive'),
        db.CheckConstraint("LENGTH(username) > 0", name='username_not_empty'),
        db.CheckConstraint("LENGTH(email) > 0", name='email_not_empty'),
        db.CheckConstraint('LENGTH(password_hash) >= 8', name='password_length_check'),
        db.CheckConstraint("email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='valid_email_check'),
        db.CheckConstraint("indirizzo ~ '[0-9]'", name='indirizzo_check'),
        db.CheckConstraint("città ~ '^[A-Za-zÀ-ÖØ-öø-ÿ ]+$'", name='città_check'),
        db.CheckConstraint("nazione ~ '^[A-Za-zÀ-ÖØ-öø-ÿ ]+$'", name='nazione_check'),
        db.CheckConstraint("cap ~ '^[0-9 ]+$'", name='cap_check'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    class UserPasswordLog(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        old_password_hash = db.Column(db.String(256))
        changed_at = db.Column(db.DateTime, server_default=db.func.now())

    trigger_log_password = """
    CREATE OR REPLACE FUNCTION password_change() RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.password_hash != NEW.password_hash THEN
            INSERT INTO user_password_log (user_id, old_password_hash)
            VALUES (NEW.id, OLD.password_hash);
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER password_change_trigger AFTER UPDATE ON "user"
    FOR EACH ROW EXECUTE FUNCTION password_change();
    """
    event.listen(db.metadata, 'after_create', DDL(trigger_log_password))


class Vendor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    piva = db.Column(db.String(20))
    nome_azienda = db.Column(db.String(100))
    indirizzo = db.Column(db.String(200))
    città = db.Column(db.String(100))
    nazione = db.Column(db.String(100))

    __table_args__ = (
        db.CheckConstraint(id > 0, name='id_positive'),
        db.CheckConstraint("LENGTH(email) > 0", name='email_not_empty'),
        db.CheckConstraint("LENGTH(piva) = 11", name='piva_correct_length'),
        db.CheckConstraint("LENGTH(nome_azienda) > 0", name='nome_azienda_not_empty'),
        db.CheckConstraint("LENGTH(indirizzo) > 0", name='indirizzo_not_empty'),
        db.CheckConstraint("LENGTH(cap) > 0", name='cap_not_empty'),
        db.CheckConstraint("LENGTH(città) > 0", name='città_not_empty'),
        db.CheckConstraint("LENGTH(nazione) > 0", name='nazione_not_empty'),
        db.CheckConstraint('LENGTH(password_hash) >= 8', name='password_length_check'),    
        db.CheckConstraint("email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='valid_email_check'),          
        db.CheckConstraint('indirizzo LIKE "%[0-9]%"', name='indirizzo_check'),
        db.CheckConstraint("città ~ '^[A-Za-zÀ-ÖØ-öø-ÿ ]+$'", name='città_check'),
        db.CheckConstraint("nazione ~ '^[A-Za-zÀ-ÖØ-öø-ÿ ]+$'", name='nazione_check'),
        db.CheckConstraint("piva ~ '^[0-9 ]+$'", name='piva_check'),
        db.CheckConstraint("cap ~ '^[0-9 ]+$'", name='cap_check')
    )

    class VendorPasswordLog(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
        old_password_hash = db.Column(db.String(256))
        changed_at = db.Column(db.DateTime, server_default=db.func.now())

    trigger_log_password = """
    CREATE OR REPLACE FUNCTION password() RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.password_hash != NEW.password_hash THEN
            INSERT INTO vendor_password_log (vendor_id, old_password_hash)
            VALUES (NEW.id, OLD.password_hash);
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER password_trigger AFTER UPDATE ON "vendor"
    FOR EACH ROW EXECUTE FUNCTION password();
    """

    event.listen(db.metadata, 'after_create', DDL(trigger_log_password))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Vendor {}>'.format(self.username)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    image_url = db.Column(db.String(256), nullable=True) 
    __table_args__ = (
        db.CheckConstraint(id > 0, name='id_positive'),
    )

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_url = db.Column(db.String(256), nullable=True)
    cart_items = db.relationship('CartItem', backref='product_ref', cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='product', lazy=True)
    __table_args__ = (
        db.CheckConstraint(id > 0, name='id_positive'),
        db.CheckConstraint(category_id > 0, name='category_id_positive'),
        db.CheckConstraint(price > 0, name='price_positive'),
        db.CheckConstraint(quantity > 0, name='quantity_positive'),
        db.CheckConstraint(seller_id > 0, name='seller_id_positive'),
        db.CheckConstraint(price <= 10000, name='price_limit'),
        db.CheckConstraint('created_at <= CURRENT_TIMESTAMP', name='created_at_past'),
        db.CheckConstraint('updated_at <= CURRENT_TIMESTAMP', name='updated_at_past'),
        db.CheckConstraint('created_at <= updated_at', name='created_before_updated'),
    )

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='cart_product_items')
    __table_args__ = (
        db.CheckConstraint('id > 0', name='id_positive'),
        db.CheckConstraint('cart_id >= 0', name='cart_id_positive'),
        db.CheckConstraint('product_id > 0', name='product_id_positive'),
        db.CheckConstraint('quantity >= 0', name='quantity_positive'),
    )

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    status = db.Column(db.String(32), default='pending')
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    items = db.relationship('OrderItem', backref='order', lazy='joined', cascade='all, delete-orphan')

    __table_args__ = (
        db.CheckConstraint('id > 0', name='id_positive'),
        db.CheckConstraint('user_id > 0', name='user_id_positive'),
        db.CheckConstraint('total_price >= 0', name='total_price_positive'),
    ) 
    trigger_total = """
    CREATE OR REPLACE FUNCTION total_price() RETURNS TRIGGER AS $$
    DECLARE calculated_total FLOAT := 0;
    BEGIN
        SELECT SUM(order_item.unit_price * order_item.quantity) 
        INTO calculated_total FROM "order_item"
        WHERE order_item.order_id = NEW.id;
        IF NEW.total_price != calculated_total THEN
            RAISE EXCEPTION 'Total price mismatch: % (should be %)', NEW.total_price, calculated_total;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER order_total_price BEFORE INSERT OR UPDATE ON "order"
    FOR EACH ROW EXECUTE FUNCTION total_price();
    """

    event.listen(db.metadata, 'after_create', DDL(trigger_total))



    trigger_cancellation = """
    CREATE OR REPLACE FUNCTION cancellation() RETURNS TRIGGER AS $$
    BEGIN
        RAISE NOTICE 'Order % has been cancelled', OLD.id; RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER cancellation_trigger AFTER DELETE ON "order"
    FOR EACH ROW EXECUTE FUNCTION cancellation();
    """

    event.listen(db.metadata,'after_create',DDL(trigger_cancellation))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

    __table_args__ = (
        db.CheckConstraint('id > 0', name='id_positive'),
        db.CheckConstraint('order_id > 0', name='order_id_positive'),
        db.CheckConstraint('product_id > 0', name='product_id_positive'),
        db.CheckConstraint('quantity > 0', name='quantity_positive'),
        db.CheckConstraint('unit_price > 0', name='unit_price_positive'),
        db.UniqueConstraint('order_id', 'product_id', name='unique_product_in_order'),
    )

    trigger = """

    CREATE OR REPLACE FUNCTION update_unit_price() RETURNS TRIGGER AS $$
    BEGIN
        SELECT price INTO NEW.unit_price
        FROM product 
        WHERE id = NEW.product_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER set_unit_price
    BEFORE INSERT OR UPDATE ON order_item"
    FOR EACH ROW
    EXECUTE FUNCTION update_unit_price();
"""

    event.listen(db.metadata, 'after_create', DDL(trigger))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    user = db.relationship('User', backref='reviews', lazy=True)

    __table_args__ = (
        db.CheckConstraint('id > 0', name='id_positive'),
        db.CheckConstraint('user_id > 0', name='user_id_positive'),
        db.CheckConstraint('product_id > 0', name='product_id_positive'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
        db.CheckConstraint('created_at IS NOT NULL', name='created_at_positive'),
        db.CheckConstraint('updated_at IS NOT NULL', name='updated_at_positive'),
        db.CheckConstraint('created_at <= CURRENT_TIMESTAMP', name='created_at_past'),
        db.CheckConstraint('updated_at <= CURRENT_TIMESTAMP', name='updated_at_past'),
        db.CheckConstraint('created_at <= updated_at', name='created_before_updated'),
    )

def set_default_image(mapper, connection, target):
    
    if hasattr(target, 'image_url') and not target.image_url:
        target.image_url = '/static/cart-purple.png'


classes_with_images = [Category, Product, OrderItem] 

for cls in classes_with_images:
    event.listen(cls, 'before_insert', set_default_image)
    event.listen(cls, 'before_update', set_default_image)