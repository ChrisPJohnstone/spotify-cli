from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

from .split_uri import split_uri


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        query = urlparse(self.path).query
        form = dict(parse_qsl(query))
        self.server._auth_code: str = form.get("code")  # type: ignore
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self._write("Return to your terminal")

    def _write(self, text: str) -> int:
        return self.wfile.write(text.encode("UTF-8"))


class AuthServer(HTTPServer):
    def __init__(self, uri: str) -> None:
        uri_parts: tuple[str, str, int] = split_uri(uri)
        super().__init__((uri_parts[1], uri_parts[2]), RequestHandler)
        self.allow_reuse_address: bool = True
        self._auth_code: str = ""

    @property
    def auth_code(self) -> str:
        return self._auth_code
