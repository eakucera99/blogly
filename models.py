"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMAGE = "https://www.freeiconspng.com/img/13470"

class Users(db.Model):
    """Blogly User."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.Text,
                     nullable = False)
    last_name = db.Column(db.Text,
                          nullable = False)
    image_url = db.Column(db.Text,
                          nullable = False,
                          default = DEFAULT_IMAGE)
    posts = db.relationship("Post", 
                            backref="user", 
                            cascade="all, delete-orphan")
    def __repr__(self):
        """INFO ABOUT USER"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
class Post(db.Model):
    """User posts."""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.Text,
                      nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'),
                         nullable = False)
    @property
    def friendly_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class PostTag(db.Model):
    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.Text, 
                     nullable=False, 
                     unique=True)
    posts = db.relationship('Post',
        secondary="posts_tags",
        backref="tags")

def connect_db(app):
    """Connect DB to flask"""
    db.app = app
    db.init_app(app)