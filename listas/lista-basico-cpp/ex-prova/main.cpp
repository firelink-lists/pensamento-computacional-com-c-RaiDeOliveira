#include <iostream>
void troca(int v[], int i, int j) {
int tmp = v[i];
v[i] = v[j];
v[j] = tmp;
}

void selection_sort(int v[], int n) {
for (int i = 0; i < n - 1; i++) {
// implementação
}
}


int min_idx = 0;
for (int j = i + 1; j < n; j++)
if (v[j] < v[min_idx])
min_idx = j;
troca(v, i, min_idx);