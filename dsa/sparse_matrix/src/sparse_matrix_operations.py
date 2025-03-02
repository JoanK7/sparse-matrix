class SparseMatrix:
    def __init__(self, filename=None, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.data = {}
        if filename:
            self.load_from_file(filename)
            
    def load_from_file(self, filename):
        try:
            file = open(filename, 'r')
            lines = file.readlines()
            file.close()
            
            if not lines:
                raise ValueError(f"Error: The file {filename} is empty.")

            line_index = 0
            while line_index < len(lines):
                line = lines[line_index].strip()
                if not line:
                    line_index += 1
                    continue
                    
                if self._starts_with(line, "rows="):
                    self.rows = self._parse_int(line.split("=")[1])
                    line_index += 1
                elif self._starts_with(line, "cols="):
                    self.cols = self._parse_int(line.split("=")[1])
                    line_index += 1
                else:
                    break
            
            while line_index < len(lines):
                line = lines[line_index].strip()
                line_index += 1
                
                if not line:
                    continue
                    
                if self._starts_with(line, "(") and self._ends_with(line, ")"):
                    content = line[1:-1].strip()
                    parts = self._split_by_comma(content)
                    
                    if len(parts) != 3:
                        raise ValueError(f"Invalid format in file {filename}: {line}")
                    
                    try:
                        row = self._parse_int(parts[0])
                        col = self._parse_int(parts[1])
                        value = self._parse_int(parts[2])
                        self.data[(row, col)] = value
                    except ValueError:
                        raise ValueError(f"Invalid number format in file {filename}: {line}")
                else:
                    raise ValueError(f"Invalid format in file {filename}: {line}")
                    
        except:
            raise ValueError(f"File {filename} not found or cannot be read.")
    
    def _starts_with(self, string, prefix):
        if len(string) < len(prefix):
            return False
        return string[:len(prefix)] == prefix
    
    def _ends_with(self, string, suffix):
        if len(string) < len(suffix):
            return False
        return string[-len(suffix):] == suffix
    
    def _split_by_comma(self, string):
        result = []
        current = ""
        for char in string:
            if char == ',':
                result.append(current.strip())
                current = ""
            else:
                current += char
        result.append(current.strip())
        return result
    
    def _parse_int(self, string):
        string = string.strip()
        if not string:
            raise ValueError("Empty string cannot be converted to integer")
        
        negative = False
        if string[0] == '-':
            negative = True
            string = string[1:]
        
        result = 0
        for char in string:
            if char < '0' or char > '9':
                raise ValueError(f"Invalid character in integer: {char}")
            result = result * 10 + (ord(char) - ord('0'))
        
        return -result if negative else result
            
    def get_element(self, row, col):
        return self.data.get((row, col), 0)
        
    def set_element(self, row, col, value):
        if value == 0:
            if (row, col) in self.data:
                del self.data[(row, col)]
        else:
            self.data[(row, col)] = value
            if row >= self.rows:
                self.rows = row + 1
            if col >= self.cols:
                self.cols = col + 1
    
    def transpose(self):
        """
        Returns a new matrix that is the transpose of this matrix.
        In the transpose, rows become columns and columns become rows.
        """
        result = SparseMatrix(rows=self.cols, cols=self.rows)
        
        for (row, col), value in self.data.items():
            result.data[(col, row)] = value
            
        return result
            
    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Matrix dimensions do not match for addition: ({self.rows}x{self.cols}) and ({other.rows}x{other.cols}).")
            
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        
        for key, val in self.data.items():
            result.data[key] = val
        for key, val in other.data.items():
            if key in result.data:
                result.data[key] += val
                if result.data[key] == 0:
                    del result.data[key]
            else:
                result.data[key] = val
                
        return result
        
    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Matrix dimensions do not match for subtraction: ({self.rows}x{self.cols}) and ({other.rows}x{other.cols}).")
            
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        
        for key, val in self.data.items():
            result.data[key] = val
        
        for key, val in other.data.items():
            if key in result.data:
                result.data[key] -= val
                if result.data[key] == 0:
                    del result.data[key]
            else:
                result.data[key] = -val
                
        return result
        
    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply: First matrix has {self.cols} columns, but second matrix has {other.rows} rows.")
            
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        
        for (r1, c1), v1 in self.data.items():
            for (r2, c2), v2 in other.data.items():
                if c1 == r2:
                    result_key = (r1, c2)
                    current_val = result.data.get(result_key, 0)
                    result.data[result_key] = current_val + (v1 * v2)
                    if result.data[result_key] == 0:
                        del result.data[result_key]
                    
        return result
        
    def display(self):
        print(f"Matrix ({self.rows}x{self.cols}):")
        for r in range(min(20, self.rows)):
            row_values = []
            for c in range(min(20, self.cols)):
                row_values.append(str(self.get_element(r, c)))
            print(' '.join(row_values))
        if self.rows > 20 or self.cols > 20:
            print("... (matrix too large to display fully)")
            
    def save_to_file(self, filename):
        file = open(filename, 'w')
        file.write(f"Matrix ({self.rows}x{self.cols}):\n")
        for r in range(self.rows):
            row_values = []
            for c in range(self.cols):
                row_values.append(str(self.get_element(r, c)))
            file.write(' '.join(row_values) + '\n')
        file.close()
        print(f"Result saved to {filename}")

if __name__ == "__main__":
    base_path = "dsa/sparse_matrix/sample_inputs/"

    print("Enter files for addition and subtraction operations:")
    file1_name = input("Enter the first matrix file name: ")
    file2_name = input("Enter the second matrix file name: ")
    
    file1 = base_path + file1_name
    file2 = base_path + file2_name
    
    while True:
        print("\nChoose an operation: 1) Addition 2) Subtraction 3) Multiplication")
        choice = input("Enter choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    try:
        if choice == '1':
            print(f"Loading {file1}...")
            matrix1 = SparseMatrix(file1)
            print(f"Loading {file2}...")
            matrix2 = SparseMatrix(file2)
            
            print("Performing addition...")
            result = matrix1.add(matrix2)
            output_file = "addition_result.txt"
            
        elif choice == '2':
            print(f"Loading {file1}...")
            matrix1 = SparseMatrix(file1)
            print(f"Loading {file2}...")
            matrix2 = SparseMatrix(file2)
            
            print("Performing subtraction...")
            result = matrix1.subtract(matrix2)
            output_file = "subtraction_result.txt"
            
        elif choice == '3':
            print("For multiplication, you need to select matrices with compatible dimensions.")
            print("Enter files for multiplication operation:")
            
            mult_option = input("Choose multiplication option:\n"
                               "1) First matrix * Third matrix\n"
                               "2) Second matrix * Third matrix\n"
                               "Enter choice (1/2): ").strip()
            
            file3_name = input("Enter the third matrix file name: ")
            file3 = base_path + file3_name
            
            if mult_option == '1':
                print(f"Loading {file1}...")
                matrix_a = SparseMatrix(file1)
                print(f"Loading {file3}...")
                matrix_b = SparseMatrix(file3)
            elif mult_option == '2':
                print(f"Loading {file2}...")
                matrix_a = SparseMatrix(file2)
                print(f"Loading {file3}...")
                matrix_b = SparseMatrix(file3)
            else:
                raise ValueError("Invalid multiplication option choice.")
            
            print(f"Matrix A dimensions: {matrix_a.rows}x{matrix_a.cols}")
            print(f"Matrix B dimensions: {matrix_b.rows}x{matrix_b.cols}")
            
            print("Performing multiplication...")
            result = matrix_a.multiply(matrix_b)
            output_file = "multiplication_result.txt"
        
        print("\nResult (first 20x20 elements):")
        result.display()
        result.save_to_file(output_file)
        print(f"Full result saved to {output_file}")
        
    except ValueError as e:
        print(f"Error: {e}")