import os

class SparseMatrix:
    def __init__(self, file_path):
        self.rows = 4035
        self.cols = 3018
        self.data = {}
        self.load_from_file(file_path)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('rows='):
                    self.rows = int(line.split('=')[1])
                elif line.startswith('cols='):
                    self.cols = int(line.split('=')[1])
                elif line.startswith('('):
                    row, col, val = map(int, line.strip('()\n').split(','))
                    self.data[(row, col)] = val

    def add(self, other):
        result = SparseMatrix.__new__(SparseMatrix)
        result.rows, result.cols = self.rows, self.cols
        result.data = self.data.copy()
        for key, val in other.data.items():
            result.data[key] = result.data.get(key, 0) + val
        return result

    def subtract(self, other):
        result = SparseMatrix.__new__(SparseMatrix)
        result.rows, result.cols = self.rows, self.cols
        result.data = self.data.copy()
        for key, val in other.data.items():
            result.data[key] = result.data.get(key, 0) - val
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not allow multiplication")
        result = SparseMatrix.__new__(SparseMatrix)
        result.rows, result.cols = self.rows, other.cols
        result.data = {}
        for (r1, c1), v1 in self.data.items():
            for (r2, c2), v2 in other.data.items():
                if c1 == r2:
                    result.data[(r1, c2)] = result.data.get((r1, c2), 0) + v1 * v2
        return result

    def display(self):
        print(f"Matrix ({self.rows}x{self.cols}):")
        for r in range(self.rows):
            row_values = []
            for c in range(self.cols):
                row_values.append(str(self.data.get((r, c), 0)))
            print(' '.join(row_values))

if __name__ == "__main__":
    matrix1 = SparseMatrix('C:/Users/krzjo/OneDrive/Documents/sparse-matrix/dsa/sparse_matrix/sample_inputs/easy_sample_03_1.txt')
    matrix2 = SparseMatrix('C:/Users/krzjo/OneDrive/Documents/sparse-matrix/dsa/sparse_matrix/sample_inputs/easy_sample_03_2.txt')


    print("Addition:")
    matrix1.add(matrix2).display()

    print("\nSubtraction:")
    matrix1.subtract(matrix2).display()

    print("\nMultiplication:")
    matrix1.multiply(matrix2).display()
