import unittest
import unittest.mock as mock

from app import GiantBombClient


class TestGiantBombClient(unittest.TestCase):
    """
    Simple Test Suite for GiantBombClient methods
    """
    def setUp(self):
        # set up some helper data and the gb client
        self.test_term = 'test'
        self.test_result = {
            'offset': 0,
            'results': [
                {
                    'aliases': 'test-aliases-1',
                    'name': 'some-test-name-1',
                    'platforms': [{'some-platform-1': {}}]
                },
                {
                    'aliases': 'test-aliases-2',
                    'name': 'some-test-name-2',
                    'platforms': [{'some-platform-2': {}}]
                },
            ],
        }
        self.test_result_outline = {
            'aliases': [],
            'name': [],
            'number_of_platforms': 0
        }
        self.test_result_data = {
            'aliases': ['test-aliases-1', 'test-aliases-2'],
            'name': ['some-test-name-1', 'some-test-name-2'],
            'number_of_platforms': 2
        }
        self.gb_base_url = 'https://giantbomb.com/api/search?'
        self.gb_test_key = 'test-key'
        self.gb_client = GiantBombClient(api_key=self.gb_test_key, base_url=self.gb_base_url)

    def test_get_url_string(self):
        # make sure the expected result has the right query param components
        url_string = self.gb_client._get_url_string(self.test_term)
        assert f'api_key={self.gb_test_key}' in url_string, f'{self.gb_test_key} not in {url_string}'
        assert url_string.startswith(self.gb_base_url), f'{url_string} does not start with {self.gb_base_url}'
        assert f'query={self.test_term}' in url_string, f'{self.test_term} not in {url_string}'

    def test_process_results(self):
        expected_num_platforms = 2
        expected_aliases = ['test-aliases-1', 'test-aliases-2']
        expected_name = ['some-test-name-1', 'some-test-name-2']
        self.gb_client._process_results(self.test_result, self.test_result_outline)
        # check that everything was parsed correctly
        assert self.test_result_outline['aliases'] == expected_aliases, f'{self.test_result_outline["aliases"]} != {expected_aliases}'
        assert self.test_result_outline['name'] == expected_name, f'{self.test_result_outline["name"]} != {expected_name}'
        assert self.test_result_outline['number_of_platforms'] == expected_num_platforms, \
            f'{self.test_result_outline["number_of_platforms"]} != {expected_num_platforms}'

    @mock.patch('app.gb_client.GiantBombClient._make_api_call')
    def test_aggregate_data(self, mock_api_call):
        # set offset to 1 so that the while loop is triggered
        self.test_result['offset'] = 1
        mock_api_call.return_value = {}
        result_data = self.gb_client._aggregate_data(self.test_term, self.test_result)
        # assert that the aggregated values match what is expected
        for key, value in result_data.items():
            assert key in self.test_result_data.keys()
            assert value == self.test_result_data.get(key)
        mock_api_call.assert_called_once()

    @mock.patch('requests.Session.get')
    def test_make_api_call(self, mock_get):
        # just make sure that the get request happens
        self.gb_client._make_api_call(self.gb_base_url)
        mock_get.assert_called_once()
        mock_get.assert_called_with(self.gb_base_url)

    @mock.patch('app.gb_client.GiantBombClient._make_api_call')
    @mock.patch('app.gb_client.GiantBombClient._aggregate_data')
    @mock.patch('app.gb_client.GiantBombClient._get_url_string')
    def test_search(self, mock_url, mock_agg, mock_api_call):
        test_url = 'some-giantbomb-api-url'
        # mock return values for these dependencies
        mock_url.return_value = test_url
        mock_api_call.return_value = self.test_result_data
        # call the search method
        self.gb_client.search(self.test_term)
        # assert called with test-term
        mock_url.assert_called_with(self.test_term)
        # assert called with the result of mock_url
        mock_api_call.assert_called_with(test_url)
        mock_api_call.assert_called_once()
        # assert called with the result of mock_api_call
        mock_agg.assert_called_with(self.test_term, self.test_result_data)
        mock_agg.assert_called_once()
