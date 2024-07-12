from marshmallow import Schema, fields, post_load
from app.models import Post, Category, Tag, User, Comment, PostTag

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)

class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    user = fields.Nested(UserSchema)
    date_created = fields.DateTime()

class BlogSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    slug = fields.Str(required=True)
    content = fields.Str(required=True)
    date_created = fields.DateTime(dump_only=True)
    category = fields.Nested(CategorySchema, attribute="category_id")
    author = fields.Nested(UserSchema, attribute="user_id")
    tags = fields.Nested(TagSchema, many=True, attribute="tags")
    comments = fields.Nested(CommentSchema, many=True)
    comments_count = fields.Int(dump_only=True)
    is_user_comment = fields.Bool(dump_only=True)

    @post_load
    def make_blog(self, data, **kwargs):
        return Post(**data)
