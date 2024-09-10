# Easy QL

EasyQL is a SQLFluff plugin to lint custom rules.

## Installation

You can install the plugin with pip:

```sh
pip install sqlfluff-plugin-easy-ql
```

Additionally you should add the following `.sqlfluff` file (also find it in the code provided in the repo).

```
[sqlfluff]
exclude_rules = LT02

[sqlfluff:layout:type:binary_operator]
line_position = trailing
```

## Usage

Once sqlfluff and this plugin are installed, call the linter normally and all the standard and custom rules will be checked.

```sh
sqlfluff lint --dialect snowflake .
```

Additionally, we added a command to analyze a tree of directories and store the linting results. The command `easy-ql lint` will lint all files with `.sql` extension and store the results for each file in another file named `<original_file_name>.lint.sql`.
This command accepts three arguments:

* --dialect: to indicate the dialect
* --directory or --file to indicate the directory to be analized or a single file

Examples:

```sh
easy-ql lint --dialect snowflake --directory sql_samples
easy-ql lint --dialect tsql --file sql_samples/test1.sql
```
