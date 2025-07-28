import easyocr

reader = easyocr.Reader(['en'])  # English OCR

def ocr_image(image_path):
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)
