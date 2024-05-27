import argparse
import sqlparse as sp

from types import SimpleNamespace


def read_file(filepath: str) -> str:
    with open(filepath, 'r') as file:
        content = file.read()
    return content


def check_keyword_casing(statement: sp.sql.Statement) -> list:
    """Sample code from chatGPT"""
    issues = []
    for token in statement.tokens:
        if token.ttype in sp.tokens.Keyword:
            if not token.value.isupper():
                issues.append(f"Keyword '{token.value}' should be uppercase.")
    return issues


def check_indentation(statement: sp.sql.Statement, expected_indent=4) -> list:
    """Sample code from chatGPT"""
    issues = []
    lines = str(statement).split('\n')
    for i, line in enumerate(lines):
        stripped_line = line.lstrip()
        actual_indent = len(line) - len(stripped_line)
        if stripped_line and actual_indent % expected_indent != 0:
            issues.append(f"Line {i+1} not indented properly: '{line}'")
    return issues

style_checks = [check_keyword_casing, check_indentation]  # list of checks


def main(args: SimpleNamespace):
    sql = read_file(args.file)
    parsed_sql = sp.parse(sql)

    issues = []
    for statement in parsed_sql:
        for check_ in style_checks:
            issues.extend(check_(statement))

    for issue in issues:
        print(issue)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="The name of the file to lint")
    args = parser.parse_args()

    main(args)
