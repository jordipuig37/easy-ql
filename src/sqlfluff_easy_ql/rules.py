"""An example of a custom rule implemented through the plugin system.

This uses the rules API supported from 0.4.0 onwards.
"""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


# These two decorators allow plugins
# to be displayed in the sqlfluff docs
class Rule_EasyQL_L001(BaseRule):
    """ORDER BY on these columns is forbidden!

    **Anti-pattern**

    Using ``ORDER BY`` one some forbidden columns.

    .. code-block:: sql

        SELECT *
        FROM foo
        ORDER BY
            bar,
            baz

    **Best practice**

    Do not order by these columns.

    .. code-block:: sql

        SELECT *
        FROM foo
        ORDER BY bar
    """

    groups = ("all",)
    config_keywords = ["forbidden_columns"]
    crawl_behaviour = SegmentSeekerCrawler({"orderby_clause"})
    is_fix_compatible = True

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)
        self.forbidden_columns = [
            col.strip() for col in self.forbidden_columns.split(",")
        ]

    def _eval(self, context: RuleContext):
        """We should not ORDER BY forbidden_columns."""
        for seg in context.segment.segments:
            col_name = seg.raw.lower()
            if col_name in self.forbidden_columns:
                desc = f"Column `{col_name}` not allowed in ORDER BY."
                return LintResult(
                    anchor=seg,
                    description=desc
                )


# # These two decorators allow plugins
# # to be displayed in the sqlfluff docs
class Rule_EasyQL_L002(BaseRule):
    """JOIN and ON keyword should be in the same line.
    """
    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({"join_clause"})

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)
        with open("test_eval.txt", "a") as f:
            f.write("logging init L2")
            f.write("\n---\n")

    def _eval(self, context: RuleContext):
        """We should not JOIN .. ON differnet lines."""
        on_appeared = False
        for seg in context.segment.segments:
            if seg.raw.lower() == "on":
                on_appeared = True
            if seg.raw == "\n" and not on_appeared:
                desc = "Join and ON keyword should be at the same line."
                return LintResult(
                    anchor=seg,
                    description=desc
                )
