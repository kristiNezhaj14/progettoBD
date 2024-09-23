from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from datetime import datetime
import os


from werkzeug.utils import secure_filename

from app.models import User, Vendor,Product,CartItem, Cart, Category, Order, OrderItem,Review
from app.forms import RegistrationForm, LoginForm, VendorRegistrationForm

# Estensioni permesse per le immagini
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            # Prima controlla se l'utente è un 'User'
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user, remember=form.remember_me.data)
                flash('Login successful', 'success')
                return redirect(url_for('home'))  # Reindirizza alla home per gli utenti normali
            
            # Se non è un 'User', controlla se è un 'Vendor'
            vendor = Vendor.query.filter_by(username=username).first()
            if vendor and vendor.check_password(password):
                login_user(vendor, remember=form.remember_me.data)
                flash('Login successful', 'success')
                return redirect(url_for('vendorprofile'))  # Reindirizza alla pagina del venditore
            
            # Se non trova corrispondenza
            flash('Login failed. Check your username and/or password.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/logout',methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('User registered successfully', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')

        return render_template('register.html', form=form)

    @app.route('/vendor', methods=['GET', 'POST'])
    def vendor():
        form = VendorRegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            piva = form.piva.data
            nome_azienda = form.nome_azienda.data
            indirizzo = form.indirizzo.data
            città = form.città.data
            nazione = form.nazione.data
            # Verifica se lo username o l'email sono già utilizzati da un utente
            if User.query.filter_by(username=username).first():
                flash('Username already exists in User accounts', 'danger')
                return redirect(url_for('vendor'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered in User accounts', 'danger')
                return redirect(url_for('vendor'))
            # Verifica se lo username o l'email sono già utilizzati da un venditore
            if Vendor.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('vendor'))

            if Vendor.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('vendor'))

            new_vendor = Vendor(username=username, email=email, piva=piva, nome_azienda=nome_azienda, indirizzo=indirizzo, città=città, nazione=nazione)
            new_vendor.set_password(password)
            db.session.add(new_vendor)
            try:
                db.session.commit()
                flash('Vendor registered successfully', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')

        return render_template('vendor.html', form=form)


    @app.route('/categories')
    def categories():
        # Ottieni tutte le categorie dal database
        categories = Category.query.all()
        return render_template('categories.html', categories=categories)

    @app.route('/offersbanner')
    def offersbanner():
        products = Product.query.all()
        return render_template('offersbanner.html',products=products)

    @app.route('/cart')
    @login_required
    def cart():
        # Recupera il carrello dell'utente loggato
        cart = Cart.query.filter_by(user_id=current_user.id).first()

        # Se l'utente non ha un carrello, creane uno vuoto
        if not cart:
            cart_items = []
        else:
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Passa i dati del carrello al template
        return render_template('cart.html', cart_items=cart_items,total_price=total_price)

    @app.route('/product/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        reviews = Review.query.filter_by(product_id=product.id).all()
        
        # Calcolo della media delle valutazioni
        average_rating = 0
        if reviews:
            average_rating = sum([r.rating for r in reviews]) / len(reviews)
        
        # Controlla se l'utente ha già lasciato una recensione
        user_review = Review.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        
        if request.method == 'POST':
            if not user_review:  # Se non ha ancora valutato
                rating = int(request.form.get('rating'))
                comment = request.form.get('comment')
                new_review = Review(
                    user_id=current_user.id,
                    product_id=product_id,
                    rating=rating,
                    comment=comment
                )
                db.session.add(new_review)
                db.session.commit()
                flash('Hai valutato il prodotto con successo!', 'success')
                return redirect(url_for('product_detail', product_id=product_id))
            else:
                flash('Hai già valutato questo prodotto.', 'danger')

        return render_template('product.html', product=product, average_rating=average_rating, user_review=user_review)


        

    
    @app.route('/contacts')
    def contacts():
        return render_template('contacts.html')
    
    @app.route('/faq')
    def faq():
        return render_template('faq.html')
    
    @app.route('/found')
    def found():
        category_filter = request.args.get('filter1')
        price_filter = request.args.get('filter2')
        rating_filter = request.args.get('filter3')

        query = Product.query

        # Filtra per categoria
        if category_filter and category_filter != 'tutti':
            query = query.filter(Product.category_id == category_filter)

        # Ordina per prezzo
        if price_filter == 'Crescente':
            query = query.order_by(Product.price.asc())
        elif price_filter == 'Decrescente':
            query = query.order_by(Product.price.desc())

        # Ordina per valutazione (questo esempio non ha un campo di valutazione reale)
        # Se avessi un campo rating, aggiungi la logica qui

        products = query.all()
        categories = Category.query.all()

        return render_template('found.html', products=products, categories=categories)

    
    @app.route('/offers')
    def offers():
        return render_template('offers.html')
    
    @app.route('/product')
    def product():
        return render_template('product.html')
    
    @app.route('/terms')
    def terms():
        return render_template('terms.html')
    
    @app.route('/question')
    def question():
        return render_template('question.html')

    @app.route('/ordine/<int:order_id>', methods=['GET'])
    @login_required
    def ordine(order_id):
        # Recupera l'ordine in base all'ID
        order = Order.query.get_or_404(order_id)
        
        # Recupera gli articoli dell'ordine
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        
        # Calcola il prezzo totale dell'ordine
        total_price = sum(item.unit_price * item.quantity for item in order_items)
        
        return render_template('ordine.html', order_items=order_items, total_price=total_price)

    

    
    @app.route('/productreg')
    def productreg():
        return render_template('productreg.html')
    
    @app.route('/vendorprofile')
    @login_required
    def vendorprofile():
       
        products = Product.query.filter_by(seller_id=current_user.id).all()
        product_ids = [product.id for product in products]
        orders = Order.query.join(OrderItem).filter(OrderItem.product_id.in_(product_ids)).all()
        
        return render_template('vendorprofile.html', products=products, orders=orders)


    @app.route('/pagamento')
    def pagamento():
        return render_template('pagamento.html')


    @app.route('/insert')
    def insert():
        categorie = Category.query.all()
        return render_template('insertProduct.html', categorie=categorie)


    @app.route('/update_shipping', methods=['POST'])
    @login_required
    def update_shipping():
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip')
        nation = request.form.get('nation')

        # Aggiorna i campi dell'utente loggato
        current_user.indirizzo = address
        current_user.città = city
        current_user.cap = zip_code
        current_user.nazione = nation

        # Salva le modifiche nel database
        try:
            db.session.commit()
            flash('Informazioni di spedizione aggiornate con successo!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Errore durante l\'aggiornamento delle informazioni. Riprova.', 'danger')

        return redirect(url_for('profile'))



    @app.route('/change_password', methods=['POST'])
    @login_required
    def change_password():
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Controlla se la password attuale è corretta
        if not current_user.check_password(current_password):
            flash('La password attuale non è corretta.', 'danger')
            return redirect(url_for('profile'))

        # Controlla che la nuova password e la conferma coincidano
        if new_password != confirm_password:
            flash('Le nuove password non coincidono.', 'danger')
            return redirect(url_for('profile'))

        # Aggiorna la password nel database
        current_user.set_password(new_password)
        try:
            db.session.commit()
            flash('Password aggiornata con successo!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Errore durante l\'aggiornamento della password. Riprova.', 'danger')

        return redirect(url_for('profile'))




    @app.route('/profile')
    @login_required
    def profile():
        # Recupera tutti gli ordini effettuati dall'utente loggato
        orders = Order.query.filter_by(user_id=current_user.id).all()
        
        # Recupera tutti i prodotti associati agli ordini dell'utente
        products = []
        for order in orders:
            for item in order.items:
                products.append({
                    'product': item.product, 
                    'quantity': item.quantity, 
                    'unit_price': item.unit_price,
                    'order_id': order.id,
                    'order_status': order.status,  # Stato dell'ordine
                    'order_date': order.created_at,  # Data dell'ordine
                    'product_image': item.product.image_url  # Immagine del prodotto
                })

        # Renderizza la pagina profilo con i prodotti
        return render_template('profile.html', products=products)


    @app.route('/process_payment', methods=['POST'])
    @login_required
    def process_payment():
        # Recupera il carrello dell'utente loggato
        cart = Cart.query.filter_by(user_id=current_user.id).first()

        # Verifica che ci siano prodotti nel carrello
        if not cart or not cart.items:
            flash('Il carrello è vuoto. Aggiungi dei prodotti prima di completare il pagamento.', 'danger')
            return redirect(url_for('cart'))

        # Calcola il prezzo totale
        total_price = sum(item.product.price * item.quantity for item in cart.items)

        # Crea un nuovo ordine con lo stato 'completed'
        new_order = Order(
            user_id=current_user.id,
            status='completed',
            total_price=total_price,
            created_at=datetime.utcnow()
        )
        db.session.add(new_order)
        db.session.commit()

        # Aggiungi i prodotti del carrello all'ordine
        for item in cart.items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            db.session.add(order_item)

        # Svuota il carrello eliminando gli articoli
        for item in cart.items:
            db.session.delete(item)

        # Salva i cambiamenti nel database
        db.session.commit()

        flash('Pagamento completato con successo. Il tuo ordine è stato creato.', 'success')
        return redirect(url_for('profile'))





    @app.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        
        # Elimina manualmente gli articoli di carrello associati al prodotto
        cart_items = CartItem.query.filter_by(product_id=product_id).all()
        for item in cart_items:
            db.session.delete(item)
        
        # Elimina manualmente gli articoli di ordine associati al prodotto
        order_items = OrderItem.query.filter_by(product_id=product_id).all()
        for item in order_items:
            db.session.delete(item)
            

        reviews = Review.query.filter_by(product_id=product_id).all()
        for review in reviews:
            db.session.delete(review)
        
        # Elimina il prodotto
        db.session.delete(product)
        
        try:
            db.session.commit()
            flash('Prodotto e articoli associati eliminati con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'eliminazione del prodotto: {str(e)}', 'danger')

        return redirect(url_for('vendorprofile'))



    @app.route('/mark_as_shipped/<int:order_id>', methods=['POST'])
    @login_required
    def mark_as_shipped(order_id):
        # Recupera l'ordine in base all'ID
        order = Order.query.get_or_404(order_id)
        
        # Verifica se lo stato dell'ordine è "in elaborazione"
        if order.status == 'pending':
            order.status = 'completed'  # Aggiorna lo stato dell'ordine a "spedito"
            db.session.commit()
            flash(f'L\'ordine #{order.id} è stato segnato come spedito.', 'success')
        else:
            flash(f'L\'ordine #{order.id} non può essere aggiornato perché non è in elaborazione.', 'danger')
        
        return redirect(url_for('vendorprofile'))



    @app.route('/carica_prodotto', methods=['POST'])
    @login_required
    def carica_prodotto():
        nome = request.form['nome']
        categoria_id = request.form['categoria']  # Prendi l'ID della categoria dal form
        prezzo = request.form['prezzo']
        quantity = request.form['quantity']
        description = request.form['description']
        immagine_file = request.files['immagine']
        
        if immagine_file and allowed_file(immagine_file.filename):
            image_filename = secure_filename(immagine_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            immagine_file.save(image_path)
            
            # Inserisci il nuovo prodotto nel database
            nuovo_prodotto = Product(
                name=nome, 
                description=description,  
                category_id=int(categoria_id),  # Assicurati che sia un intero
                price=float(prezzo), 
                quantity=int(quantity),
                seller_id=current_user.id,
                image_url=image_filename
            )
            
            db.session.add(nuovo_prodotto)
            db.session.commit()

            flash('Prodotto caricato con successo!', 'success')
            return redirect(url_for('vendorprofile'))
        else:
            flash('Errore durante il caricamento dell\'immagine', 'danger')
            return redirect(url_for('vendorprofile'))


    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    @login_required
    def add_to_cart(product_id):
        # Trova il prodotto selezionato
        product = Product.query.get_or_404(product_id)

        # Recupera il carrello dell'utente loggato
        cart = Cart.query.filter_by(user_id=current_user.id).first()

        # Se l'utente non ha un carrello, creane uno nuovo
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        # Controlla se il prodotto è già presente nel carrello
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

        if cart_item:
            # Se il prodotto è già presente, aggiorna la quantità
            cart_item.quantity += 1
        else:
            # Altrimenti, aggiungi un nuovo prodotto al carrello
            cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
            db.session.add(cart_item)

        try:
            db.session.commit()
            flash('Prodotto aggiunto al carrello con successo!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Errore durante l\'aggiunta del prodotto al carrello.', 'danger')

        return redirect(url_for('cart'))


    @app.route('/search', methods=['GET'])
    def search_products():
        keyword = request.args.get('keyword', '')

        # Cerca nei prodotti per nome, descrizione e nome della categoria
        results = Product.query.join(Category).filter(
            (Product.name.ilike(f'%{keyword}%')) |
            (Product.description.ilike(f'%{keyword}%')) |
            (Category.name.ilike(f'%{keyword}%'))
        ).all()

        return render_template('found.html', products=results, keyword=keyword)
    





