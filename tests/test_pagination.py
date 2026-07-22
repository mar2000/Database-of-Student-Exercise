from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_course_pagination_is_25_items_per_page():
    js=(ROOT/'site/assets/course.js').read_text(encoding='utf-8')
    builder=(ROOT/'generator/builder.py').read_text(encoding='utf-8')
    assert 'const PAGE_SIZE=25' in js
    assert 'a.slice(start,start+PAGE_SIZE)' in js
    assert 'id="pagination"' in builder
    assert 'currentPage=1;renderP()' in js
