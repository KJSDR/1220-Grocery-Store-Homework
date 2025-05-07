from grocery_app.extensions import db
from grocery_app.utils import FormEnum
from flask_login import UserMixin

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

# Create a bridge table for the many-to-many relationship between User and GroceryItem
shopping_list_table = db.Table('shopping_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('grocery_item.id'))
)

class User(UserMixin, db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    
    # Shopping list relationship - many-to-many with GroceryItem
    shopping_list_items = db.relationship(
        'GroceryItem', 
        secondary=shopping_list_table,
        backref=db.backref('users_who_want_to_buy', lazy='dynamic'),
        lazy='dynamic'
    )

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    
    # Adding created_by to track who created the store
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(db.String)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    
    # Adding created_by to track who created the item
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')