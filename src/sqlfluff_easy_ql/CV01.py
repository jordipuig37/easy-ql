"""EasyQL convention rule 
"""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext
)
from sqlfluff.utils.functional import FunctionalContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_EasyQL_CV01(BaseRule):
    """Prohibit the use of 'WHERE 1=1' in queries."""
    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({"where_clause"})
    is_fix_compatible = False

    def _eval(self, context: RuleContext):
        text_segments = (
            FunctionalContext(context)
            .segment.children()
        )

        for idx, seg in enumerate(text_segments):
            # Look for the pattern '1=1'
            if "1=1" in seg.raw_upper.replace(" ", ""):
                return LintResult(anchor=seg)
        return None
