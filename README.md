# File Server with Upload and Download Functionality

This is a simple Python script that creates a basic file server using the built-in `http.server` module. The script allows users to upload files, which are then made available for download. Uploaded files are stored in a designated directory, and HTML pages are generated to list and provide download links for these files.

## How to Use

1. Make sure you have Python installed on your system.

2. Copy and save the script to a file named `file_server.py`.

3. Open your terminal or command prompt and navigate to the directory containing the `file_server.py` script.

4. Run the script by executing the following command:

python file_server.py


5. Once the server is running, open a web browser and navigate to `http://localhost:8080/` to access the file upload page.

6. On the upload page, you can select and upload files. After the upload is complete, you'll be redirected to a page listing the uploaded files with download links.

7. Click on the file names to download the uploaded files.

## Features

- **Upload Files:** You can upload multiple files using the file input form on the main page.

- **Download Files:** The uploaded files are available for download through generated HTML pages.

- **Randomized Links:** Each uploaded file has a randomly generated link associated with it, making it difficult to predict the URLs.

- **Generated Pages:** An HTML page is generated for each batch of uploaded files, containing links to the uploaded files for easy download.

## Notes

- The script uses the `http.server` module to handle incoming HTTP requests and responses.

- Uploaded files are stored in the "uploads" directory. If the directory doesn't exist, it will be created automatically.

- To keep track of uploaded files, each file is assigned a unique filename, which includes a UUID and the original filename.

- The links to uploaded files are generated randomly using a combination of letters and digits.

- The script provides basic error handling for cases where files or pages are not found.

- The server runs on port 8080 by default. You can change the port by modifying the `port` variable in the script.

- Remember that this script is meant for educational and basic file-sharing purposes. For production use or more advanced features, consider using a more robust web framework.

## Disclaimer

This script is provided as-is with no warranties or guarantees. Use it responsibly and ensure that it aligns with your intended use case and security requirements.
