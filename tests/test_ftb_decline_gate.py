"""Static gate for punch item #5: silent declines in the floating-
toolbar dispatch chains. Law 3 — a decline must SPEAK. This gate scans
every *_from_toolbar helper and fails if an `except` handler returns
False without breadcrumbing first (the claimed-but-failed swallow that
made 'the button does nothing' reports undiagnosable).
"""
import os
import re
import unittest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHELL = os.path.join(_REPO_ROOT, "sentinel_personal_development.py")


class TestDeclinesSpeak(unittest.TestCase):
    def test_no_unlogged_except_swallow_in_toolbar_chain(self):
        with open(_SHELL, encoding="utf-8") as f:
            src = f.read()
        offenders = []
        for m in re.finditer(
                r"def (_\w+_from_toolbar)\(self\).*?(?=\n    def )",
                src, re.S):
            name, body = m.group(1), m.group(0)
            # Line-based scan (no regex backtracking): inside each
            # `except ...:` handler, `return False` must be preceded by
            # a _qlog breadcrumb somewhere in that handler block.
            lines = body.splitlines()
            i = 0
            while i < len(lines):
                stripped = lines[i].strip()
                if stripped.startswith("except") and stripped.endswith(":"):
                    indent = len(lines[i]) - len(lines[i].lstrip())
                    handler, j = [], i + 1
                    while j < len(lines):
                        nxt = lines[j]
                        if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                            break
                        handler.append(nxt)
                        j += 1
                    block = "\n".join(handler)
                    if "return False" in block and "_qlog" not in block:
                        offenders.append(name)
                    i = j
                else:
                    i += 1
        self.assertEqual(
            offenders, [],
            f"silent except-swallows in toolbar chain: {offenders} — "
            "a decline must breadcrumb (_qlog) before returning False")

    def test_terminal_fallthroughs_speak(self):
        with open(_SHELL, encoding="utf-8") as f:
            src = f.read()
        for chain in ("ftb-add: fell through", "ftb-remove: fell through",
                      "ftb-save: fell through"):
            self.assertIn(chain, src)


if __name__ == "__main__":
    unittest.main()
