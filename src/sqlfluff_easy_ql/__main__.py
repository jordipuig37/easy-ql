import argparse
import sys
import os
import subprocess

from tqdm import tqdm
from pathlib import Path


def write_results(
        result: subprocess.CompletedProcess[str],
        lint_output_path: str
) -> None:
    """
    Writes sqfluff output to a file. If the file already exists
    the file is rewritten. If the process ends without lint errors,
    the file is not written and if it exists the file is deleted.
    """
    if result.returncode != 0:
        with open(lint_output_path, "w") as output_file:
            output_file.write(result.stdout)
    else:
        if os.path.exists(lint_output_path):
            os.remove(lint_output_path)


def lint_sql_files(directory: str, dialect: str):
    tree = list(os.walk(directory))
    for root, _, files in tqdm(
        tree, desc="Processing directories", position=0
    ):
        for file in tqdm(
            files, desc=f"Processing files in {root}", position=1, leave=False
        ):
            if Path(file).suffix.lower() == ".sql":
                file_path = os.path.join(root, file)
                file_name = Path(file_path).stem
                lint_output_path = f"{file_name}.lint.txt"

                # Run sqlfluff lint and capturing the output
                result = subprocess.run([
                    "python", "-m", "sqlfluff", "lint", "--dialect", dialect,
                    file_path],
                    capture_output=True, text=True
                )
                write_results(result, lint_output_path)


def lint_single_sql_file(file_path: str, dialect: str):
    if Path(file_path).suffix.lower() == ".sql":
        file_name = file_name = Path(file_path).stem
        lint_output_path = f"{file_name}.lint.txt"

        result = subprocess.run([
            "python", "-m", "sqlfluff", "lint", "--dialect", dialect,
            file_path],
            capture_output=True, text=True
        )
        write_results(result, lint_output_path)


def lint(args):
    """Main linter adapted to easy-ql.

    This function will lint the files (either a single one or all files in a
    directory) and store the lint results in a new file with the name pattern:
    <original_file_name>.lint.txt

    Arguments include: (see main)
        + dialect
        + file
        + directory
    """
    if args.file != "":
        lint_single_sql_file(args.file, args.dialect)
    else:
        lint_sql_files(args.directory, args.dialect)


def main():
    parser = argparse.ArgumentParser(prog='easy-ql')
    subparsers = parser.add_subparsers(dest='command')

    parser_lint = subparsers.add_parser(
        'lint', help='Run the lint and save the results in files'
    )
    parser_lint.add_argument(
        '--directory',
        type=str, default=".",
        help="If this option is set, lint all .sql files in the directory."
    )
    parser_lint.add_argument(
        "-f", '--file',
        type=str, default="",
        help="If this option is set, lint the file."
    )
    parser_lint.add_argument(
        '--dialect',
        type=str, default="ansi",
        help="The dialect used to lint the files."
    )
    parser_lint.set_defaults(func=lint)

    # Parse the arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Call the appropriate function
    args.func(args)
