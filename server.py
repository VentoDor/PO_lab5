import http.server
import socketserver

PORT = 8080

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Обработка GET-запросов
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/page2.html':
            self.path = '/page2.html'
        else:
            self.send_error(404, "File Not Found")
            return

        # Отправка файла
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()