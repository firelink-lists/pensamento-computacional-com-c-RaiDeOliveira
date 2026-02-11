#!/usr/bin/env python3
"""
Test Generator - Gera casos de teste automaticamente baseado no tipo de problema
"""

import os
import json
import random
from pathlib import Path

TEMP_DIR = Path("temp")
SRC_DIR = Path("src")

def generate_math_tests(problem_types, description):
    """Gera testes para problemas matemáticos"""
    tests = []
    
    # Teste básico - valores pequenos
    tests.append({
        'name': 'Caso básico',
        'input': '5 3',
        'expected': '8',
        'description': 'Valores simples positivos'
    })
    
    # Teste edge - zero
    tests.append({
        'name': 'Caso com zero',
        'input': '0 5',
        'expected': '5',
        'description': 'Testa operação com zero'
    })
    
    # Teste edge - negativos
    tests.append({
        'name': 'Caso negativo',
        'input': '-3 7',
        'expected': '4',
        'description': 'Testa valores negativos'
    })
    
    # Teste stress - valores grandes
    tests.append({
        'name': 'Caso grande',
        'input': '1000 2000',
        'expected': '3000',
        'description': 'Testa valores maiores'
    })
    
    return tests

def generate_string_tests(problem_types, description):
    """Gera testes para problemas com strings"""
    tests = []
    
    # Teste básico
    tests.append({
        'name': 'Caso básico',
        'input': 'hello',
        'expected': 'HELLO',
        'description': 'String simples'
    })
    
    # Teste edge - string vazia
    tests.append({
        'name': 'String vazia',
        'input': '',
        'expected': '',
        'description': 'Testa string vazia'
    })
    
    # Teste edge - espaços
    tests.append({
        'name': 'Com espaços',
        'input': 'hello world',
        'expected': 'HELLO WORLD',
        'description': 'Testa string com espaços'
    })
    
    # Teste stress - string longa
    tests.append({
        'name': 'String longa',
        'input': 'a' * 100,
        'expected': 'A' * 100,
        'description': 'Testa string grande'
    })
    
    return tests

def generate_array_tests(problem_types, description):
    """Gera testes para problemas com arrays/vetores"""
    tests = []
    
    # Teste básico
    tests.append({
        'name': 'Caso básico',
        'input': '5\n1 2 3 4 5',
        'expected': '15',
        'description': 'Array pequeno'
    })
    
    # Teste edge - array vazio ou 1 elemento
    tests.append({
        'name': 'Array mínimo',
        'input': '1\n42',
        'expected': '42',
        'description': 'Array com 1 elemento'
    })
    
    # Teste edge - valores negativos
    tests.append({
        'name': 'Com negativos',
        'input': '3\n-1 -2 -3',
        'expected': '-6',
        'description': 'Array com valores negativos'
    })
    
    # Teste stress - array grande
    tests.append({
        'name': 'Array grande',
        'input': f'100\n{" ".join([str(i) for i in range(1, 101)])}',
        'expected': '5050',
        'description': 'Array com 100 elementos'
    })
    
    return tests

def generate_conditional_tests(problem_types, description):
    """Gera testes para problemas condicionais"""
    tests = []
    
    # Teste caso positivo
    tests.append({
        'name': 'Caso positivo',
        'input': '10',
        'expected': 'positivo',
        'description': 'Valor positivo'
    })
    
    # Teste caso negativo
    tests.append({
        'name': 'Caso negativo',
        'input': '-5',
        'expected': 'negativo',
        'description': 'Valor negativo'
    })
    
    # Teste caso zero/boundary
    tests.append({
        'name': 'Caso zero',
        'input': '0',
        'expected': 'zero',
        'description': 'Valor zero (caso limite)'
    })
    
    return tests

