from pdfminer.high_level import extract_text

def pdf_to_text(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"PDF 변환 실패: {e}")
        return ""
