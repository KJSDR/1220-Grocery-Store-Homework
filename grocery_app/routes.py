from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

# Import app and db from extensions
from grocery_app.extensions import db, bcrypt

# Define blueprints
main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Main Routes                  #
##########################################

@main.route('/')
def homepage():
    """Display the homepage with a list of all grocery stores."""
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    """Route to create a new grocery store."""
    # Create a GroceryStoreForm
    form = GroceryStoreForm()

    # If form was submitted and was valid
    if form.validate_on_submit():
        # Create a new GroceryStore object and save it to the database
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user  # Add the current user as the creator
        )
        db.session.add(new_store)
        db.session.commit()
        
        # Flash a success message
        flash('New store created successfully!')
        
        # Redirect the user to the store detail page
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    # Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    """Route to create a new grocery item."""
    # Create a GroceryItemForm
    form = GroceryItemForm()

    # If form was submitted and was valid
    if form.validate_on_submit():
        # Create a new GroceryItem object and save it to the database
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user  # Add the current user as the creator
        )
        db.session.add(new_item)
        db.session.commit()
        
        # Flash a success message
        flash('New item created successfully!')
        
        # Redirect the user to the item detail page
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    # Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    """Route to view and update a grocery store's details."""
    store = GroceryStore.query.get(store_id)
    
    # Create a GroceryStoreForm and pass in obj=store
    form = GroceryStoreForm(obj=store)

    # If form was submitted and was valid
    if form.validate_on_submit():
        # Update the GroceryStore object and save it to the database
        store.title = form.title.data
        store.address = form.address.data
        # Don't update created_by - it should remain the original creator
        db.session.commit()
        
        # Flash a success message
        flash('Store updated successfully!')
        
        # Redirect the user to the store detail page
        return redirect(url_for('main.store_detail', store_id=store.id))

    # Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    """Route to view and update a grocery item's details."""
    item = GroceryItem.query.get(item_id)
    
    # Create a GroceryItemForm and pass in obj=item
    form = GroceryItemForm(obj=item)

    # If form was submitted and was valid
    if form.validate_on_submit():
        # Update the GroceryItem object and save it to the database
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        # Don't update created_by - it should remain the original creator
        db.session.commit()
        
        # Flash a success message
        flash('Item updated successfully!')
        
        # Redirect the user to the item detail page
        return redirect(url_for('main.item_detail', item_id=item.id))

    # Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    """Add an item to the current user's shopping list."""
    item = GroceryItem.query.get(item_id)
    
    if item not in current_user.shopping_list_items.all():
        current_user.shopping_list_items.append(item)
        db.session.commit()
        flash(f'{item.name} added to your shopping list!')
    else:
        flash(f'{item.name} is already in your shopping list!')
    
    return redirect(url_for('main.item_detail', item_id=item_id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    """Display the current user's shopping list."""
    shopping_list_items = current_user.shopping_list_items.all()
    return render_template('shopping_list.html', shopping_list_items=shopping_list_items)

@main.route('/remove_from_shopping_list/<item_id>', methods=['POST'])
@login_required
def remove_from_shopping_list(item_id):
    """Remove an item from the current user's shopping list (stretch challenge)."""
    item = GroceryItem.query.get(item_id)
    
    if item in current_user.shopping_list_items.all():
        current_user.shopping_list_items.remove(item)
        db.session.commit()
        flash(f'{item.name} removed from your shopping list!')
    
    return redirect(url_for('main.shopping_list'))

##########################################
#           Auth Routes                  #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up page."""
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('main.homepage'))