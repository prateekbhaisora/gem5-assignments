#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

#define MAX_VAL 100
#define BSize 32

using namespace std;

void generateRandomInputs(vector<vector<int>> &matrix, int &rows, int &cols) {
    matrix.resize(rows);
    for (auto &row : matrix) {
        row.resize(cols);   
    }
    for (int i=0; i<rows; i++) {
        for (int j=0; j<cols; j++) {
            matrix[i][j] = rand() % MAX_VAL;
        }
    }
}

void blockMultiply(const vector<vector<int>> &A, const vector<vector<int>> &B, vector<vector<int>> &C, int ii, int jj, int kk) {
    for (int i = ii; i < min(ii + BSize, (int)A.size()); i++) {
        for (int j = jj; j < min(jj + BSize, (int)B[0].size()); j++) {
            for (int k = kk; k < min(kk + BSize, (int)A[0].size()); k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void multiplyMatrices(const vector<vector<int>> &matrixA, const vector<vector<int>> &matrixB, vector<vector<int>> &matrixC) {
    int n = matrixA.size();
    for (int ii = 0; ii < n; ii += BSize) {
        for (int jj = 0; jj < n; jj += BSize) {
            for (int kk = 0; kk < n; kk += BSize) {
                blockMultiply(matrixA, matrixB, matrixC, ii, jj, kk);
            }
        }
    }
}

void printOutput(const vector<vector<int>> &matrix) {
    int row1 = matrix.size(), col2 = matrix[0].size();
    for (int i = 0; i < row1; i++) {
        for (int j = 0; j < col2; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << "\n";
    }
}

int main() {
    int row1 = 64, col1 = 64, row2 = 64, col2 = 64;
    vector<vector<int>> matrixA, matrixB;
    if (col1 != row2) {
        cout << "Invalid Input! Multiplication not possible!" << "\n";
        return -1;
    } 
    srand(time(0));
    generateRandomInputs(matrixA, row1, col1);
    generateRandomInputs(matrixB, row2, col2);
    vector<vector<int>> matrixC(row1, vector<int>(col2));
    multiplyMatrices(matrixA, matrixB, matrixC);
    // printOutput(matrixC);
    return 0;
}                              