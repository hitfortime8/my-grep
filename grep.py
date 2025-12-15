import sys
import os
import argparse
import glob



parser = argparse.ArgumentParser(description='Утилита для поиска определенных слов в файле', usage='program -> flag(s) -> word -> file path')
parser.add_argument('-i', action='store_true', help='Поиск без учета регистра')
parser.add_argument('-n', action='store_true', help='Отображение номера строки, в которой найдено слово')
parser.add_argument('-v', action='store_true', help='Инвертированный поиск')
parser.add_argument('-c', action='store_true', help='Подсчитывает количество строк, в которых найдено совпадение')
parser.add_argument('-r', action='store_true', help='Поиск рекурсивно в директории')
parser.add_argument('-l', action='store_true', help='Вывести только имена файлов, в которых есть совпадение')
parser.add_argument('word', help='Слово, принимаемое для поиска')
parser.add_argument('path', help='Путь до файла, где искать слово')

args = parser.parse_args()

def get_file_list(path, recursive=False):
    files = []

    if not os.path.exists(path):
        files.append(path)
        return files

    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        if recursive:
            pattern = os.path.join(path, '**', '*')
            for file in glob.glob(pattern, recursive=True):
                if os.path.isfile(file):
                    files.append(file)
        else:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path):
                    files.append(full_path)
    return files


def single_file(filepath):
    try:
        lines_counter = 0
        total_lines = 0

        with open(filepath, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file,1):
                total_lines += 1
                if args.i:
                    search_word = args.word.lower()
                    search_line = line.lower()
                else:
                    search_word = args.word
                    search_line = line

                match = search_word in search_line
                need_print = match if not args.v else not match

                if need_print:
                    lines_counter += 1

                    if not args.c and not args.l:
                        if args.n:
                            if args.r:
                                print(f"{filepath}:{line_number}:{line.strip()}")
                            else:
                                print(f"{line_number}:{line.strip()}")
                        else:
                            if args.r:
                                print(f"{filepath}:{line.strip()}")
                            else:
                                print(line.strip())

        if not args.l:
            if args.c:
                if args.r or len(get_file_list(args.path, args.r)) > 1:
                    print(f"{filepath}:{lines_counter}")
                else:
                    print(lines_counter)
        else:
            print(filepath)                
    except FileNotFoundError:
        sys.stderr.write(f"Файл {filepath} не найден\n")

def grep(args):
    files = get_file_list(args.path, args.r)

    for filepath in files:
        single_file(filepath)

if __name__ == "__main__":
    grep(args)