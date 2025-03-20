import pytesseract
from pdf2image import convert_from_path
import os

# Set Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text_from_scanned_pdf(pdf_path, output_text_file):
    """
    Extracts text from a scanned PDF using OCR (Tesseract)
    and saves it to a text file.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return None
    
    print("🔄 Converting PDF to images...")
    images = convert_from_path(pdf_path)
    extracted_text = ""
    
    for i, img in enumerate(images):
        print(f"🔍 Processing page {i + 1}...")
        text = pytesseract.image_to_string(img, lang='eng')
        extracted_text += text + "\n"
    
    if extracted_text.strip():
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"✅ Text extracted and saved to {output_text_file}")
    else:
        print("❌ No text extracted from PDF.")
    
    return extracted_text

# Example usage
if __name__ == "__main__":
    pdf_path = "data\Hospital_management.pdf"  # Change this to your actual PDF file
    output_text_file = "data\extracted_text.txt"
    extract_text_from_scanned_pdf(pdf_path, output_text_file)
