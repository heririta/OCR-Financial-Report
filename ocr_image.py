# Initialize Mistral client with API key
from mistralai import Mistral

api_key = "hg8KTuHmhwVmDFeZWxMurc63KmveBLP0" # Replace with your API key
client = Mistral(api_key=api_key)

import base64
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk
import json
from pathlib import Path

# Verify image exists
image_file = Path("receipt.png")
assert image_file.is_file()

# Encode image as base64 for API
encoded = base64.b64encode(image_file.read_bytes()).decode()
base64_data_url = f"data:image/jpeg;base64,{encoded}"

# Process image with OCR
image_response = client.ocr.process(
    document=ImageURLChunk(image_url=base64_data_url),
    model="mistral-ocr-latest"
)

# Convert response to JSON
response_dict = json.loads(image_response.model_dump_json())
json_string = json.dumps(response_dict, indent=4)
print(json_string)

# Save OCR response to a JSON file
output_json_path = image_file.with_suffix(".ocr.json")
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(response_dict, f, ensure_ascii=False, indent=4)
