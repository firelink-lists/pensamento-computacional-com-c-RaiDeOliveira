#!/usr/bin/env python3
"""
Autograding Generator - Gera configuração do GitHub Classroom
"""

import os
import json
from pathlib import Path

TEMP_DIR = Path("temp")
GITHUB_DIR = Path(".github/classroom")

def generate_autograding_config():
    """Gera configuração do autograding.json"""
    
    # Encontra todos os arquivos com testes
    test_files = sorted(TEMP_DIR.glob("*_with_tests.json"))
    
    if not test_files:
        print("Nenhum arquivo com testes encontrado")
        return None
    
    autograding_tests = []
    
    for test_file in test_files:
        with open(test_file, 'r', encoding='utf-8') as f:
            lista_data = json.load(f)
        
        lista_name = lista_data['lista_name']
        
        for exercise in lista_data['exercises']:
            ex_num = exercise['number']
            ex_dir = f"src/{lista_name}/ex{ex_num:02d}"
            
            for test in exercise.get('tests', []):
                test_config = {
                    'name': f"{lista_name} - Ex{ex_num:02d} - {test['name']}",
                    'setup': f"cd {ex_dir} && g++ -std=c++17 -Wall -O2 main.cpp -o exercise",
                    'run': f"cd {ex_dir} && echo '{test['input']}' | ./exercise",
                    'input': test['input'],
                    'output': test['expected'],
                    'comparison': 'exact',
                    'timeout': 1
                }
                
                autograding_tests.append(test_config)
    
    autograding_config = {
        'tests': autograding_tests,
        'metadata': {
            'generated_by': 'template-cpp-autograding-generator',
            'total_tests': len(autograding_tests)
        }
    }
    
    return autograding_config

def main():
    """Função principal"""
    # Cria diretório .github/classroom se não existir
    GITHUB_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Gerando configuração do GitHub Classroom...")
    
    config = generate_autograding_config()
    
    if config:
        output_file = GITHUB_DIR / "autograding.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*50}")
        print(f"Configuração gerada com sucesso!")
        print(f"Arquivo: {output_file}")
        print(f"Total de testes: {config['metadata']['total_tests']}")
        print(f"\nO GitHub Classroom está configurado para correção automática!")
    else:
        print("Falha ao gerar configuração")

if __name__ == "__main__":
    main()
