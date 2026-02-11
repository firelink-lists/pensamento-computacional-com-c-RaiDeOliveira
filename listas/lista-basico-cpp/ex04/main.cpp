/**
 * @exercise Lista Básico C++ - Exercício 4
 * @title Template e Shared Pointer
 * @description Crie uma template de função `trocar` que receba dois parâmetros por referência e troque seus valores. No `main`, crie dois `shared_ptr` para diferentes tipos (ex: `int` e `double`), use a função template para trocar os valores apontados pelos shared_ptr, exiba os valores antes e depois da troca, e mostre a contagem de referências.
 * @input stdin
 * @output stdout
 * @timeout 1000
 * @test name="Troca int" input="5 10" expected="Antes: 5 10\nDepois: 10 5\nRefs: 1 1"
 * @test name="Troca double" input="3.14 2.71" expected="Antes: 3.14 2.71\nDepois: 2.71 3.14\nRefs: 1 1"
 */

#include <iostream>
#include <memory>

using namespace std;

// TODO: Crie o template de função trocar

template<typename T>
void trocar(T& a, T& b) {
    // Implemente a troca
}

int main() {
    // TODO: Crie shared_ptr para int
    
    // TODO: Crie shared_ptr para double
    
    // TODO: Exiba valores antes da troca
    
    // TODO: Troque os valores
    
    // TODO: Exiba valores depois da troca
    
    // TODO: Mostre contagem de referências
    
    return 0;
}
