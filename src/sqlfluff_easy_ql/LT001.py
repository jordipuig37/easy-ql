"""Implementation of Rule CV06."""

from typing import List

from sqlfluff.core.parser import NewlineSegment, WhitespaceSegment
from sqlfluff.core.rules import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_EasyQL_LT001(BaseRule):
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

    def _eval(self, context: RuleContext) -> List[LintResult]:
        # skip entire part of CREATE [OR REPLACE]
        segments = context.segment.segments
        obj_reference = context.segment.type.split("_")[1] + "_reference"
        table_name_idx, table_name_segment = next(
            ((idx, s) for idx, s in enumerate(segments)
                if s.type == obj_reference)
        )

        # assert that there is a newline and 4 spaces before the name
        if segments[table_name_idx-2].type == "newline" and \
                segments[table_name_idx-1].type == "whitespace" and \
                len(segments[table_name_idx-1].raw) == 4:
            return None
        else:  # apply fixes and return lint result
            fixes_to_apply = list()
            # [ ] (wip) make the logic robust and do not leave trailing spaces
            #   as a result of the fix
            fix = LintFix.create_before(
                    table_name_segment,
                    [NewlineSegment(), WhitespaceSegment("    ")]
            )
            fixes_to_apply.append(fix)

            return LintResult(
                    anchor=table_name_segment,
                    fixes=fixes_to_apply,
                    description="Stylish create"
                )
