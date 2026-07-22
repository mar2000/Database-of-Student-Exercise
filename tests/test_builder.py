from pathlib import Path
import json, unittest
from generator import builder
class Tests(unittest.TestCase):
 def test_content(self):
  f,c,p,m=builder.collect(); self.assertEqual(len(f),3); self.assertEqual(len(c),4); self.assertGreaterEqual(len(p),5); self.assertGreaterEqual(len(m),4)
 def test_build(self):
  builder.build_site(); d=json.loads((builder.BUILD/'data/catalog.json').read_text()); self.assertIn('fields',d); self.assertTrue((builder.BUILD/'files/uw-matematyka-am2/uw-matematyka-am2-analiza-matematyczna-ii-cwiczenia/Analiza_Matematyczna_II.pdf').exists())
if __name__=='__main__': unittest.main()



def test_course_page_has_correct_mathjax_and_no_random():
    builder.build_site()
    page=(builder.BUILD/'przedmioty'/'uw-matematyka-am2'/'index.html').read_text(encoding='utf-8')
    assert '\\\\(' in page
    assert '\\\\[' in page
    assert 'id="random"' not in page
    assert 'Wylosuj' not in page

def test_course_script_has_no_random_handler():
    script=(builder.ROOT/'site'/'assets'/'course.js').read_text(encoding='utf-8')
    assert 'random.onclick' not in script

def test_problem_filters_are_exactly_three():
    builder.build_site()
    page=(builder.BUILD/'przedmioty'/'uw-matematyka-am2'/'index.html').read_text(encoding='utf-8')
    assert 'id="topic"' in page
    assert 'id="difficulty"' in page
    assert 'id="source-type"' in page
    assert 'id="search"' not in page
    assert 'id="academic-year"' not in page
    for label in ['Kolokwium','Egzamin','Ćwiczenia','Inne']:
        assert f'>{label}<' in page

def test_source_filter_groups_other_types_as_inne():
    script=(builder.ROOT/'site'/'assets'/'course.js').read_text(encoding='utf-8')
    assert "return 'inne'" in script
    assert "sourceCategory(x.source.type)===s" in script

def test_set_page_exports_pdf_without_printing():
    builder.build_site()
    page=(builder.BUILD/'zestaw'/'index.html').read_text(encoding='utf-8')
    script=(builder.ROOT/'site'/'assets'/'set.js').read_text(encoding='utf-8')
    assert 'Eksportuj zadania do PDF' in page
    assert 'html2pdf.bundle.min.js' in page
    assert 'id="print-set"' not in page
    assert 'print()' not in script
    assert 'html2pdf()' in script
    assert 'zestaw-zadan-' in script


def test_pdf_export_uses_svg_math_and_removes_accessibility_duplicates():
    builder.build_site()
    page=(builder.BUILD/'zestaw'/'index.html').read_text(encoding='utf-8')
    script=(builder.ROOT/'site'/'assets'/'set.js').read_text(encoding='utf-8')
    style=(builder.ROOT/'site'/'assets'/'style.css').read_text(encoding='utf-8')
    assert 'tex-svg.js' in page
    assert 'tex-mml-chtml.js' not in page
    assert "mjx-assistive-mml" in script
    assert "node.remove()" in script
    assert 'font-size:13px' in style
    assert 'font-size:28px' in style


def test_am2_topics_are_canonical_and_complete():
    import yaml
    course=yaml.safe_load((builder.CONTENT/'courses'/'uw-matematyka-am2'/'course.yaml').read_text(encoding='utf-8'))
    ids=[t['id'] for t in course['topics']]
    expected=[
        'normy-iloczyn-skalarny','granice-ciaglosc-wielu-zmiennych','pochodna-funkcji-wielu-zmiennych',
        'rozniczkowanie-zlozenia','stozki-styczne-gradient','ekstrema','wzor-taylora','funkcja-uwiklana',
        'funkcja-odwrotna','teoria-miary','twierdzenia-lebesguea-o-zbieznosci','rozniczkowanie-pod-znakiem-calki',
        'twierdzenie-fubiniego','calkowanie-przez-podstawienie','srodek-ciezkosci','calkowalnosc-funkcji',
        'sploty','przestrzenie-lp','aproksymacja-funkcjami-gladkimi','transformata-fouriera','podrozmaitosci',
        'wyznacznik-grama','miara-powierzchniowa','powierzchnie-obrotowe','formy-rozniczkowe-1',
        'calki-z-form-po-krzywych','rozniczka-zewnetrzna','formy-rozniczkowe-k','cofniecie-formy','twierdzenie-stokesa'
    ]
    assert ids == expected

def test_all_am2_problem_topics_are_known():
    import yaml
    course_dir=builder.CONTENT/'courses'/'uw-matematyka-am2'
    course=yaml.safe_load((course_dir/'course.yaml').read_text(encoding='utf-8'))
    allowed={t['id'] for t in course['topics']}
    for path in (course_dir/'zadania').glob('*.md'):
        meta=yaml.safe_load(path.read_text(encoding='utf-8').split('---',2)[1])
        assert set(meta.get('topics',[])) <= allowed, path


def test_problem_statement_uses_normal_font_weight():
    root = Path(__file__).resolve().parents[1]
    course_js = (root / "site" / "assets" / "course.js").read_text(encoding="utf-8")
    css = (root / "site" / "assets" / "style.css").read_text(encoding="utf-8")
    assert 'class="math statement"' in course_js
    assert '.statement, .statement p' in css
    assert 'font-weight: 400 !important' in css