def generate_general_tests(problem_types, description):
    """Gera testes genéricos quando o tipo não é claro"""
    tests = []
    
    # Teste básico
    tests.append({
        'name': 'Caso básico',
        'input': '10',
        'expected': '10',
        'description': 'Entrada simples'
    })
    
    # Teste edge
    tests.append({
        'name': 'Caso edge',
        'input': '0',
        'expected': '0',
        'description': 'Valor limite'
    })
    
    # Teste stress
    tests.append({
        'name': 'Caso grande',
        'input': '999999',
        'expected': '999999',
        'description': 'Valor grande'
    })
    
    return tests

def generate_tests_for_exercise(exercise):
    """Gera testes apropriados baseado no tipo de problema"""
    problem_types = exercise.get('problem_types', ['geral'])
    description = exercise.get('description', '')
    
    # Prioriza o primeiro tipo encontrado
    primary_type = problem_types[0] if problem_types else 'geral'
    
    test_generators = {
        'matematica': generate_math_tests,
        'string': generate_string_tests,
        'array': generate_array_tests,
        'condicional': generate_conditional_tests,
        'geral': generate_general_tests,
    }
    
    generator = test_generators.get(primary_type, generate_general_tests)
    return generator(problem_types, description)

def generate_cpp_code(exercise, tests):
    """Gera o código C++ com Doxygen comments"""
    ex_num = exercise['number']
    title = exercise['title']
    description = exercise['description']
    
    # Limita descrição para o comentário
    desc_short = description[:200] + '...' if len(description) > 200 else description
    
    # Gera comentários @test
    test_comments = []
    for test in tests:
        test_comments.append(f" * @test name=\"{test['name']}\" input=\"{test['input']}\" expected=\"{test['expected']}\"")
    
    test_section = '\n'.join(test_comments)
    
    cpp_template = f"""/**
 * @exercise Lista - Exercício {ex_num}
 * @title {title}
 * @description {desc_short}
 * @input stdin
 * @output stdout
 * @timeout 1000
{test_section}
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

int main() {{
    // TODO: Implemente a solução aqui
    
    // Leia a entrada
    
    // Processa os dados
    
    // Imprima o resultado
    
    return 0;
}}
"""
    
    return cpp_template

def main():
    """Função principal"""
    # Encontra todos os arquivos parseados
    parsed_files = sorted(TEMP_DIR.glob("*_parsed.json"))
    
    if not parsed_files:
        print(f"Nenhum arquivo parseado encontrado em {TEMP_DIR}/")
        print("Execute primeiro: python3 scripts/exercise_parser.py")
        return
    
    print(f"Encontrados {len(parsed_files)} arquivo(s) para gerar testes")
    
    total_exercises = 0
    
    for parsed_file in parsed_files:
        lista_name = parsed_file.stem.replace('_parsed', '')
        
        with open(parsed_file, 'r', encoding='utf-8') as f:
            lista_data = json.load(f)
        
        print(f"\nProcessando {lista_name}:")
        
        # Cria diretório da lista
        lista_dir = SRC_DIR / lista_name
        lista_dir.mkdir(parents=True, exist_ok=True)
        
        for exercise in lista_data['exercises']:
            ex_num = exercise['number']
            ex_dir = lista_dir / f"ex{ex_num:02d}"
            ex_dir.mkdir(parents=True, exist_ok=True)
            
            # Gera testes
            tests = generate_tests_for_exercise(exercise)
            exercise['tests'] = tests
            
            # Gera código C++
            cpp_code = generate_cpp_code(exercise, tests)
            
            # Salva main.cpp
            main_cpp_path = ex_dir / "main.cpp"
            with open(main_cpp_path, 'w', encoding='utf-8') as f:
                f.write(cpp_code)
            
            print(f"  Ex{ex_num:02d}: {len(tests)} testes gerados -> {main_cpp_path}")
            total_exercises += 1
        
        # Atualiza arquivo JSON com testes
        lista_data['exercises'] = [ex for ex in lista_data['exercises']]
        output_file = TEMP_DIR / f"{lista_name}_with_tests.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(lista_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Geração concluída: {total_exercises} exercício(s) criados")
    print(f"Código fonte salvo em: {SRC_DIR}/")
    print(f"Próximo passo: execute 'python3 scripts/autograding_generator.py'")

if __name__ == "__main__":
    main()
