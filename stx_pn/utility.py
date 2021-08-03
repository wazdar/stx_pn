import requests
from django.utils.crypto import get_random_string


def generate_secret_key(env_file_name: str) -> None:
    """
    Create secret_key and write to .env file.
    :param env_file_name: String/path to env file.
    :return:
    """
    with open(env_file_name, "w+") as env_file:
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        generated_secret_key = get_random_string(50, chars)
        env_file.write(f"SECRET_KEY = '{generated_secret_key}'\n")


def generate_debug_mode(env_file_name: str, debug_mode: bool = False) -> None:
    """
    Add to .env file debug mode settings.
    :param env_file_name: env_file_name: String/path to env file.
    :param debug_mode: Enable/Disable
    :return:
    """
    with open(env_file_name, "a") as env_file:
        env_file.write(f"DEBUG = {debug_mode}\n")


class ApiRequest:
    __API_URL = "https://www.googleapis.com/books/v1/volumes?q="

    def __init__(self, q: str):
        self.query_url = self.__init_query(q)

    def __init_query(self, query: str):
        return self.__API_URL + query

    def __make_request(self, max_results: int = 40, start_index: int = 0) -> dict:
        """
        Do request and return JSON.
        :param max_results:
        :param start_index:
        :return:
        """
        try:
            request = requests.get(
                f"{self.query_url}&startIndex={start_index}&maxResults={max_results}"
            )
            return request.json()
        except requests.exceptions.RequestException as e:
            print(e)

        return {}

    def __get_necessary_data(self, raw_data: list, data_set: list) -> None:
        """
        Collects the necessary data and adds it to the list.
        :param raw_data:
        :param data_set:
        :return:
        """
        for book in raw_data:
            try:
                data_set.append(
                    {
                        "title": book["volumeInfo"]["title"],
                        "authors": book["volumeInfo"]["authors"]
                        if "authors" in book["volumeInfo"]
                        else None,
                        "publication_date": book["volumeInfo"]["publishedDate"]
                        if "publishedDate" in book["volumeInfo"]
                        else None,
                        "categories": book["volumeInfo"]["categories"]
                        if "categories" in book["volumeInfo"]
                        else None,
                        "average_rating": book["volumeInfo"]["averageRating"]
                        if "averageRating" in book["volumeInfo"]
                        else 0,
                        "ratings_count": book["volumeInfo"]["ratingsCount"]
                        if "ratingsCount" in book["volumeInfo"]
                        else 0,
                        "thumbnail": book["volumeInfo"]["imageLinks"]["smallThumbnail"]
                        if "imageLinks" in book["volumeInfo"]
                        and "smallThumbnail" in book["volumeInfo"]["imageLinks"]
                        else None,
                    }
                )
            except Exception as e:
                print(f"Error: {e} in {book}")

    def get_data(self):
        """
        Return list of books from Google API.
        :return:
        """
        data = []
        raw_data = self.__make_request()
        total_items = raw_data.get("totalItems", None)

        self.__get_necessary_data(raw_data=raw_data["items"], data_set=data)

        if 0 < total_items > 40:
            current_index = 40

            while current_index < total_items:
                try:
                    raw_data = self.__make_request(start_index=current_index)
                    if "items" in raw_data:
                        self.__get_necessary_data(
                            raw_data=raw_data["items"], data_set=data
                        )
                except Exception as e:
                    print(f"Error - {e}")

                current_index += 40

        return data
