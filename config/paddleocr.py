from paddleocr import PaddleOCR


ocr = PaddleOCR(lang="es", use_doc_unwarping=True, use_doc_orientation_classify=True,use_textline_orientation=True)  # Initialize PaddleOCR
