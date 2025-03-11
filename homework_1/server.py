import http.server
import json
import urllib.parse
import xml.etree.ElementTree as ET
import os



BOOKS_FILE = "books.xml"



def init_books_file ():

    '''
        Initializes the file for storing the books.

        Input:
            - None

        Output:
            - None
    '''
    
    # If the file does not exist, create it.
    if not os.path.exists(BOOKS_FILE):
        root = ET.Element("library")
        tree = ET.ElementTree(root)
        tree.write(BOOKS_FILE)



def load_books ():

    '''
        Reads the books from the XML file and returns a list of dictionaries.

        Input:
            - None

        Output:
            - books: the list of books
    '''

    # Parse the XML file.
    tree = ET.parse(BOOKS_FILE)
    root = tree.getroot()

    # Create a list to store the books.
    books = []

    # Add each book to the list of books.
    for book in root.findall("book"):
        book_data = {"id": book.get("id")}
        for child in book:
            book_data[child.tag] = child.text
        books.append(book_data)

    return books



def save_books (books):

    '''
        Writes the list of book dictionaries to the XML file.

        Input:
            - books (list): the list of books

        Output:
            - None
    '''

    # Create the root element.
    root = ET.Element("library")

    # Add each book to the root element.
    for book in books:

        # Create a new book element.
        book_elem = ET.SubElement(root, "book", id = str(book["id"]))

        # Add each field to the book element.
        for key, value in book.items():
            if key == "id":
                continue
            child = ET.SubElement(book_elem, key)
            child.text = str(value)

    # Write the element to the XML file.
    tree = ET.ElementTree(root)

    # Overwrite the existing file.
    tree.write(BOOKS_FILE)



def generate_new_id (books):

    '''
        Generates a new unique ID based on the existing books.

        Input:
            - books (list): the list of books

        Output:
            - integer: the new unique ID
    '''

    # If there are no books, return 1.
    if not books:
        return 1
    
    # Otherwise, return the maximum ID plus 1.
    else:
        max_id = max(int(b["id"]) for b in books)
        return max_id + 1
    


