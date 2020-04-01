import io
import typing

class AccountsLineSanitizer:
    """
    How we clean stuff, neatly encapsulated
    """
    def __init__(self):
        self.column_count = 5
        self.int_columns = [0, 3]
        self.delimiter = '\t'
        self.reserved = {'\t', '\n', '\r'}


    def clean_line(self, stream: io.TextIOWrapper, line: str) -> typing.List[str]:
        """
        cleans each row based on the constraints
        :param stream: our open file
        :param line: line to clean
        :return: fixed row
        """
        row = line.split(self.delimiter)
        if len(row) < self.column_count:
            self._add_columns(stream, row)
        elif len(row) > self.column_count:
            self._remove_extra_tabs(row)
        self._remove_raw_strings(row)
        return row

    def _remove_raw_strings(self, row: typing.List[str]) -> None:
        """
        delete '/r' string
        :param row: tsv row
        :return: cleaned row
        """
        for idx, col in enumerate(row):
            row[idx] = col.replace('\r', '\\r')

    def _remove_extra_tabs(self, row: typing.List[str]) -> None:
        """
        removing extra tabs
        :param row: row
        :return: cleaned row
        """
        # you know you need int columns in column 0 and 3
        column_check = [self._is_int_column(row[idx]) for idx in self.int_columns]

        # there are unexpected additional columns here. how do you know where a tab starts and ends?
        # may need some name checking or other wild logic here
        if not all(column_check):
            # what do you do here?
            pass
        # you have too many columns, condense the crap out of them
        else:
            values = [row.pop(idx) for idx in range(5, len(row))]
            joined = '\\t'.join(values)
            row.append(joined)


    @staticmethod
    def _clean_bad_newline(row: typing.Sequence[str], next_row: typing.Sequence[str]) -> None:
        """
        cleans an unexpected newline character
        :param row: csv row
        :param next_row: the next csv row
        :return: cleaned csv row
        """
        last_col = row.pop()
        next_row_col = next_row.pop(0)

        cleaned_last_item = last_col.replace('\n', '\\n')+ next_row_col

        row.append(cleaned_last_item)
        row.extend(next_row)


    def _add_columns(self, stream: io.TextIOWrapper, row: typing.Sequence[str]) -> None:
        """
        add columns to a row with unexpected newline
        :param stream: file stream
        :param row: csv row
        :return:
        """
        while True:
            next_column = self._get_next_column(stream)
            stream.seek(stream.tell() - len(next_column) - 1)
            if self._is_int_column(next_column):
                break
            else:
                next_row = stream.readline().split(self.delimiter)
                self._clean_bad_newline(row, next_row)

    @staticmethod
    def _get_next_column(stream: io.TextIOWrapper) -> str:
        """
        get the next column
        :param stream: file stream
        :return: returns the next column
        """
        column = ''
        while True:
            char = stream.read(1)
            if char == '\t':
                break
            else:
                column += char
        return column

    @staticmethod
    def _is_int_column(column_value: str) -> bool:
        """
        is the column an int (an id column or account number)
        :param column_value: the requisite column to ask
        :return: True or False?
        """
        try:
            int(column_value[:1])
        except ValueError:
            return False
        else:
            return True