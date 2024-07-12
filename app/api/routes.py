from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse
from app import db
from app.models import User, Category, Tag, Post, Comment
from flask_login import current_user
from .serializers import *
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

class UserAPI(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"id": user.id, "username": user.username, "email": user.email}



class CategoryAPI(Resource):
    def get(self):
        categories = Category.query.all()
        result = [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in categories]
        return jsonify(result)
    
    def post(self):
        data = request.get_json()
        new_category = Category(name=data['name'], slug=data['slug'])
        db.session.add(new_category)
        db.session.commit()
        return {'message': 'Category created successfully'}, 201

    def put(self, category_id):
        data = request.get_json()
        category = Category.query.get_or_404(category_id)
        if 'name' in data:
            category.name = data['name']
        if 'slug' in data:
            category.slug = data['slug']
        db.session.commit()
        return {'message': 'Category updated successfully'}

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}

    
class TagAPI(Resource):
    def get(self, tag_id=None):
        if tag_id:
            tag = Tag.query.get_or_404(tag_id)
            return {"id": tag.id, "name": tag.name, "slug": tag.slug}
        tags = Tag.query.all()
        result = [{'id': t.id, 'name': t.name, 'slug': t.slug} for t in tags]
        return jsonify(result)

    def post(self):
        data = request.get_json()
        new_tag = Tag(name=data['name'], slug=data['slug'])
        db.session.add(new_tag)
        db.session.commit()
        return {'message': 'Tag created successfully'}, 201

    def put(self, tag_id):
        data = request.get_json()
        tag = Tag.query.get_or_404(tag_id)
        if 'name' in data:
            tag.name = data['name']
        if 'slug' in data:
            tag.slug = data['slug']
        db.session.commit()
        return {'message': 'Tag updated successfully'}

    def delete(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {'message': 'Tag deleted successfully'}


class BlogAPI(Resource):
    def get(self, blog_id=None):
        if blog_id:
            blog = Post.query.get_or_404(blog_id)
            schema = BlogSchema()
            result = schema.dump(blog)
            
            # Add comments count
            result['comments_count'] = len(blog.comments)

            # Check if the current user has commented
            if current_user.is_authenticated:
                user_comments = Comment.query.filter_by(blog_id=blog_id, user_id=current_user.id).count()
                result['is_user_comment'] = user_comments > 0
            else:
                result['is_user_comment'] = False

            return jsonify(result)
        
        blogs = Post.query.all()
        result = []
        for blog in blogs:
            schema = BlogSchema()
            blog_data = schema.dump(blog)
            blog_data['comments_count'] = len(blog.comments)
            blog_data['is_user_comment'] = False
            result.append(blog_data)
        
        return jsonify(result)

    def post(self):
        data = request.get_json()
        schema = BlogSchema()
        blog_data = schema.load(data)
        new_blog = Post(
            title=blog_data['title'],
            slug=blog_data['slug'],
            content=blog_data['content'],
            category_id=blog_data['category_id'],
            user_id=blog_data['user_id']
        )
        
        # Add tags
        for tag_data in blog_data['tags']:
            tag = Tag.query.get(tag_data['id'])
            if tag:
                new_blog.tags.append(PostTag(tag=tag))

        db.session.add(new_blog)
        db.session.commit()
        return schema.dump(new_blog), 201

    def put(self, blog_id):
        data = request.get_json()
        blog = Post.query.get_or_404(blog_id)
        schema = BlogSchema()
        blog_data = schema.load(data)
        
        blog.title = blog_data['title']
        blog.slug = blog_data['slug']
        blog.content = blog_data['content']
        blog.category_id = blog_data['category']['id']
        blog.user_id = blog_data['author']['id']

        # Update tags
        blog.tags = []
        for tag_data in blog_data['tags']:
            tag = Tag.query.get(tag_data['id'])
            if tag:
                blog.tags.append(PostTag(tag=tag))

        db.session.commit()
        return schema.dump(blog)

    def delete(self, blog_id):
        blog = Post.query.get_or_404(blog_id)
        db.session.delete(blog)
        db.session.commit()
        return '', 204

    
api.add_resource(UserAPI, '/users/<int:user_id>')
api.add_resource(CategoryAPI, '/categories', '/categories/<int:category_id>')
api.add_resource(TagAPI, '/tags', '/tags/<int:tag_id>')
api.add_resource(BlogAPI, '/blogs', '/blogs/<int:blog_id>')

