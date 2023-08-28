from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import urllib.parse

# Define the directory to store uploaded files
UPLOAD_DIRECTORY = "uploads"

class FileServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # List the uploaded files
            uploaded_files = os.listdir(UPLOAD_DIRECTORY)
            file_list = ""
            for filename in uploaded_files:
                file_list += f'<li><a href="/download/{filename}">{filename}</a></li>'
            
            response = f"""
            <html>
            <head><title>File Server</title></head>
            <body>
            <h1>Uploaded Files</h1>
            <ul>
            {file_list}
            </ul>
            <form enctype="multipart/form-data" method="post">
            <input type="file" name="file" multiple>
            <input type="submit" value="Upload">
            </form>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        elif self.path.startswith("/download/"):
            file_name = urllib.parse.unquote(os.path.basename(self.path))
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Disposition", f"attachment; filename={file_name}")
                self.send_header("Content-type", "application/octet-stream")
                self.end_headers()

                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")

    def do_POST(self):
        if self.path == "/":
            content_type, _ = cgi.parse_header(self.headers.get("Content-Type"))
            if content_type == "multipart/form-data":
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={"REQUEST_METHOD": "POST"}
                )
                for field in form.list:
                    if field.filename:
                        file_path = os.path.join(UPLOAD_DIRECTORY, os.path.basename(field.filename))
                        with open(file_path, "wb") as f:
                            f.write(field.file.read())
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()

def run_server():
    port = 8080
    server_address = ("", port)
    httpd = HTTPServer(server_address, FileServerHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

run_server()
