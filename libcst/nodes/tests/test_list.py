# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict
from typing import Any, Callable

import libcst.nodes as cst
from libcst.nodes.tests.base import CSTNodeTest
from libcst.parser import parse_expression, parse_statement
from libcst.testing.utils import data_provider


class ListTest(CSTNodeTest):

    # A lot of Element/StarredElement tests are provided by the tests for Tuple, so we
    # we don't need to duplicate them here.
    @data_provider(
        [
            # zero-element list
            {"node": cst.List([]), "code": "[]", "parser": parse_expression},
            # one-element list, sentinel comma value
            {
                "node": cst.List([cst.Element(cst.Name("single_element"))]),
                "code": "[single_element]",
                "parser": parse_expression,
            },
            # custom whitespace between brackets
            {
                "node": cst.List(
                    [cst.Element(cst.Name("single_element"))],
                    lbracket=cst.LeftSquareBracket(
                        whitespace_after=cst.SimpleWhitespace("\t")
                    ),
                    rbracket=cst.RightSquareBracket(
                        whitespace_before=cst.SimpleWhitespace("    ")
                    ),
                ),
                "code": "[\tsingle_element    ]",
                "parser": parse_expression,
            },
            # two-element list, sentinel comma value
            {
                "node": cst.List(
                    [cst.Element(cst.Name("one")), cst.Element(cst.Name("two"))]
                ),
                "code": "[one, two]",
                "parser": None,
            },
            # with parenthesis
            {
                "node": cst.List(
                    [cst.Element(cst.Name("one"))],
                    lpar=[cst.LeftParen()],
                    rpar=[cst.RightParen()],
                ),
                "code": "([one])",
                "parser": None,
            },
            # starred element
            {
                "node": cst.List(
                    [
                        cst.StarredElement(cst.Name("one")),
                        cst.StarredElement(cst.Name("two")),
                    ]
                ),
                "code": "[*one, *two]",
                "parser": None,
            },
            # missing spaces around list, always okay
            {
                "node": cst.For(
                    target=cst.List(
                        [
                            cst.Element(cst.Name("k"), comma=cst.Comma()),
                            cst.Element(cst.Name("v")),
                        ]
                    ),
                    iter=cst.Name("abc"),
                    body=cst.SimpleStatementSuite([cst.Pass()]),
                    whitespace_after_for=cst.SimpleWhitespace(""),
                    whitespace_before_in=cst.SimpleWhitespace(""),
                ),
                "code": "for[k,v]in abc: pass\n",
                "parser": parse_statement,
            },
        ]
    )
    def test_valid(self, **kwargs: Any) -> None:
        self.validate_node(**kwargs)

    @data_provider(
        (
            (
                lambda: cst.List(
                    [cst.Element(cst.Name("mismatched"))],
                    lpar=[cst.LeftParen(), cst.LeftParen()],
                    rpar=[cst.RightParen()],
                ),
                "unbalanced parens",
            ),
        )
    )
    def test_invalid(
        self, get_node: Callable[[], cst.CSTNode], expected_re: str
    ) -> None:
        self.assert_invalid(get_node, expected_re)