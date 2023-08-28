from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import urllib.parse
import uuid
import random
import string

UPLOAD_DIRECTORY = "uploads"
LINK_LENGTH = 6

def generate_random_link(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class FileServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            response = """
            <html>
            <head><title>File Server</title></head>
            <body>
            <h1>Upload Files</h1>
            <form enctype="multipart/form-data" method="post">
            <input type="file" name="file" multiple>
            <input type="submit" value="Upload">
            </form>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        else:
            # Serve the generated HTML pages for uploaded files
            page_path = os.path.join(UPLOAD_DIRECTORY, self.path[1:])
            if os.path.exists(page_path):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                with open(page_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Page not found")

    def do_POST(self):
        if self.path == "/":
            content_type, _ = cgi.parse_header(self.headers.get("Content-Type"))
            if content_type == "multipart/form-data":
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={"REQUEST_METHOD": "POST"}
                )
                uploaded_files = []
                for field in form.list:
                    if field.filename:
                        unique_filename = str(uuid.uuid4()) + "_" + os.path.basename(field.filename)
                        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
                        with open(file_path, "wb") as f:
                            f.write(field.file.read())
                        
                        link = generate_random_link(LINK_LENGTH)
                        uploaded_files.append((unique_filename, link))
                
                if uploaded_files:
                    # Generate and write the HTML page for the uploaded files
                    page_content = self.generate_files_page(uploaded_files)
                    page_link = generate_random_link(LINK_LENGTH)
                    page_path = os.path.join(UPLOAD_DIRECTORY, page_link + ".html")
                    with open(page_path, "w") as page_file:
                        page_file.write(page_content)
                    
                    # Redirect the user to the generated page
                    self.send_response(302)
                    self.send_header("Location", f"/{page_link}.html")
                    self.end_headers()

    def generate_files_page(self, uploaded_files):
        page_content = f"""
        <html>
        <head><title>Uploaded Files</title></head>
        <body>
        <h1>Uploaded Files</h1>
        <ul>
        """
        for filename, _ in uploaded_files:
            page_content += f"<li><a href=/file/{filename}>{filename}</a></li>"
        page_content += """
        </ul>
        </body>
        </html>
        """
        return page_content

def run_server():
    port = 8080
    server_address = ("", port)
    httpd = HTTPServer(server_address, FileServerHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

run_server()
