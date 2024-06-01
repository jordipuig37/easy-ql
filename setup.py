from setuptools import find_packages, setup

# Change these names in your plugin, e.g. company name or plugin purpose.
PLUGIN_LOGICAL_NAME = "easy-ql"
PLUGIN_ROOT_MODULE = "sqlfluff_easy_ql"

setup(
    name=f"sqlfluff-plugin-{PLUGIN_LOGICAL_NAME}",
    version="0.1.0",
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires="sqlfluff>=0.4.0",
    entry_points={
        "sqlfluff": [f"sqlfluff_{PLUGIN_LOGICAL_NAME} = {PLUGIN_ROOT_MODULE}"]
    },
)
