"""Implementation of Rule CV06."""

from typing import List

from sqlfluff.core.parser import NewlineSegment, WhitespaceSegment
from sqlfluff.core.rules import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_EasyQL_LT01(BaseRule):
    """The name of the objects created in CREATE statements should be indented.
    """
    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({
        # more or less all matches to create_(.*)_statement
        "create_table_statement",
        "create_index_statement",
        "create_view_statement",
        "create_function_statement",
        "create_procedure_statement"
    })
    is_fix_compatible = True

    def _aux_fix(self, segments, object_name_segment, object_name_idx) -> List[LintFix]:
        """Applies the fix logic for the different possible cases."""
        fix_segments = list()

        # check whether there is a newline
        if segments[object_name_idx-2].type != "newline" and \
                segments[object_name_idx-1].type != "newline":
            fix_segments.append(NewlineSegment())
        # check the indentation
        if segments[object_name_idx-1].type != "whitespace" or \
                len(segments[object_name_idx-1].raw) != 4:
            fix_segments.append(WhitespaceSegment("    "))

        fix = LintFix.create_before(
            object_name_segment,
            fix_segments
        )

        return [fix]

    def _eval(self, context: RuleContext) -> List[LintResult]:
        # skip entire part of CREATE [OR REPLACE]
        segments = context.segment.segments
        obj_reference = context.segment.type.split("_")[1] + "_reference"
        table_name_idx, table_name_segment = next(
            ((idx, s) for idx, s in enumerate(segments)
                if s.type == obj_reference or s.type == "function_name")  # in procedures is function_name
        )

        # assert that there is a newline and 4 spaces before the name
        if segments[table_name_idx-2].type == "newline" and \
                segments[table_name_idx-1].type == "whitespace" and \
                len(segments[table_name_idx-1].raw) == 4:
            return None
        else:  # apply fixes and return lint result
            fixes_to_apply = self._aux_fix(segments, table_name_segment, table_name_idx)

            return LintResult(
                    anchor=table_name_segment,
                    fixes=fixes_to_apply,
                    description="The name of the created object must be in a new line and indented."
                )
