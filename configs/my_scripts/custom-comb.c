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

int computeBinomialExpansion(int n) {
    int result = 0;

    for (int k = 0; k <= n; ++k) {
        int nCr;
        
        asm volatile(
            "comb %[res], %[n_val], %[k_val]\n\t"
            : [res] "=r" (nCr)
            : [n_val] "r" (n), [k_val] "r" (k)
        );

        int A_pow = riscv_pow(A, n - k);
        int X_pow = riscv_pow(X, k);

        int term;
        asm volatile(
            "mul %[term], %[nCr], %[A_pow]\n\t"   
            "mul %[term], %[term], %[X_pow]\n\t"  
            : [term] "=r" (term)
            : [nCr] "r" (nCr), [A_pow] "r" (A_pow), [X_pow] "r" (X_pow)
        );

        result += term;
    }

    return result;
}

int main() {
    int result = computeBinomialExpansion(n);
    printf("(%d + %d)^%d using custom RISC-V instruction = %d\n", A, X, n, result);
    return 0;
}
