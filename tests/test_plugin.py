# stdlib
import ast
from typing import Set

# 3rd party
import pytest

# this package
from flake8_unused_fstrings import NUF001, Plugin


def results(s: str) -> Set[str]:
	return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


bad_code = [
		("f''", {f"1:0: {NUF001}"}),
		('f""', {f"1:0: {NUF001}"}),
		('f""""""', {f"1:0: {NUF001}"}),
		("f''''''", {f"1:0: {NUF001}"}),
		('(\n	"thing"\n	f"asdf"\n)', {f"2:1: {NUF001}"}),
		(
				"\nf''\nf''\n",
				{f"2:0: {NUF001}", f"3:0: {NUF001}"},
				),
		pytest.param(
				"""\nf"{f''}"\n""",
				None,
				marks=pytest.mark.xfail(reason="nested fstrings is not yet detected"),
				),
		]


@pytest.mark.parametrize("test_code, errors", bad_code)
def test_bad_code(test_code: str, errors: Set):
	assert results(test_code) == errors


good_code = [
		'"{}"',
		'"{{}}"',
		'"{{}}".format(1)',
		'\nthing = 1\nf"{thing}"\n',
		'\nasdf = 1\n(\n	"thing"\n	f"{asdf}"\n)\n',
		'"{val}".format(1)',
		"""
import time
import_start = time.time()
import_end = time.time()
cmd_name = "hi how are you?"
f"{0.123456789:.3f}"
f'Took {import_end - import_start:.3f} to import {cmd_name}'
""",
		"""\na = 3\nf'{f"{a}"}'\n""",
		]


@pytest.mark.parametrize("test_code", good_code)
def test_good_code(test_code: str):
	assert results(test_code) == set()
