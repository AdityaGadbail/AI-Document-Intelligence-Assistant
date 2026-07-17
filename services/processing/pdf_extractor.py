import fitz
from services.processing.dto.extraction_result import ExtractionResult

class PDFExtractor:

    @classmethod
    def extract_pdf(pdf_path:str)-> ExtractionResult:

        document = fitz.open(pdf_path)

        pages = []

        try:
            for page in document:
                text = page.get_text("text")

                if text.strip():
                    pages.append(text)

            extracted_text =  "\n".join(pages)    
            return ExtractionResult(
                text = extracted_text,
                page_count = len(document),
                word_count = len(extracted_text.split()),
                character_count = len(extracted_text)
                )        


        finally:
            document.close()                    
                            

        