class RequestHandler (http.server.BaseHTTPRequestHandler):
    
    '''
        Handles the HTTP requests.

        Input:
            - http.server.BaseHTTPRequestHandler: the base class for handling the requests

        Output:
            - None
    '''


    def _set_headers (self, code = 200, content_type = "application/json"):

        '''
            Set up the response headers.

            Input:
                - code (integer): the status code to be sent (default: 200 = "OK")
                - content_type (string): the content type of the response (default: JSON)
            
            Output:
                - None
        '''

        # Send the status code to the client.
        self.send_response(code)

        # Set up the header of the response.
        self.send_header("Content-Type", content_type)

        # Finish setting up the headers.
        self.end_headers()


    def do_GET (self):

        '''
            Handles the GET requests.

            Input:
                - None

            Output:
                - None
        '''

        # Parse the path and split it into parts.
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # GET /books - Retrieve All Books
        if len(path_parts) == 1 and path_parts[0] == "books":

            # Load the books from the XML file.
            books = load_books()

            # Set the status code.
            self._set_headers(200)

            # Send the books to the client as JSON.
            self.wfile.write(json.dumps(books).encode())

        # GET /books/{id} - Retrieve a Book by ID
        elif len(path_parts) == 2 and path_parts[0] == "books":

            # Extract the book ID from the path.
            book_id = path_parts[1]

            # Load the books from the XML file.
            books = load_books()

            # Retrieve the book with the given ID or None if not found.
            book = next((book for book in books if book["id"] == book_id), None)

            # If the book exists, dend the book to the client as JSON.
            if book:
                self._set_headers(200)
                self.wfile.write(json.dumps(book).encode())

            # If the book does not exist, send an error message to the client.
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "\n\tThe book does not exist.\n"}).encode())
        
        # The path is invalid.
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "\n\tThe path is not valid.\n"}).encode())


    def do_POST (self):

        '''
            Handles the POST requests.

            Input:
                - None
            
            Output:
                - None
        '''

        # Parse the path and split it into parts.
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # Get the size of the request body.
        content_length = int(self.headers.get("Content-Length", 0))

        # Read the request body.
        post_data = self.rfile.read(content_length)

        # Parse the JSON data if possible.
        try:
            data = json.loads(post_data.decode())

        # If the JSON data is invalid, send an error message to the client.
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "\n\tThe JSON data is invalid.\n"}).encode())
            return

        # POST /books - Add a Book
        if len(path_parts) == 1 and path_parts[0] == "books":

            # Load the books from the XML file.
            books = load_books()

            # Generate a new ID for the book.
            new_id = generate_new_id(books)

            # Create a new book with the provided data.
            book = {"id": str(new_id)}

            # Add the provided data to the book.
            for key, value in data.items():
                book[key] = value

            # Add the new book to the list of books.
            books.append(book)

            # Save the updated list of books to the XML file.
            save_books(books)

            # Send the new book to the client as JSON.
            self._set_headers(201)
            self.wfile.write(json.dumps(book).encode())

        # POST /books/batch - Add Multiple Books
        elif len(path_parts) == 2 and path_parts[0] == "books" and path_parts[1] == "batch":

            # If the data is not a list, send an error message to the client.
            if not isinstance(data, list):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "\n\tThe content must be a list of books.\n"}).encode())
                return
            
            # Load the books from the XML file.
            books = load_books()

            # Create a new list to store the created books.
            created_books = []

            # Add each book to the list of books.
            for book_data in data:

                # Generate a new ID for the book.
                new_id = generate_new_id(books)

                # Create a new book with the provided data.
                book = {"id": str(new_id)}

                # Add the provided data to the book.
                for key, value in book_data.items():
                    book[key] = value

                # Add the new book to the list of books.
                books.append(book)

                # Add the new book to the list of created books.
                created_books.append(book)
            
            # Save the updated list of books to the XML file.
            save_books(books)

            # Send the list of created books to the client as JSON.
            self._set_headers(201)
            self.wfile.write(json.dumps(created_books).encode())

        # The path is invalid.
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "\n\tThe path is not valid.\n"}).encode())


    def do_PUT (self):

        '''
            Handles the PUT requests.

            Input:
                - None
            
            Output:
                - None
        '''
        
        # Parse the path and split it into parts.
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # Get the size of the request body.
        content_length = int(self.headers.get("Content-Length", 0))

        # Read the request body.
        put_data = self.rfile.read(content_length)

        # Parse the JSON data if possible.
        try:
            data = json.loads(put_data.decode())

        # If the JSON data is invalid, send an error message to the client.
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "\n\tThe JSON data is not valid.\n"}).encode())
            return

        # PUT /books/{id} - Update a Book by ID
        if len(path_parts) == 2 and path_parts[0] == "books":

            # Extract the book ID from the path.
            book_id = path_parts[1]

            # Load the books from the XML file.
            books = load_books()

            # Find the book with the given ID or None if not found.
            book = next((b for b in books if b["id"] == book_id), None)

            # If the book exists, update the provided fields and save the changes.
            if book:

                # Update provided fields (ignoring "id" if included).
                for key, value in data.items():
                    if key != "id":
                        book[key] = value

                # Save the updated list of books to the XML file.
                save_books(books)

                # Send the updated book to the client as JSON.
                self._set_headers(200)
                self.wfile.write(json.dumps(book).encode())

            # If the book does not exist, send an error message to the client.
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "\n\tThe book does not exist.\n"}).encode())

        # PUT /books - Replace Entire Collection
        elif len(path_parts) == 1 and path_parts[0] == "books":

            # If the data is not a list, send an error message to the client.
            if not isinstance(data, list):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "\n\tThe data must be a list of books.\n"}).encode())
                return
            
            # Load the books from the XML file.
            new_books = []

            # Add each book to the list of books.
            for book_data in data:

                # Generate a new ID for the book if not provided.
                if "id" not in book_data:
                    new_id = generate_new_id(new_books)
                    book_data["id"] = str(new_id)

                # Add the new book to the list of books.
                new_books.append(book_data)

            # Save the updated list of books to the XML file.
            save_books(new_books)

            # Send the new list of books to the client as JSON.
            self._set_headers(200)
            self.wfile.write(json.dumps(new_books).encode())

        # The path is invalid.
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "\n\tThe path is not valid.\n"}).encode())


    def do_DELETE (self):

        '''
            Handles the DELETE requests.

            Input:
                - None
            
            Output:
                - None
        '''

        # Parse the path and split it into parts.
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # DELETE /books/{id} - Delete a Book by ID
        if len(path_parts) == 2 and path_parts[0] == "books":

            # Extract the book ID from the path.
            book_id = path_parts[1]

            # Load the books from the XML file.
            books = load_books()

            # Remove the book with the given ID if it exists.
            new_books = [b for b in books if b["id"] != book_id]

            # If the book was not found, send an error message to the client.
            if len(new_books) == len(books):
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "\n\tThe book does not exist.\n"}).encode())

            # If the book was found, save the updated list of books.
            else:

                # Save the updated list of books to the XML file.
                save_books(new_books)

                # Send a success message to the client.
                self._set_headers(200)
                self.wfile.write(json.dumps({"message": "\n\tThe book was deleted successfully.\n"}).encode())

        # DELETE /books - Delete All Books
        elif len(path_parts) == 1 and path_parts[0] == "books":

            # Save an empty list of books to the XML file.
            save_books([])

            # Send a success message to the client.
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "\n\tAll books have been deleted.\n"}).encode())

        # The path is invalid.
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "\n\tThe path is not valid.\n"}).encode())



def run (server_class = http.server.HTTPServer, handler_class = RequestHandler, port = 8000):

    '''
        Runs the server.

        Input:
            - server_class (class): the HTTP server class to be used
            - handler_class (class): the request handler class to be used
            - port (integer): the port number to listen on
        
        Output:
            - None
    '''
    
    # Initialize the file for storing the books.
    init_books_file()

    # Set up the server address.
    server_address = ("", port)

    # Create an instance of the server.
    httpd = server_class(server_address, handler_class)

    # Start the server.
    print(f"\n\tThe server has started running on the port {port}.\n")

    # Handle the incoming requests until interrupted.
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\tThe server has been interrupted.\n")

    # Close the server.
    httpd.server_close()



# Run the application.

if __name__ == "__main__":

    run()