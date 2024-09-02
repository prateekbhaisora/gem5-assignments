#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

#define MAX_VAL 100

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

void multiplyMatrices(const vector<vector<int>> &matrixA, const vector<vector<int>> &matrixB, vector<vector<int>> &matrixC) {
    int row1 = matrixA.size(), col1 = matrixA[0].size();
    int row2 = matrixB.size(), col2 = matrixB[0].size();
    for (int i = 0; i < row1; i++) {
        for (int j = 0; j < col2; j++) {
            matrixC[i][j] = 0;
            for (int k = 0; k < col1; k++) {
                matrixC[i][j] += matrixA[i][k] * matrixB[k][j];
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
    int row1 = 64, col1 = 32, row2 = 32, col2 = 16;
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
}                                      // TC = O(n^3) SC = O(n^2)