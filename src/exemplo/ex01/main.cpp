/**
 * @exercise Exemplo - Exercício 1
 * @title Soma de dois números
 * @description Escreva um programa que leia dois números inteiros e imprima a soma deles.
 * @input stdin
 * @output stdout
 * @timeout 1000
 * @test name="Caso básico" input="5 3" expected="8"
 * @test name="Caso com zero" input="0 5" expected="5"
 * @test name="Caso negativo" input="-3 7" expected="4"
 * @test name="Caso grande" input="1000 2000" expected="3000"
 */

#include <iostream>
using namespace std;

int main() {
    int a, b;
    
    // Leia dois inteiros
    cin >> a >> b;
    
    // Calcule e imprima a soma
    cout << a + b << endl;
    
    return 0;
}
