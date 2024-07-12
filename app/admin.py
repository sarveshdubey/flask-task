from flask_admin.contrib.sqla import ModelView
from app import admin, db
from .models import User, Category, Tag, Post, Comment

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
