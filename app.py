from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import BytesIO
import requests

app = FastAPI()


def parse_pdf_from_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes in memory."""
    output_string = BytesIO()
    with BytesIO(pdf_bytes) as pdf_file:
        extract_text_to_fp(
            pdf_file,
            output_string,
            laparams=LAParams(),
            output_type='text',
            codec=None
        )
    return output_string.getvalue().decode('utf-8')


def download_file_from_box_to_memory(file_name: str, access_token: str, folder_id: str) -> bytes:
    """Download a file from Box directly into memory."""
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get file list from folder
    folder_items_url = f"https://api.box.com/2.0/folders/{folder_id}/items"
    response = requests.get(folder_items_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"[Box Folder Error] Status {response.status_code}: {response.text}")

    items = response.json().get("entries", [])
    file_info = next((item for item in items if item["name"] == file_name), None)

    if not file_info:
        raise Exception(f"File '{file_name}' not found in Box folder ID '{folder_id}'.")

    file_id = file_info["id"]

    # Download the file
    download_url = f"https://api.box.com/2.0/files/{file_id}/content"
    file_response = requests.get(download_url, headers=headers)

    if file_response.status_code != 200:
        raise Exception(f"[Box Download Error] Status {file_response.status_code}: {file_response.text}")

    return file_response.content


@app.post("/parse_invoice_pdfs/")
async def parse_invoice_pdfs(request: Request):
    try:
        data = await request.json()
        file_names = data.get("file_names")
        access_token = data.get("access_token")
        folder_id = data.get("folder_id")

        if not access_token or not folder_id or not file_names or not isinstance(file_names, list):
            return JSONResponse(status_code=400, content={
                "error": "Request must include: access_token (str), folder_id (str), file_names (list of file names)."
            })

        results = []

        for file_name in file_names:
            try:
                pdf_bytes = download_file_from_box_to_memory(file_name, access_token, folder_id)
                parsed_text = parse_pdf_from_bytes(pdf_bytes)
                results.append({
                    "file": file_name,
                    "text": parsed_text
                })
            except Exception as e:
                results.append({
                    "file": file_name,
                    "error": str(e)
                })

        return results

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
