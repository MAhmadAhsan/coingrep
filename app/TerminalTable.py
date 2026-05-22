from .logger import get_logger

class TerminalTable:
    def __init__(self, total_rows, total_columns):
        self.logger = get_logger(__name__)

        self.logger.info(
            f"Creating TerminalTable with "
            f"{total_rows} rows and "
            f"{total_columns} columns."
        )

        if total_rows <= 0 or total_columns <= 0:
            self.logger.error(
                "Invalid table dimensions provided."
            )
            raise ValueError("Invalid Argument")

        self.total_rows = total_rows
        self.total_columns = total_columns

        self.table = [
            ["" for _ in range(total_columns)]
            for _ in range(total_rows)
        ]

        self.colors = [
            ["" for _ in range(total_columns)]
            for _ in range(total_rows)
        ]

        self.max_col_widths = [
            0 for _ in range(total_columns)
        ]

        self.logger.info(
            "TerminalTable initialized successfully."
        )

    def _update_max_col_widths(self, data, i, j):
        data = str(data)

        if len(data) > self.max_col_widths[j]:
            old_width = self.max_col_widths[j]

            self.max_col_widths[j] = len(data)

            self.logger.debug(
                f"Updated column {j} width "
                f"from {old_width} "
                f"to {self.max_col_widths[j]}"
            )

    def insert(self, data, i, j):
        self.logger.info(
            f"Inserting data at row={i}, col={j}"
        )

        self._update_max_col_widths(data, i, j)

        str_data = str(data)

        sanitized_data = " ".join(str_data.split())

        self.table[i][j] = sanitized_data

        self.logger.debug(
            f"Inserted value: '{sanitized_data}'"
        )

    def get(self, i, j):
        self.logger.debug(
            f"Fetching data from row={i}, col={j}"
        )

        return self.table[i][j]

    def draw(self):
        self.logger.info(
            "Drawing terminal table..."
        )

        total_rows_with_borders = 2 * self.total_rows + 1

        table = [
            [] for _ in range(total_rows_with_borders)
        ]

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

                pieces = [
                    "─" * self.max_col_widths[col_no]
                    for col_no in range(self.total_columns)
                ]

            else:
                left, mid, right = "│", "│", "│"

                for col_no in range(self.total_columns):

                    row_no_in_table = row_no // 2

                    data = self.table[row_no_in_table][col_no]

                    padding_size = (
                        self.max_col_widths[col_no]
                        - len(data)
                    )

                    padded_data = (
                        data + " " * padding_size
                    )

                    pieces.append(padded_data)

            line = left + mid.join(pieces) + right

            print(line)

        self.logger.info(
            "Table drawn successfully."
        )