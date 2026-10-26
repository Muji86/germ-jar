"""Serves Germ Jar over HTTPS on port 5008. The Pi's germ-jar.service runs this.

Only the files in public/ are served: index.html and germ-jar-ca.crt, the certificate a
computer installs once to trust this server. The keys live in ~/.germ-jar-tls (see README).
Plain http:// requests to the same port are redirected to https://.
"""
import functools
import http.server
import socket
import ssl
from pathlib import Path

PORT = 5008
PUBLIC = Path(__file__).resolve().parent / "public"
TLS = Path.home() / ".germ-jar-tls"
TLS_HANDSHAKE = 0x16   # first byte a browser sends when it starts https


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Always check for a newer index.html, so a deploy shows up on the next reload.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


class Redirect(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host") or f"{self.server.server_address[0]}:{PORT}"
        self.send_response(301)
        self.send_header("Location", f"https://{host}{self.path}")
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_HEAD = do_GET


class Server(http.server.ThreadingHTTPServer):
    def __init__(self, ctx):
        super().__init__(("0.0.0.0", PORT), functools.partial(Handler, directory=str(PUBLIC)))
        self.ctx = ctx

    def finish_request(self, request, client_address):
        # Runs in the request's own thread: peek at the first byte to tell https from plain http.
        request.settimeout(30)
        try:
            first = request.recv(1, socket.MSG_PEEK)
        except OSError:
            return
        if not first:
            return
        if first[0] != TLS_HANDSHAKE:
            Redirect(request, client_address, self)
            return
        try:
            tls = self.ctx.wrap_socket(request, server_side=True)
        except (ssl.SSLError, OSError):
            return   # e.g. a browser that doesn't trust the certificate yet
        try:
            self.RequestHandlerClass(tls, client_address, self)
        finally:
            tls.close()


def main():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(TLS / "server.crt", TLS / "server.key")
    Server(ctx).serve_forever()


if __name__ == "__main__":
    main()
