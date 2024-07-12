from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Category, Tag, Post, PostTag, Comment
# Initialize Flask application and SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')  # Adjust this based on your Flask application setup
db = SQLAlchemy(app)

def populate_users():
    users = [
        {"username": "user1", "email": "user1@example.com"},
        {"username": "user2", "email": "user2@example.com"},
        {"username": "user3", "email": "user3@example.com"},
        # Add more users as needed
    ]
    for user_data in users:
        user = User(**user_data)
        db.session.add(user)
    db.session.commit()

def populate_categories():
    categories = [
        {"name": "Technology", "slug": "technology"},
        {"name": "Travel", "slug": "travel"},
        {"name": "Food", "slug": "food"},
        # Add more categories as needed
    ]
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
    db.session.commit()

def populate_tags():
    tags = [
        {"name": "Python", "slug": "python"},
        {"name": "Flask", "slug": "flask"},
        {"name": "Docker", "slug": "docker"},
        # Add more tags as needed
    ]
    for tag_data in tags:
        tag = Tag(**tag_data)
        db.session.add(tag)
    db.session.commit()

def populate_posts():
    # Assuming you have predefined categories, tags, and users
    category_tech = Category.query.filter_by(name='Technology').first()
    category_food = Category.query.filter_by(name='Food').first()
    user1 = User.query.filter_by(username='user1').first()
    user2 = User.query.filter_by(username='user2').first()

    posts = [
        {
            "title": "Introduction to Flask",
            "slug": "introduction-to-flask",
            "content": "This is an introductory post about Flask.",
            "date_created": datetime.utcnow(),
            "category_id": category_tech.id,
            "user_id": user1.id,
            "tags": [Tag.query.filter_by(name='Python').first(), Tag.query.filter_by(name='Flask').first()]
        },
        {
            "title": "Best Food Destinations",
            "slug": "best-food-destinations",
            "content": "Explore the best food destinations around the world.",
            "date_created": datetime.utcnow(),
            "category_id": category_food.id,
            "user_id": user2.id,
            "tags": [Tag.query.filter_by(name='Food').first()]
        }
        # Add more posts as needed
    ]
    for post_data in posts:
        post = Post(**post_data)
        db.session.add(post)
    db.session.commit()

def populate_comments():
    # Assuming you have posts and users already populated
    post1 = Post.query.filter_by(slug='introduction-to-flask').first()
    post2 = Post.query.filter_by(slug='best-food-destinations').first()
    user1 = User.query.filter_by(username='user1').first()
    user2 = User.query.filter_by(username='user2').first()

    comments = [
        {"content": "Great post!", "user_id": user1.id, "post_id": post1.id},
        {"content": "Looking forward to more posts like this.", "user_id": user2.id, "post_id": post1.id},
        {"content": "Amazing destinations!", "user_id": user1.id, "post_id": post2.id},
        {"content": "I want to visit these places!", "user_id": user2.id, "post_id": post2.id},
        # Add more comments as needed
    ]
    for comment_data in comments:
        comment = Comment(**comment_data)
        db.session.add(comment)
    db.session.commit()

def main():
    with app.app_context():
        populate_users()
        populate_categories()
        populate_tags()
        populate_posts()
        populate_comments()

if __name__ == "__main__":
    main()
