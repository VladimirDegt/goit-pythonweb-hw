import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging
import json
from typing import Dict
from datetime import datetime
from jinja2 import Template

logging.basicConfig(level=logging.INFO)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        pr_url = urllib.parse.urlparse(self.path)
        logging.info(f'Received GET request: {self.path}')
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        elif pr_url.path == '/read':
            self.show_messages()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self) -> None:
        data = self.rfile.read(int(self.headers['Content-Length']))
        logging.info(f'Received POST data: {data}')
        data_parse = urllib.parse.unquote_plus(data.decode())
        logging.info(f'Parsed POST data: {data_parse}')
        data_dict: Dict[str, str] = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        logging.info(f'Parsed data as dict: {data_dict}')

        self.store_data(data_dict)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self) -> None:
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def store_data(self, data: Dict[str, str]) -> None:
        timestamp = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        data_to_save = {timestamp: data}

        storage_dir = pathlib.Path('storage')
        storage_dir.mkdir(parents=True, exist_ok=True)

        file_path = storage_dir / 'data.json'

        try:
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        existing_data.update(data_to_save)

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def show_messages(self) -> None:
        storage_dir = pathlib.Path('storage')
        file_path = storage_dir / 'data.json'

        try:
            with open(file_path, 'r') as f:
                messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = {}

        with open('read.html', 'r') as f:
            template = Template(f.read())

        rendered_html = template.render(messages=messages)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(rendered_html.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=HttpHandler) -> None:
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        logging.info('Server starting...')
        http.serve_forever()
    except KeyboardInterrupt:
        logging.info('Server stopped by user.')
        http.server_close()


if __name__ == '__main__':
    run()
