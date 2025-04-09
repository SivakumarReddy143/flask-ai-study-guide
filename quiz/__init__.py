from flask import Blueprint

quiz_bp = Blueprint('quiz', __name__)

from . import chat_utils, html_generator, template