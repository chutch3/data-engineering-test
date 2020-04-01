import io
import os
import typing
import multiprocessing
import argparse

from accounts_line_sanitizer import AccountsLineSanitizer

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_path', help='input file path')
parser.add_argument('-o', '--output_path', help='output file path')
parser.add_argument('-w', '--workers', type=int, help='number of workers', default=2)

def sanitize_file(path: str, start:int, length: int) -> str:
    """
    worker process to clean file
    :param path: where to get the file
    :param start: starting byte
    :param length: number of bytes to sanitize
    :return: sanitized str
    """
    with open(path, 'r') as f:
        result = sanitize_partition(f, start, length)
        return result


def sanitize_partition(stream: io.TextIOWrapper, start: int, length: int) -> str:
    """
    sanitizes the particular partition
    :param stream: file stream
    :param start: starting byte
    :param length: number of bytes to sanitize
    :return: sanitized str adjusted to length
    """
    sanitizer = AccountsLineSanitizer()
    start_byte = start
    end_byte = start
    sanitized = ''
    finish = start + length
    stream.seek(start_byte)
    while True:
        line = stream.readline()
        end_byte += len(line.encode('utf-8'))
        if end_byte >= finish:
            break
        # elif sanitizer.is_first_row:
        #     row = sanitizer.complete_first_row(stream, line)
        #     sanitized += '\t'.join([i for i in row])
        else:
            row = sanitizer.clean_line(stream, line)
            print(row)
            sanitized += '\t'.join([i for i in row])
    return sanitized[:length]

def sanitize_file_wrapper(args: typing.Tuple) -> typing.Callable:
    """
    wrapper function to pass args to file
    :param args: args for sanitize_file
    :return: output of sanitize_file
    """
    return sanitize_file(*args)

def re_encode_file(path: str, encoding: str ='UTF-16LE', temp_path = '/tmp/data_utf8.tsv'):
    """
    horrendous, but because of all the variable byte mismatches, this takes our file and
    essentially re-encodes it in utf-8
    :param path: file to re-encode
    :param encoding: original encoding
    :param temp_path: where to send the temp file
    :return:
    """

    with open(path, 'r', encoding=encoding) as f:
        with open(temp_path, 'w') as f2:
            for line in f.readlines():
                f2.write(line)
    file_size = os.path.getsize(temp_path)
    print(file_size)
    return file_size



if __name__ == '__main__':
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    num_workers = args.workers
    temp_path = '/tmp/data_utf8.tsv'
    file_size = re_encode_file(input_path)
    starts = [start for start in range(0, file_size, file_size//num_workers)]
    lengths = [file_size//num_workers for start in starts[1:]] + [file_size - starts[-1]]
    print(starts, lengths)
    repeated_input_path = [temp_path] * num_workers
    args = zip(repeated_input_path, starts, lengths)
    with multiprocessing.Pool(num_workers) as pool:
        data = pool.map(sanitize_file_wrapper, args)
    for item in data:
        with open(output_path, 'a') as f2:
            f2.write(item)

