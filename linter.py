import argparse
import pathlib
import subprocess


'''
- Scan directory recursively for input files
- Filter out paths/files to ignore
- check code formatting on all remaining files
'''

# Could be replaced with a map if more languages/extensions are to be added
c_cpp_file_extensions = {'c', 'cpp', 'h', 'hpp'}

ERROR = 1
OK = 0

class CheckerC:
    def is_file_ok(self, candidate: str) -> int:
        return self.__file_linting_ok(candidate) and self.__file_formatting_ok(candidate)


    def __file_formatting_ok(self, candidate: str) -> bool:
        clang_output = subprocess.check_output("clang-format -style=file --dry-run "
                + candidate, stderr=subprocess.STDOUT, shell=True)
        if clang_output != b'':
            print(clang_output.decode("utf-8"))
            return False
        return True


    def __file_linting_ok(self, candidate: str) -> bool:
        cppcheck_output = subprocess.check_output("cppcheck " + candidate +
                " --enable=warning,style,performance --quiet --inline-suppr",
                stderr=subprocess.STDOUT, shell=True)
        if cppcheck_output != b'':
            print(cppcheck_output.decode("utf-8"))
            return False
        return True


def parse_cmd_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = '''Run Format Checker and Linter on Source File'''
    )

    parser.add_argument(
        '--src', type=str,
        required=True,
        help='File to be checked'
    )
    parser.add_argument(
        '--ignore-list', type=str,
        help='File containing paths to ignore when going over input file',
        default='./.lint_ignore'
    )

    return parser.parse_args()


def is_ignore_candidate(candidate: str, ignore_list: [str]) -> bool:
    for item in ignore_list:
        if candidate.find(item) != -1:
            return True
    return False


def construct_ignore_list(path: str) -> [str]:
    ignore_list = []
    if pathlib.Path(path).is_file():
        with open(path) as f:
            for line in f:
                ignore_list.append(line.strip('\n'))
    return ignore_list


def check_file(candidate: str) -> int:
    checker = get_file_checker(candidate)
    if checker:
        print("return val {}".format(checker.is_file_ok(candidate)))
        if checker.is_file_ok(candidate):
            return OK
    return ERROR


def get_file_checker(candidate: str):
    if pathlib.Path(candidate).is_file():
        if has_c_file_extension(candidate):
            return CheckerC()
    return None


def has_c_file_extension(file_path: str) -> bool:
    try:
        # Look for files with a single dot in their name
        items = file_path.split('.')
    except ValueError:
        return False
    return items[-1] in c_cpp_file_extensions


def main():
    args = parse_cmd_args()
    items_to_ignore = construct_ignore_list(args.ignore_list)

    if is_ignore_candidate(args.src, items_to_ignore):
        exit(OK)
    else:
        exit(check_file(args.src))


if __name__ == "__main__":
  main()
