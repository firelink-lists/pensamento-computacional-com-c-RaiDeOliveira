#!/usr/bin/env python3
"""
Run Tests - Executa testes localmente
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Tuple

TEMP_DIR = Path("temp")
LISTAS_DIR = Path("listas")

def compile_exercise(ex_dir: Path) -> Tuple[bool, str]:
    """Compila um exercício e retorna sucesso/erro"""
    bin_dir = ex_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    
    main_cpp = ex_dir / "main.cpp"
    exercise_bin = bin_dir / "exercise"
    
    if not main_cpp.exists():
        return False, f"Arquivo {main_cpp} não encontrado"
    
    cmd = [
        "g++", "-std=c++17", "-Wall", "-Wextra", "-O2",
        str(main_cpp), "-o", str(exercise_bin)
    ]
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, "Compilação bem-sucedida"
        else:
            return False, f"Erro de compilação:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout na compilação"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def run_test(ex_dir: Path, test: Dict) -> Tuple[bool, str, float]:
    """Executa um teste e retorna sucesso/saída/tempo"""
    exercise_bin = ex_dir / "bin" / "exercise"
    
    if not exercise_bin.exists():
        return False, "Binário não encontrado", 0.0
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [str(exercise_bin)],
            input=test['input'],
            capture_output=True,
            text=True,
            timeout=test.get('timeout', 1)
        )
        
        elapsed = time.time() - start_time
        
        actual_output = result.stdout.strip()
        expected_output = test['expected'].strip()
        
        if actual_output == expected_output:
            return True, actual_output, elapsed
        else:
            return False, actual_output, elapsed
            
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT", test.get('timeout', 1)
    except Exception as e:
        return False, f"ERRO: {str(e)}", 0.0

def run_tests_for_exercise(lista_name: str, exercise: Dict) -> Dict:
    """Executa todos os testes de um exercício"""
    ex_num = exercise['number']
    ex_dir = LISTAS_DIR / lista_name / f"ex{ex_num:02d}"
    
    results = {
        'lista': lista_name,
        'exercise': ex_num,
        'title': exercise.get('title', f'Exercício {ex_num}'),
        'compilation': {'success': False, 'message': ''},
        'tests': [],
        'passed': 0,
        'total': 0
    }
    
    # Compila
    success, message = compile_exercise(ex_dir)
    results['compilation'] = {'success': success, 'message': message}
    
    if not success:
        return results
    
    # Executa testes
    tests = exercise.get('tests', [])
    for test in tests:
        test_result = {
            'name': test['name'],
            'input': test['input'],
            'expected': test['expected']
        }
        
        success, actual, elapsed = run_test(ex_dir, test)
        
        test_result['success'] = success
        test_result['actual'] = actual
        test_result['time'] = elapsed
        
        results['tests'].append(test_result)
        results['total'] += 1
        
        if success:
            results['passed'] += 1
    
    return results

def print_results(results: List[Dict]):
    """Imprime resultados formatados"""
    print("\n" + "="*70)
    print("RESULTADOS DOS TESTES")
    print("="*70)
    
    total_exercises = len(results)
    total_passed = sum(1 for r in results if r['passed'] == r['total'] and r['total'] > 0)
    
    for result in results:
        lista = result['lista']
        ex = result['exercise']
        title = result['title']
        
        # Status de compilação
        if not result['compilation']['success']:
            print(f"\n❌ {lista}/ex{ex:02d}: ERRO DE COMPILAÇÃO")
            print(f"   {result['compilation']['message'][:100]}")
            continue
        
        # Status dos testes
        passed = result['passed']
        total = result['total']
        
        if passed == total:
            status = "✅"
        elif passed > 0:
            status = "⚠️"
        else:
            status = "❌"
        
        print(f"\n{status} {lista}/ex{ex:02d}: {title[:40]}")
        print(f"   Testes: {passed}/{total} passaram")
        
        # Detalhes dos testes que falharam
        for test in result['tests']:
            if not test['success']:
                print(f"   ❌ {test['name']}:")
                print(f"      Input: {test['input'][:50]}")
                print(f"      Esperado: {test['expected'][:50]}")
                print(f"      Obtido: {test['actual'][:50]}")
    
    print("\n" + "="*70)
    print(f"RESUMO: {total_passed}/{total_exercises} exercícios completos")
    print("="*70)

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Executa testes localmente')
    parser.add_argument('--lista', help='Testar apenas lista específica (ex: lista01)')
    args = parser.parse_args()
    
    # Encontra arquivos com testes
    if args.lista:
        test_files = [TEMP_DIR / f"{args.lista}_with_tests.json"]
    else:
        test_files = sorted(TEMP_DIR.glob("*_with_tests.json"))
    
    if not test_files or not test_files[0].exists():
        print("Nenhum teste encontrado. Execute primeiro: make process-pdfs")
        return
    
    all_results = []
    
    for test_file in test_files:
        if not test_file.exists():
            continue
            
        with open(test_file, 'r', encoding='utf-8') as f:
            lista_data = json.load(f)
        
        lista_name = lista_data['lista_name']
        print(f"\nTestando {lista_name}...")
        
        for exercise in lista_data['exercises']:
            result = run_tests_for_exercise(lista_name, exercise)
            all_results.append(result)
    
    print_results(all_results)

if __name__ == "__main__":
    main()
