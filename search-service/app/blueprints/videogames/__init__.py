from flask import Blueprint

videogames = Blueprint('videogames', __name__, url_prefix='/videogames', template_folder='templates/search')

from . import routes # noqa