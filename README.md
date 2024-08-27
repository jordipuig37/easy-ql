# Easy QL

EasyQL is a SQLFluff plugin to lint custom rules.

## Installation

You can install the plugin with pip:

```sh
pip install sqlfluff-plugin-easy-ql
```

Additionally you should add the following `.sqlfluff` file (also find it in the code provided in the repo).

```toml
[sqlfluff]
exclude_rules = LT02

[sqlfluff:layout:type:binary_operator]
line_position = trailing
```

## Usage

Once sqlfluff and this plugin are installed, call the linter normally and all the rules will be checked.

```sh
sqlfluff lint --dialect snowflake .
```
