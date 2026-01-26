import http.server
import socketserver
import os
import urllib.parse
import json

BASE_DIR = os.path.abspath("public")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Usuwamy początkowy "/"
        path = path.lstrip("/")
        # Tworzymy pełną ścieżkę do pliku w BASE_DIR
        full_path = os.path.join(BASE_DIR, path)
        return full_path

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if "id" in query_params:
            item_id = query_params["id"][0]
            base_json_path = os.path.join(BASE_DIR, "base.json")

            print(f"[DEBUG] Otrzymano zapytanie z id='{item_id}'")
            print(f"[DEBUG] Szukam pliku: {base_json_path}")

            try:
                with open(base_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                found_link = None
                for obj in data:
                    if item_id in obj:
                        found_link = obj[item_id]
                        print(f"[DEBUG] Znaleziono link dla id='{item_id}': {found_link}")
                        break

                if found_link:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(found_link.encode("utf-8"))
                    print(f"[DEBUG] Wypisano link jako tekst: {found_link}")
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"ID not found.")
                    print(f"[DEBUG] Nie znaleziono id='{item_id}' w base.json")

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"Error reading base.json: {e}".encode("utf-8"))
                print(f"[ERROR] Problem z odczytem base.json: {e}")
        else:
            # Jeśli nie ma ?id=..., serwujemy pliki z katalogu public
            super().do_GET()

PORT = 8000

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Server works on port:{PORT}")
    httpd.serve_forever()
