import http.server
import socketserver
import os

# Ustal folder bazowy, z którego będą serwowane pliki
BASE_DIR = os.path.abspath("public")  # np. folder "public" w tym samym katalogu

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Usuwamy początkowy "/"
        path = path.lstrip("/")
        # Tworzymy pełną ścieżkę do pliku w BASE_DIR
        full_path = os.path.join(BASE_DIR, path)
        return full_path

PORT = 8000

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Server works on port:{PORT}")
    httpd.serve_forever()
