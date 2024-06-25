from bottle import route, run, request, HTTPResponse
import json

DATA_FILE_NAME = "books.json"
BASE_ROUTE = "/books"


def read_books_data() -> dict:
    f = open(DATA_FILE_NAME, "r")
    data = json.load(f)
    f.close()
    return data


def write_books_data(data: list) -> None:
    f = open(DATA_FILE_NAME, "w+")
    f.write(json.dumps(data))
    f.close()
    return None


def is_post_valid(body: dict) -> bool:
    res = False
    if "author" in body and "title" in body:
        res = True
    return res


# ROUTE FOR GENERIC GET API VIEW
@route(BASE_ROUTE, method="GET")
def index():
    books = read_books_data()
    return {"data": books}


# ROUTE FOR GENERIC POST API VIEW (Adding new book)
@route(BASE_ROUTE, method="POST")
def index():
    body = request.json
    if is_post_valid(body):
        books = read_books_data()
        body["id"] = len(books) + 1
        books.append(body)
        write_books_data(books)
        return HTTPResponse(status=201, body={"data": books})
    else:
        return HTTPResponse(
            status=400, body={"error": "missing required keys (title, author)"}
        )


# ROUTE FOR GENERIC DELETE API VIEW (Removing book)
@route(f"{BASE_ROUTE}/<id>", method="DELETE")
def index(id):
    ID = int(id)
    books = read_books_data()
    books_by_ids = [book["id"] for book in books]
    if ID is not None and ID in books_by_ids:
        filtered_data = [row for row in books if row["id"] != ID]
        write_books_data(filtered_data)
        return HTTPResponse(status=200, body={"data": filtered_data})
    else:
        return HTTPResponse(status=404, body={"error": "ID not found"})


# ROUTE FOR DETAIL OBJECT API VIEW
@route(f"{BASE_ROUTE}/<id>", method="GET")
def index(id):
    ID = int(id)
    books = read_books_data()
    books_by_ids = [row["id"] for row in books]
    res = []

    if ID is not None and ID in books_by_ids:
        res = [row for row in books if row["id"] == ID]
        if len(res) == 1:
            return HTTPResponse(status=200, body={"data": res[0]})
        else:
            return HTTPResponse(
                status=400, body={"error": "More than one book with provided ID found."}
            )
    else:
        return HTTPResponse(
            status=404, body={"error": "Book with provided ID not found"}
        )

run(host="localhost", port=8080)
