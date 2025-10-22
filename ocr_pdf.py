# Initialize Mistral client with API key
from mistralai import Mistral

api_key = "hg8KTuHmhwVmDFeZWxMurc63KmveBLP0" # Replace with your API key
client = Mistral(api_key=api_key)

# Import required libraries
from pathlib import Path
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk
import json

# Verify PDF file exists
pdf_file = Path("08 Agustus 2025 - Format New SE OJK.pdf")
assert pdf_file.is_file()

# Upload PDF file to Mistral's OCR service
uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

# Get URL for the uploaded file
signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

# Process PDF with OCR, including embedded images
pdf_response = client.ocr.process(
    document=DocumentURLChunk(document_url=signed_url.url),
    model="mistral-ocr-latest",
    include_image_base64=True
)


pdf_ocr_markdown = [page.markdown for page in pdf_response.pages]

# Get structured response from model
chat_response = client.chat.complete(
    model="ministral-8b-latest",
    messages=[
        {
            "role": "user",
            "content": [
                TextChunk(
                    text=(
                        f"Ini adalah OCR gambar dalam markdown:\n\n{pdf_ocr_markdown}\n.\n"
                        "Ubah ini menjadi respons JSON terstruktur yang masuk akal dan dalam bahasa indonesia"
                        "Dari nama bank , jenis laporan dan periode laporan "
                        "Outputnya harus benar-benar JSON tanpa komentar tambahan."
                    )
                ),
            ],
        }
    ],
    response_format={"type": "json_object"},
    temperature=0,
)

# Parse and return JSON response
response_dict = json.loads(chat_response.choices[0].message.content)
print(json.dumps(response_dict, indent=4))

# Save OCR response to a JSON file
output_json_path = pdf_file.with_suffix(".ocr.json")
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(response_dict, f, ensure_ascii=False, indent=4)
