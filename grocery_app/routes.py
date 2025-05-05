from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, ItemCategory
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    """Display the homepage with a list of all grocery stores."""
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    """Route to create a new grocery store."""
    # Create a GroceryStoreForm
    form = GroceryStoreForm()

    # If form was submitted and was valid
    if form.validate_on_submit():
        # Create a new GroceryStore object and save it to the database
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
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
            store=form.store.data
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
        db.session.commit()
        
        # Flash a success message
        flash('Store updated successfully!')
        
        # Redirect the user to the store detail page
        return redirect(url_for('main.store_detail', store_id=store.id))

    # Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
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
        db.session.commit()
        
        # Flash a success message
        flash('Item updated successfully!')
        
        # Redirect the user to the item detail page
        return redirect(url_for('main.item_detail', item_id=item.id))

    # Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)