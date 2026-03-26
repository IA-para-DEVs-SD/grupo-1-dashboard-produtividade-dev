from pathlib import Path


def test_app_contains_streamlit_title():
    """Verify that app.py contains the expected st.title call."""
    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    content = app_path.read_text(encoding="utf-8")
    assert 'st.title("Dashboard de Produtividade Dev")' in content
