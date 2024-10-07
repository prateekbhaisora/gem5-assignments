#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

#define MAX_VAL 100

using namespace std;

void generateRandomInputs(vector<vector<double>> &matrix, int &rows, int &cols) {
    matrix.resize(rows);
    for (auto &row : matrix) {
        row.resize(cols);   
    }
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = ((double)rand()) / RAND_MAX * MAX_VAL;  
        }
    }
}

void multiplyMatrices(const vector<vector<double>> &matrixA, const vector<vector<double>> &matrixB, vector<vector<double>> &matrixC) {
    int row1 = matrixA.size(), col1 = matrixA[0].size();
    int row2 = matrixB.size(), col2 = matrixB[0].size();

    for (int i = 0; i < row1; i++) {
        for (int k = 0; k < col1; k++) {
            for (int j = 0; j < col2; j++) {    
                matrixC[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
}

void printOutput(const vector<vector<double>> &matrix) {
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
    vector<vector<double>> matrixA, matrixB;
    if (col1 != row2) {
        cout << "Invalid Input! Multiplication not possible!" << "\n";
        return -1;
    }
    srand(time(0)); 
    generateRandomInputs(matrixA, row1, col1);
    generateRandomInputs(matrixB, row2, col2);
    vector<vector<double>> matrixC(row1, vector<double>(col2, 0.0));
    multiplyMatrices(matrixA, matrixB, matrixC);
    // printOutput(matrixC);
    return 0;
}