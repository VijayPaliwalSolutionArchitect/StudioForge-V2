"""backend/tests/test_brand_retriever_rag.py — Brand guideline retrieval tests."""

from app.rag.brand_retriever import BrandRetriever


def test_retriever_extracts_brand_pillars(client):
    retriever: BrandRetriever = client.app.state.retriever
    guidelines = retriever.retrieve_guidelines("brand-shivam-itcs", "enterprise AI campaign")
    assert guidelines["brand_found"] is True
    assert guidelines["brand_name"] == "Shivam ITCS"
    assert "Authoritative" in guidelines["tone_pillars"]
    assert "Chief Technology Officers" in guidelines["target_personas"]


def test_retriever_includes_forbidden_words(client):
    retriever: BrandRetriever = client.app.state.retriever
    guidelines = retriever.retrieve_guidelines("brand-shivam-itcs", "query")
    assert "cheap" in guidelines["forbidden_words"]
    assert "hacky" in guidelines["forbidden_words"]


def test_retriever_non_existent_brand(client):
    retriever: BrandRetriever = client.app.state.retriever
    guidelines = retriever.retrieve_guidelines("brand-unknown-999", "query")
    assert guidelines["brand_found"] is False


def test_retriever_color_palette(client):
    retriever: BrandRetriever = client.app.state.retriever
    guidelines = retriever.retrieve_guidelines("brand-shivam-itcs", "palette")
    assert guidelines["primary_color"] == "#06b6d4"
    assert guidelines["secondary_color"] == "#3b82f6"
