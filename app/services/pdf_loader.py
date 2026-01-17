import fitz # PyMuPDF

class PDFLoaderService:
    @staticmethod
    async def extract_text(file) -> str:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
