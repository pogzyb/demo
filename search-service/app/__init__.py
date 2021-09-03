import logging
import os

from flask import Flask, jsonify
from requests import codes

from app.blueprints import videogames
from app.gb_client import GiantBombClient
from config import get_app_config


logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger(__name__).setLevel(logging.DEBUG)


def create_app(env: str) -> Flask:
    """
    Factory function;
    Initializes the application as well as its configurations,
    plugins, routers, and dependencies.

    :return: initialized Flask application
    """
    app = Flask(__name__)
    app.config.from_object(get_app_config(env))
    app.giant_bomb_client = GiantBombClient()
    app.register_blueprint(videogames)
    register_errorhandlers(app)
    return app


def register_errorhandlers(app: Flask) -> None:
    """Error handlers for 404s and 500s"""
    def render_error(err):
        return jsonify(detail=f"{err}"), err.code

    for e in [(codes.internal_server_error), codes.not_found]:
        app.errorhandler(e)(render_error)
