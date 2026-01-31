import http.server
import socketserver
import os
import urllib.parse
import json

BASE_DIR = os.path.abspath("public")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.lstrip("/")
        full_path = os.path.join(BASE_DIR, path)
        return full_path

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if "id" in query_params:
            item_id = query_params["id"][0]
            base_json_path = os.path.join(BASE_DIR, "base.json")

            try:
                with open(base_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                found_link = None
                for obj in data:
                    if item_id in obj:
                        found_link = obj[item_id]
                        break

                if found_link:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(found_link.encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"ID not found.")

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"Error reading base.json: {e}".encode("utf-8"))

        elif "search" in query_params:
            search_text = query_params["search"][0].lower()
            search_json_path = os.path.join(BASE_DIR, "search-db.json")

            try:
                with open(search_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                results = []
                for obj in data:
                    if search_text in obj.get("id", "").lower() or search_text in obj.get("title", "").lower():
                        results.append(obj)
                    if len(results) >= 10:  # maksymalnie 10 wyników
                        break

                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()

                # Jeśli tylko jeden wynik, zwracamy obiekt, jeśli więcej – listę
                if len(results) == 1:
                    self.wfile.write(json.dumps(results[0], ensure_ascii=False, indent=2).encode("utf-8"))
                else:
                    self.wfile.write(json.dumps(results, ensure_ascii=False, indent=2).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"Error reading search-db.json: {e}".encode("utf-8"))

        else:
            super().do_GET()

PORT = 8000

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Server works on port:{PORT}")
    httpd.serve_forever()
