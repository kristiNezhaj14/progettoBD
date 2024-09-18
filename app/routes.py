from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from datetime import datetime


from app.models import User, Vendor,Product,CartItem, Cart, Category, Order, OrderItem
from app.forms import RegistrationForm, LoginForm, VendorRegistrationForm

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

    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        return render_template('product.html', product=product)
    
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
    

    
    @app.route('/productreg')
    def productreg():
        return render_template('productreg.html')
    
    @app.route('/vendorprofile')
    def vendorprofile():
        return render_template('vendorprofile.html')

    @app.route('/pagamento')
    def pagamento():
        return render_template('pagamento.html')


    @app.route('/insert')
    def insert():
        return render_template('insert.html')


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

