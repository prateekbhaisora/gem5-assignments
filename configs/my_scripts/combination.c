#include <stdio.h>

int main() {
    int n = 5;      
    int r = 2;      
    int result;

    asm volatile
    (
        "comb   %[res], %[n_val], %[r_val]\n\t"  
        : [res] "=r" (result)                   
        : [n_val] "r" (n), [r_val] "r" (r)      
    );

    int expected = 10;  

    if (result != expected) {
        printf("\n[[FAILED]]: Expected %d, but got %d\n", expected, result);
        return -1;
    }

    printf("\n[[PASSED]]: Result = %d\n", result);
    return 0;
}
