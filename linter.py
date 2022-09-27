import argparse
import pathlib
import subprocess


'''
- Scan directory recursively for input files
- Filter out paths/files to ignore
- check code formatting on all remaining files
'''

c_cpp_file_extensions = {'c', 'cpp', 'h', 'hpp'}
ERROR = 1
OK = 0


def parse_cmd_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description = '''Run Format Checker and Linter on Source File'''
  )

  parser.add_argument(
    '--src', type=str,
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


def is_file_ok(candidate: str) -> int:
  if pathlib.Path(candidate).is_file():
    if has_c_cpp_file_extension(candidate):
      return is_c_file_ok(candidate)
  return OK


def has_c_cpp_file_extension(file_path: str) -> bool:
  try:
    # Look for files with a single dot in their name
    items = file_path.split('.')
  except ValueError:
    return False
  return items[-1] in c_cpp_file_extensions


def is_c_file_ok(candidate: str) -> int:
  if c_file_linting_ok(candidate) and c_file_formatting_ok(candidate):
    return OK
  return ERROR


def c_file_formatting_ok(candidate: str) -> bool:
  clang_output = subprocess.check_output("clang-format -style=file --dry-run "
      + candidate, stderr=subprocess.STDOUT, shell=True)
  if clang_output != b'':
    print(clang_output.decode("utf-8"))
    return False
  return True


def c_file_linting_ok(candidate: str) -> bool:
  cppcheck_output = subprocess.check_output("cppcheck " + candidate +
      " --enable=warning,style,performance --quiet --inline-suppr",
      stderr=subprocess.STDOUT, shell=True)
  if cppcheck_output != b'':
    print(cppcheck_output.decode("utf-8"))
    return False
  return True


def construct_ignore_list(path: str) -> [str]:
  ignore_list = []
  if pathlib.Path(path).is_file():
    with open(path) as f:
      for line in f:
        ignore_list.append(line.strip('\n'))
  return ignore_list


def main():
  args = parse_cmd_args()
  items_to_ignore = construct_ignore_list(args.ignore_list)

  if is_ignore_candidate(args.src, items_to_ignore):
    exit(OK)
  else:
    exit(is_file_ok(args.src))


if __name__ == "__main__":
  main()
