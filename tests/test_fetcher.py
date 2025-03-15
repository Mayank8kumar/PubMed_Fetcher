import pytest
from pubmed_fetcher.fetcher import fetch_article_details
from pubmed_fetcher.fetcher import fetch_pubmed_articles

def test_fetch_pubmed_articles():
    """Test fetching PubMed articles with a valid query."""
    results = fetch_pubmed_articles("cancer", max_results=3)
    assert isinstance(results, list)  # Should return a list
    assert len(results) > 0  # Ensure we get results
    assert "Title" in results[0]  # Check if title exists in results



def test_fetch_article_details():
    """Test fetching article details with valid IDs."""
    article_ids = ["40087147", "40087146"]  # Example valid PubMed IDs
    results = fetch_article_details(article_ids)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "Authors" in results[0]


def test_sample():
    assert 1 + 1 == 2  # Basic check 

