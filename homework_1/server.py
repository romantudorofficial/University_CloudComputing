import http.server
import socketserver
import json
import urllib.parse
import xml.etree.ElementTree as ET
import os

# File that stores the persistent data.
BOOKS_FILE = "books.xml"

def init_books_file():
    """Initialize the XML file if it doesn't exist."""
    if not os.path.exists(BOOKS_FILE):
        root = ET.Element("library")
        tree = ET.ElementTree(root)
        tree.write(BOOKS_FILE)

def load_books():
    """Read books from the XML file and return a list of dictionaries."""
    tree = ET.parse(BOOKS_FILE)
    root = tree.getroot()
    books = []
    for book in root.findall("book"):
        book_data = {"id": book.get("id")}
        for child in book:
            book_data[child.tag] = child.text
        books.append(book_data)
    return books

def save_books(books):
    """Write the list of book dictionaries to the XML file."""
    root = ET.Element("library")
    for b in books:
        book_elem = ET.SubElement(root, "book", id=str(b["id"]))
        for key, value in b.items():
            if key == "id":
                continue
            child = ET.SubElement(book_elem, key)
            child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(BOOKS_FILE)

def generate_new_id(books):
    """Generate a new unique ID based on existing books."""
    if not books:
        return 1
    else:
        max_id = max(int(b["id"]) for b in books)
        return max_id + 1

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # GET /books - retrieve all books
        if len(path_parts) == 1 and path_parts[0] == "books":
            books = load_books()
            self._set_headers(200)
            self.wfile.write(json.dumps(books).encode())

        # GET /books/{id} - retrieve a specific book by ID
        elif len(path_parts) == 2 and path_parts[0] == "books":
            book_id = path_parts[1]
            books = load_books()
            book = next((b for b in books if b["id"] == book_id), None)
            if book:
                self._set_headers(200)
                self.wfile.write(json.dumps(book).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Book not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode())
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        # POST /books - create a new book
        if len(path_parts) == 1 and path_parts[0] == "books":
            books = load_books()
            new_id = generate_new_id(books)
            book = {"id": str(new_id)}
            # Expect data to include book details (e.g., title, author)
            for key, value in data.items():
                book[key] = value
            books.append(book)
            save_books(books)
            self._set_headers(201)
            self.wfile.write(json.dumps(book).encode())

        # POST /books/batch - create multiple books
        elif len(path_parts) == 2 and path_parts[0] == "books" and path_parts[1] == "batch":
            if not isinstance(data, list):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Expected a list of books"}).encode())
                return
            books = load_books()
            created_books = []
            for book_data in data:
                new_id = generate_new_id(books)
                book = {"id": str(new_id)}
                for key, value in book_data.items():
                    book[key] = value
                books.append(book)
                created_books.append(book)
            save_books(books)
            self._set_headers(201)
            self.wfile.write(json.dumps(created_books).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_PUT(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")
        content_length = int(self.headers.get("Content-Length", 0))
        put_data = self.rfile.read(content_length)
        try:
            data = json.loads(put_data.decode())
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        # PUT /books/{id} - update a specific book by ID
        if len(path_parts) == 2 and path_parts[0] == "books":
            book_id = path_parts[1]
            books = load_books()
            book = next((b for b in books if b["id"] == book_id), None)
            if book:
                # Update provided fields (ignoring "id" if included)
                for key, value in data.items():
                    if key != "id":
                        book[key] = value
                save_books(books)
                self._set_headers(200)
                self.wfile.write(json.dumps(book).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Book not found"}).encode())

        # PUT /books - bulk update: replace the entire collection
        elif len(path_parts) == 1 and path_parts[0] == "books":
            if not isinstance(data, list):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Expected a list of books"}).encode())
                return
            new_books = []
            for book_data in data:
                if "id" not in book_data:
                    new_id = generate_new_id(new_books)
                    book_data["id"] = str(new_id)
                new_books.append(book_data)
            save_books(new_books)
            self._set_headers(200)
            self.wfile.write(json.dumps(new_books).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # DELETE /books/{id} - delete a specific book by ID
        if len(path_parts) == 2 and path_parts[0] == "books":
            book_id = path_parts[1]
            books = load_books()
            new_books = [b for b in books if b["id"] != book_id]
            if len(new_books) == len(books):
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Book not found"}).encode())
            else:
                save_books(new_books)
                self._set_headers(200)
                self.wfile.write(json.dumps({"message": "Book deleted"}).encode())

        # DELETE /books - delete all books
        elif len(path_parts) == 1 and path_parts[0] == "books":
            save_books([])  # Overwrite XML with an empty collection
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "All books deleted"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8080):
    init_books_file()  # Ensure persistent file is ready
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer interrupted and is shutting down.")
    httpd.server_close()

if __name__ == "__main__":
    run(port=8000)
