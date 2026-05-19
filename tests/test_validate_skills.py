from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import split_frontmatter, validate_skill


class ValidateSkillsTests(unittest.TestCase):
    def test_split_frontmatter_requires_closing_delimiter_line(self) -> None:
        with self.assertRaises(ValueError):
            split_frontmatter('---\nname: "tool"\ndescription: "Use it"\n# Body\n')

    def test_validate_skill_accepts_delimited_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tool" / "SKILL.md"
            path.parent.mkdir()
            path.write_text(
                '---\nname: "tool"\ndescription: "Use it"\n---\n\n# Tool\n',
                encoding="utf-8",
            )

            self.assertEqual(validate_skill(path), [])


if __name__ == "__main__":
    unittest.main()
