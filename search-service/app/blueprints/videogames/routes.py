import logging

from flask import current_app, request
from requests import codes

from . import videogames
from .schemas import videogame_schema


logger = logging.getLogger(__name__)


@videogames.route("/search", methods=['GET'])
def search_giant_bomb():
    """The "search" endpoint will query the GiantBomb API for the given term."""

    # validate term
    term = request.args.get('term', None)
    if not term:
        return {'detail': '?term=<something> must be specified as a query parameter.'}, \
               codes.not_acceptable

    # query the given term via the client
    result = current_app.giant_bomb_client.search(term)
    if not result:
        # something went wrong when communicating with giantbomb.com
        return {'detail': 'Query failed. Try again.'}, codes.failed_dependency
    else:
        # return successful query response
        return videogame_schema.dump(result), codes.ok
