import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_single_metal, update_metal
from views import get_all_orders, get_single_order, create_order, delete_order

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server """
        self._set_headers(200)

        (resource, id) = self.parse_url(self.path)

        response = {}  # Default response

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)

                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": f"That metal is not currently in stock for jewelry."}

            else:
                response = get_all_metals()

        if resource == "orders":
            if id is not None:
                response = get_single_order(id)

                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": f"That order was never placed, or was cancelled."}
            else:
                response = get_all_orders()


        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        "docustring"
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_order = None


        if resource == "orders":

            if "metal_id" in post_body and "size_id" in post_body and "style_id" in post_body:
                self._set_headers(201)
                new_order = create_order(post_body)

            else:
                self._set_headers(400)

                new_order = {
                    "message": f'{"Metal is required"}' if "metal" not in post_body else "" f'{"Size is required"}' if "size" not in post_body else "" f'{"Style is required"}' if "style" not in post_body else ""
                }

                self.wfile.write(json.dumps(new_order).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self.do_PUT()

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        "docustring"
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "orders":
            delete_order(id)

        self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        response = {}

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            self._set_headers(204)
            update_metal(id, post_body)

        if resource == "orders":
            self._set_headers(405)
            response = {"message": "Once placed, production for orders begins immediately and therefore cannot be edited or cancelled. Please contact the company directly for support."}

            self.wfile.write(json.dumps(response).encode())

        self.wfile.write("".encode())

    def parse_url(self, path):
        "docustring"

        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:

            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
