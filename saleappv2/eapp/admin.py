from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product

from eapp import db, app

admin = Admin(app=app, name="e-Commerce's Admin")
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))