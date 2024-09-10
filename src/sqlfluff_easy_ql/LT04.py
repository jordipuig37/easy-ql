"""Implementation of custom rule for indentation in JOIN ... ON clauses."""

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_EasyQL_LT04(BaseRule):
    """Conditions in JOIN ... ON clause should be in a new line and indented.
    """
    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({"join_on_condition"})
    is_fix_compatible = False

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)

    def _eval(self, context: RuleContext):
        """Conditions in JOIN ... ON clause should be in a new line and
        indented.
        """
        segments = context.segment.segments
        # import pdb; pdb.set_trace()
        if segments[2].type != "newline":
            # add to lint errors the segment
            return [
                LintResult(
                    anchor=segments[0],
                    description="Conditions in JOIN ... ON clause should be in a new line."  # noqa: E501
                )
            ]

        elif segments[2].type == "newline" and \
                (segments[3].type != "whitespace" or
                 segments[3].type == "whitespace" and
                 len(segments[3].raw) != 4):
            return [
                LintResult(
                    anchor=segments[0],
                    description="Conditions in JOIN ... ON clause should be in a new line and indented with 4 spaces."  # noqa: E501
                )
            ]

        # TODO: check that all statements are properly indented
