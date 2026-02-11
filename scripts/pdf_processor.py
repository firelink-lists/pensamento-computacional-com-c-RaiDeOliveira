#!/usr/bin/env python3
"""
PDF Processor - Extrai texto de PDFs usando OCR ou texto selecionável
"""

import os
import sys
import glob
from pathlib import Path

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("Aviso: PyMuPDF não instalado. Usando OCR para todos os PDFs.")

try:
    from pdf2image import convert_from_path
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Aviso: pdf2image/pytesseract não instalados. OCR indisponível.")

PDFS_DIR = Path("pdfs")
TEMP_DIR = Path("temp")

def extract_text_with_pymupdf(pdf_path):
    """Extrai texto usando PyMuPDF (para PDFs com texto selecionável)"""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += f"\n--- PÁGINA {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Erro ao extrair texto de {pdf_path}: {e}")
        return None

def extract_text_with_ocr(pdf_path):
    """Extrai texto usando OCR (para PDFs com imagens)"""
    if not OCR_AVAILABLE:
        print(f"OCR não disponível para {pdf_path}")
        return None
    
    text = ""
    try:
        print(f"Convertendo {pdf_path} para imagens...")
        images = convert_from_path(pdf_path, dpi=300)
        
        for i, image in enumerate(images):
            print(f"  Processando página {i + 1}/{len(images)}...")
            page_text = pytesseract.image_to_string(image, lang='por')
            text += f"\n--- PÁGINA {i + 1} ---\n"
            text += page_text
        
        return text
    except Exception as e:
        print(f"Erro no OCR de {pdf_path}: {e}")
        return None

def process_pdf(pdf_path):
    """Processa um PDF e extrai o texto"""
    pdf_name = Path(pdf_path).stem
    output_file = TEMP_DIR / f"{pdf_name}_raw.txt"
    
    print(f"\nProcessando: {pdf_path}")
    
    # Tenta extrair texto direto primeiro
    text = None
    if PYMUPDF_AVAILABLE:
        text = extract_text_with_pymupdf(pdf_path)
        if text and len(text.strip()) > 100:  # Verifica se extraiu algo significativo
            print(f"  Texto extraído via PyMuPDF ({len(text)} caracteres)")
        else:
            print(f"  Texto insuficiente, tentando OCR...")
            text = None
    
    # Se não conseguiu ou texto muito curto, usa OCR
    if text is None and OCR_AVAILABLE:
        text = extract_text_with_ocr(pdf_path)
        if text:
            print(f"  Texto extraído via OCR ({len(text)} caracteres)")
    
    if text:
        # Salva texto extraído
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  Salvo em: {output_file}")
        return True
    else:
        print(f"  FALHA ao processar {pdf_path}")
        return False

def main():
    """Função principal"""
    # Cria diretório temp se não existir
    TEMP_DIR.mkdir(exist_ok=True)
    
    # Encontra todos os PDFs
    pdf_files = sorted(PDFS_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print(f"Nenhum PDF encontrado em {PDFS_DIR}/")
        print("Coloque seus PDFs na pasta 'pdfs/' e execute novamente.")
        return
    
    print(f"Encontrados {len(pdf_files)} PDF(s) para processar")
    
    success_count = 0
    for pdf_path in pdf_files:
        if process_pdf(pdf_path):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"Processamento concluído: {success_count}/{len(pdf_files)} PDFs processados")
    print(f"Textos extraídos salvos em: {TEMP_DIR}/")
    print(f"Próximo passo: execute 'python3 scripts/exercise_parser.py'")

if __name__ == "__main__":
    main()
