[ ] Define the styleguide properly
    [ ] establish a way to categorize rules
    [ ] enumerate rules

[ ] list all the rules we need to add to the plugin
    [x] join and on in the same line
        [ ] disable default checks in the sqlfluff config
    [x] do not write 1 = 1 in where clause
    [x] name of object created in new indented line
    [ ] subqueries
    [ ] select * from final at the end of CTEs
    [ ] the last ; should be in a separate line, when the last line of the statement is indented
    ...

[x] setup the pipeline to turn this project into a PyPI (https://packaging.python.org/en/latest/tutorials/packaging-projects/)
    [ ] when first version is complete, release it to PyPI (not testpypi)
        https://twine.readthedocs.io/en/latest/

[x] setup flake8 and mypy linting for python code

[ ] Curate and improve code samples, for the guideline .md and for testing
    [ ] Think better and complete examples
    [ ] Change fields and table names

[x] Check https://docs.sqlfluff.com/en/stable/gettingstarted.html#basic-usage
    * https://docs.sqlfluff.com/en/stable/configuration.html#default-configuration

[ ] integrate the EasyQL plugin properly in the VS Code sqlfluff plugin
