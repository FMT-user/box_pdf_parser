# Box PDF Upload Script
This script is designed to upload PDF files to a Box account using the Box API. It utilizes         
# Readme for Box PDF Upload Script      
the `boxsdk` library to interact with the Box API and handle file uploads.
# Requirements
## Prerequisites
- Python 3.x
- Box account with API access
# Installation
## Install Dependencies
```bash
pip install boxsdk
```
# Usage
## Set Up Environment Variables
Set the following environment variables in your system:
- `BOX_CLIENT_ID`: Your Box application client ID.
- `BOX_CLIENT_SECRET`: Your Box application client secret.
- `BOX_ACCESS_TOKEN`: Your Box access token for authentication.
## Run the Script
```bash
python upload_pdf.py <path_to_pdf_file>
```
# Example
```bash
python upload_pdf.py /path/to/your/file.pdf
```
# Notes
- Ensure that the Box application has the necessary permissions to upload files.
- The script will upload the specified PDF file to the root folder of your Box account.
# License
This script is released under the MIT License. See the LICENSE file for more details.
# Author
This script was created by [Durgesh]. Feel free to modify and use it as needed.




