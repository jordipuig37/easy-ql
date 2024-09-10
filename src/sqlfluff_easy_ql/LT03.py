"""Implementation of custom rule for indentation in JOIN ... ON clauses."""

from typing import List

from sqlfluff.core.parser import NewlineSegment, WhitespaceSegment
from sqlfluff.core.rules import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.parser.segments.base import BaseSegment
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_EasyQL_LT03(BaseRule):
    """JOIN and ON keyword should be in the same line.
    """
    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({"join_clause"})

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)

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
