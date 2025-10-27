from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io
import tempfile

app = FastAPI(title="OCR API", description="API OCR qui extrait le texte d'une image ou d'un PDF")

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    print("Fichier reçu :", file.filename)

    try:
        filename = file.filename.lower()
        content = await file.read()
        text_result = ""

        if filename.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(content)
                tmp_pdf.flush()
                images = convert_from_bytes(content)
                for img in images:
                    text_result += pytesseract.image_to_string(img, lang="fra+eng") + "\n"
        else:
            image = Image.open(io.BytesIO(content))
            text_result = pytesseract.image_to_string(image, lang="fra+eng")

        return JSONResponse(content={"filename": filename, "text": text_result.strip()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
#update ocr for test