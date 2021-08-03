import responses

from .test_dumydata import google_call
from .tests_setup import TestSetUp
from stx_pn.utility import ApiRequest


class TestApiCalls(TestSetUp):
    @responses.activate
    def test_grab_data_from_google(self):
        responses.add(
            responses.GET,
            "https://www.googleapis.com/books/v1/volumes?q=war&startIndex=0&maxResults=40",
            json=google_call,
            status=200,
        )

        api_data = ApiRequest("war").get_data()

        self.assertEqual(len(api_data), len(google_call["items"]))
