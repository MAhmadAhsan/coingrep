class TerminalTable:
    def __init__(self, total_rows, total_columns):
        if total_rows <= 0 or total_columns <= 0:
            raise ValueError("Invalid Argument")
        
        self.total_rows = total_rows
        self.total_columns = total_columns
        self.table = [["" for _ in range(total_columns)] for _ in range(total_rows)]
        self.colors = [["" for _ in range(total_columns)] for _ in range(total_rows)]
        self.max_col_widths = [0 for _ in range(total_columns)]
    
    def _update_max_col_widths(self, data, i, j):
        data = str(data)
        if len(data) > self.max_col_widths[j]:
            self.max_col_widths[j] = len(data)        
    
    def insert(self, data, i , j):
        self._update_max_col_widths(data, i , j)
        str_data = str(data)
        sanitized_data = " ".join(str_data.split())
        self.table[i][j] = sanitized_data
    
    def get(self, i, j):
        return self.table[i][j]
    
    def draw(self):
        total_rows_with_borders = 2 * self.total_rows + 1
        table = [[] for _ in range(total_rows_with_borders)]
        
        for row_no in range(total_rows_with_borders):
            is_border = (row_no % 2 == 0)
            left, mid, right = "", "", ""
            pieces = []
            
            if is_border:
                if row_no == 0:
                    left, mid, right = "┌", "┬", "┐"
                elif row_no == total_rows_with_borders - 1:
                    left, mid, right = "└", "┴", "┘"
                else:
                    left, mid, right = "├", "┼", "┤"
                pieces = ["─" * self.max_col_widths[col_no] for col_no in range(self.total_columns)]
            else:
                left, mid, right = "│", "│", "│"
                
                for col_no in range(self.total_columns):
                    row_no_in_table = row_no // 2
                    data = self.table[row_no_in_table][col_no]
                    padding_size = self.max_col_widths[col_no] - len(data)
                    padded_data = data + " " * padding_size
                    pieces.append(padded_data)
                
            line = left + mid.join(pieces) + right
            print(line)