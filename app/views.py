from flask import Blueprint, render_template
from .models import *
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return "Welcome to the Flask Blog!"

