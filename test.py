import requests
import json


class TestBooksAPI:
    FILENAME = "books.json"
    BASE_ROUTE = "http://localhost:8080/books"
    DATA_FIELDS = ["id", "title", "author"]
    TEST_BOOK_NAME = "test_name"
    TEST_BOOK_AUTHOR = "test_author"

    BOOKS = []

    def read_file_length(self):
        f = open(self.FILENAME, "r")
        books = json.load(f)
        return len(books)

    def get_all_books(self):
        res = requests.get(self.BASE_ROUTE)
        if res.status_code == 200:
            data = res.json()
            return data["data"]
        else:
            return []

    def extract_test_books_ids(self, books: list) -> list:
        return [
            row["id"]
            for row in books
            if row["title"] == self.TEST_BOOK_NAME
            and row["author"] == self.TEST_BOOK_AUTHOR
        ]

    def test_get_all_books(self):
        file_length = self.read_file_length()
        res = requests.get(self.BASE_ROUTE)

        # Verify status
        assert res.status_code == 200

        # Verify content-type
        assert res.headers["Content-Type"] == "application/json"

        # Verify response structure & data length
        data = res.json()
        assert "data" in data
        books = data["data"]
        assert len(books) == file_length

    def test_get_book_by_id(self):
        res = requests.get(f"{self.BASE_ROUTE}/1")

        # Verify status
        assert res.status_code == 200

        # Verify Content-Type
        assert res.headers["Content-Type"] == "application/json"

        # Verify response structure
        data = res.json()
        assert isinstance(data, dict)

        for key in self.DATA_FIELDS:
            assert key in data["data"]

    def test_add_new_book(self):
        payload = {"title": self.TEST_BOOK_NAME, "author": self.TEST_BOOK_AUTHOR}
        res = requests.post(self.BASE_ROUTE, json=payload)

        assert res.status_code == 201
        assert res.headers["Content-Type"] == "application/json"

        all_books = self.get_all_books()
        test_ids = self.extract_test_books_ids(all_books)

        # Verify if rows with test name & author exist
        assert len(test_ids) > 0

    def test_remove_book(self):
        all_books = self.get_all_books()
        test_id = self.extract_test_books_ids(all_books)

        # Verify if test books exists
        assert len(test_id) > 0

        for ID in test_id:
            res = requests.delete(f"{self.BASE_ROUTE}/{ID}")
            assert res.status_code == 200

        all_books_check = self.get_all_books()
        test_id_check = self.extract_test_books_ids(all_books_check)

        # Verify if all test books has been removed
        assert len(test_id_check) == 0
