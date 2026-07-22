from pathlib import Path

def test_statement_typography_normalization_present():
    root=Path(__file__).resolve().parents[1]
    js=(root/"build/assets/course.js").read_text(encoding="utf-8")
    css=(root/"build/assets/style.css").read_text(encoding="utf-8")
    assert "normalizeStatementTypography" in js
    assert "font-variation-settings" in js
    assert ".statement p" in css
