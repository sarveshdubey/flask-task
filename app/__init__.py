from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_restful import Api

db = SQLAlchemy()
admin = Admin()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    Migrate(app, db)
    admin.init_app(app)
    api.init_app(app)
    
    from .views import main_blueprint
    from .api.routes import api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app
