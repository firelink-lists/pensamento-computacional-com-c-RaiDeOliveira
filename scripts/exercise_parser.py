#!/usr/bin/env python3
"""
Exercise Parser - Analisa texto extraído e identifica exercícios
"""

import os
import re
import json
from pathlib import Path

TEMP_DIR = Path("temp")
OUTPUT_DIR = Path("temp")

def clean_text(text):
    """Limpa e normaliza o texto"""
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    # Remove espaços no início/fim das linhas
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)

def identify_exercises(text):
    """Identifica exercícios no texto usando padrões comuns"""
    exercises = []
    
    # Padrões para identificar exercícios
    # Exemplo: "1.", "Exercício 1", "Questão 1", etc.
    patterns = [
        r'(?:^|\n)\s*(\d+)[\.\)\-]\s*',  # 1. ou 1) ou 1-
        r'(?:^|\n)\s*[Ee]xerc[ií]cio\s*(\d+)\s*[:\.\-]?\s*',
        r'(?:^|\n)\s*[Qq]uest[aã]o\s*(\d+)\s*[:\.\-]?\s*',
        r'(?:^|\n)\s*[Pp]roblema\s*(\d+)\s*[:\.\-]?\s*',
    ]
    
    # Encontra todas as posições de início de exercício
    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            matches.append((match.start(), int(match.group(1)), match.end()))
    
    # Ordena por posição
    matches.sort(key=lambda x: x[0])
    
    # Extrai cada exercício
    for i, (start_pos, ex_num, end_pos) in enumerate(matches):
        # Fim deste exercício = início do próximo ou fim do texto
        if i + 1 < len(matches):
            end_pos = matches[i + 1][0]
        else:
            end_pos = len(text)
        
        exercise_text = text[start_pos:end_pos].strip()
        
        # Extrai título/descrição
        lines = exercise_text.split('\n')
        title = lines[0] if lines else f"Exercício {ex_num}"
        description = '\n'.join(lines[1:]) if len(lines) > 1 else ""
        
        # Limpa descrição
        description = clean_text(description)
        
        exercises.append({
            'number': ex_num,
            'title': title,
            'description': description,
            'raw_text': exercise_text
        })
    
    return exercises

def extract_problem_type(description):
    """Tenta identificar o tipo de problema"""
    description_lower = description.lower()
    
    types = []
    
    # Padrões para tipos de problemas
    if any(word in description_lower for word in ['soma', 'subtração', 'multiplicação', 'divisão', 'média', 'área', 'perímetro', 'volume']):
        types.append('matematica')
    
    if any(word in description_lower for word in ['string', 'texto', 'palavra', 'caractere', 'concatenar', 'inverter']):
        types.append('string')
    
    if any(word in description_lower for word in ['vetor', 'array', 'lista', 'matriz', 'matriz', 'elemento']):
        types.append('array')
    
    if any(word in description_lower for word in ['condição', 'se', 'senão', 'if', 'else', 'switch']):
        types.append('condicional')
    
    if any(word in description_lower for word in ['loop', 'laço', 'for', 'while', 'repetir', 'iterar']):
        types.append('repeticao')
    
    if any(word in description_lower for word in ['função', 'procedimento', 'recursivo', 'recursão']):
        types.append('funcao')
    
    if any(word in description_lower for word in ['struct', 'classe', 'objeto', 'registro']):
        types.append('struct')
    
    if any(word in description_lower for word in ['arquivo', 'file', 'ler arquivo', 'escrever arquivo']):
        types.append('arquivo')
    
    if not types:
        types.append('geral')
    
    return types

def parse_lista(lista_name, raw_text):
    """Parseia uma lista completa"""
    print(f"\nAnalisando: {lista_name}")
    
    exercises = identify_exercises(raw_text)
    
    parsed_data = {
        'lista_name': lista_name,
        'total_exercises': len(exercises),
        'exercises': []
    }
    
    for ex in exercises:
        problem_types = extract_problem_type(ex['description'])
        
        parsed_ex = {
            'number': ex['number'],
            'title': ex['title'],
            'description': ex['description'],
            'problem_types': problem_types,
            'has_input': any(word in ex['description'].lower() for word in ['leia', 'entrada', 'input', 'digite']),
            'has_output': any(word in ex['description'].lower() for word in ['imprima', 'escreva', 'saída', 'output', 'mostre']),
        }
        
        parsed_data['exercises'].append(parsed_ex)
        print(f"  Exercício {ex['number']}: {ex['title'][:50]}... (tipos: {', '.join(problem_types)})")
    
    return parsed_data

def main():
    """Função principal"""
    # Encontra todos os arquivos de texto extraídos
    raw_files = sorted(TEMP_DIR.glob("*_raw.txt"))
    
    if not raw_files:
        print(f"Nenhum arquivo de texto encontrado em {TEMP_DIR}/")
        print("Execute primeiro: python3 scripts/pdf_processor.py")
        return
    
    print(f"Encontrados {len(raw_files)} arquivo(s) para analisar")
    
    all_listas = []
    
    for raw_file in raw_files:
        lista_name = raw_file.stem.replace('_raw', '')
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        parsed_data = parse_lista(lista_name, raw_text)
        all_listas.append(parsed_data)
        
        # Salva dados parseados
        output_file = OUTPUT_DIR / f"{lista_name}_parsed.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print(f"  Dados salvos em: {output_file}")
    
    print(f"\n{'='*50}")
    print(f"Parsing concluído: {len(all_listas)} lista(s) analisadas")
    print(f"Total de exercícios encontrados: {sum(l['total_exercises'] for l in all_listas)}")
    print(f"Próximo passo: execute 'python3 scripts/test_generator.py'")

if __name__ == "__main__":
    main()
