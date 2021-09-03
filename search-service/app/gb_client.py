import os
import logging
from urllib.parse import urlencode
# from functools import wraps
from typing import Dict, Any, Union

import requests

logger = logging.getLogger(__name__)


class GiantBombClient:

    def __init__(self,
                 api_key: str = None,
                 base_url: str = None,
                 requests_kwargs: Dict[str, Any] = {}):

        self.key = api_key or os.getenv('GIANTBOMB_API_KEY', None)
        if not self.key:
            logger.error(f'GIANTBOMB_API_KEY was not specified.')
            raise

        self.base_url = base_url or os.getenv('GIANTBOMB_API_SEARCH_URL', None)
        if not self.key:
            logger.error(f'GIANTBOMB_API_SEARCH_URL was not specified.')
            raise

        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': os.getenv('GIANTBOMB_USER_AGENT', 'something-unique')})
        self.requests_kwargs = requests_kwargs

    def search(self, term: str) -> Union[Dict[str, Any], None]:
        # build initial URL string
        url =  self._get_url_string(term)
        # make initial API call
        response = self._make_api_call(url)
        if not response:
            return None
        giantbomb_data = self._aggregate_data(term, response)
        return giantbomb_data

    def _get_url_string(self, term: str, offset: int = 0) -> str:
        base_url = 'https://giantbomb.com/api/search?'
        query_params = {
            'api_key': self.key,
            'format': 'json',
            'query': term,
            'resources': 'game',
            'limit': 100,
            'offset': offset,
            'field_list': 'aliases,name,platforms'}
        return f'{base_url}{urlencode(query_params)}'

    def _make_api_call(self, url: str) -> Union[Dict[str, Any], None]:
        try:
            response = self.session.get(url, **self.requests_kwargs)
            response.raise_for_status()
            logger.debug(f'received response from giantbomb:{url}')
            return response.json()
        except requests.HTTPError:
            logger.exception(f'problem calling the giantbomb api')
            return None

    def _aggregate_data(self, term: str, query_result: Dict[str, Any]):
        # initial outline of expected data
        data = {
            'aliases': [],
            'name': [],
            'number_of_platforms': 0}
        # populate data from query_result
        data = self._process_results(query_result, data)
        # check for more data via "offset"
        while query_result.get('offset') != 0:
            url = self._get_url_string(term, query_result['offset'])
            # make additional API call using the "offset" parameter
            query_result = self._make_api_call(url)
            if not query_result:
                logger.debug(f'hit bad api response: breaking off data aggregations.')
                break  # todo: handle this more elegantly
            else:
                data = self._process_results(query_result, data)
        # return the complete set of data from the API
        return data

    @staticmethod
    def _process_results(current_data, all_data) -> Dict[str, Any]:
        for result in current_data['results']:
            for field in ['aliases', 'name', 'platforms']:
                # extract field and save
                field_data = result.get(field)
                if field_data:
                    if field == 'platforms':
                        # increment the number of platforms
                        all_data['number_of_platforms'] += len(field_data)
                    else:
                        # save names and aliases into the list
                        all_data[field].append(field_data)
        # return updated data store
        return all_data
