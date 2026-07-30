"""Static gates for the study-tab dispatch contract (the 'reader'
init defect, 2026-07-30). Shop laws applied: validate before teardown
(design-by-contract), declines must breadcrumb (Law 3), and a fixed
defect gets a gate so it cannot quietly return (Law 5).
"""
import os
import re
import unittest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHELL = os.path.join(_REPO_ROOT, "sentinel_personal_development.py")


def _method_body(src: str, name: str) -> str:
    start = src.index(f"def {name}(")
    nxt = src.find("\n    def ", start + 1)
    return src[start:nxt if nxt != -1 else len(src)]


class TestStudyTabContract(unittest.TestCase):
    def setUp(self):
        with open(_SHELL, encoding="utf-8") as f:
            self.src = f.read()

    def test_no_call_site_requests_the_removed_reader_tab(self):
        self.assertNotIn('_show_study_tab("reader")', self.src)
        self.assertNotIn("_show_study_tab('reader')", self.src)

    def test_key_validated_before_teardown(self):
        body = _method_body(self.src, "_show_study_tab")
        guard = body.index("not in self._study_tab_frames")
        teardown = body.index("pack_forget")
        self.assertLess(guard, teardown,
                        "key must be validated BEFORE tabs are torn down")

    def test_unknown_key_decline_breadcrumbs(self):
        body = _method_body(self.src, "_show_study_tab")
        self.assertIn("_qlog", body)

    def test_workspace_build_lands_on_a_registered_tab(self):
        body = _method_body(self.src, "open_study_workspace")
        m = re.search(r'_show_study_tab\("(\w+)"\)', body)
        self.assertIsNotNone(m, "workspace build must select a tab")
        tabs = re.findall(r'\("(\w+)",\s*"[^"]*",\s*self\._build_tab_',
                          body)
        self.assertIn(m.group(1), tabs,
                      "default tab must exist in the tabs registry")


if __name__ == "__main__":
    unittest.main()
