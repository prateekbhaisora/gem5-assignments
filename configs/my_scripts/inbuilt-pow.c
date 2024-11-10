#include <stdio.h>

const int A = 10;
const int X = 6;
const int n = 3;

int riscv_pow(int base, int exp) {
    int result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            asm volatile(
                "mul %[res], %[res], %[base]\n\t"  
                : [res] "=r" (result)             
                : "0" (result), [base] "r" (base) 
            );
        }
        asm volatile(
            "mul %[base], %[base], %[base]\n\t"  
            : [base] "=r" (base)                 
            : "0" (base)                         
        );
        exp /= 2;
    }
    return result;
}

int computeDirect(int n) {
    return riscv_pow(A + X, n);  
}

int main() {
    int result = computeDirect(n);
    printf("(%d + %d)^%d using inbuilt RISC-V instruction = %d\n", A, X, n, result);
    return 0;
}
