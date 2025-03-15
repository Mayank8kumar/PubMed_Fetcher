import requests
import logging
from typing import List, Dict
from lxml import etree
from .config import PUBMED_SEARCH_URL, PUBMED_FETCH_URL,PUBMED_DETAILS_URL
from .utils import extract_email_from_affiliation, detect_non_academic_authors
import time

logging.basicConfig(level=logging.INFO)


def fetch_pubmed_articles(query: str, max_results: int = 10) -> List[Dict]:
    """Fetches PubMed articles based on a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    try:
        response = requests.get(PUBMED_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 🔍 Print API response
        print("🔍 PubMed Response:", data)

        article_ids = data.get("esearchresult", {}).get("idlist", [])
        
        # Debug: Print extracted IDs
        # print(f"✅ Extracted article IDs: {article_ids}")

        return fetch_article_details(article_ids) if article_ids else []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching articles: {e}")
        return []



def fetch_article_details(article_ids: List[str]) -> List[Dict]:
    """Fetches detailed information about PubMed articles given their IDs."""
    
    if not article_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(article_ids),
        "retmode": "xml"
    }

    try:
        time.sleep(1)  # ⏳ Prevent PubMed API rate limits
        response = requests.get(PUBMED_DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()

        # 🔍 Debug API response
        # print(f"✅ PubMed API Response Code: {response.status_code}")
        # print(f"🔍 Response Content (first 500 chars): {response.text[:500]}")

        root = etree.fromstring(response.content)

        # Proceed with parsing XML data
        articles = []
        for article in root.xpath("//PubmedArticle"):
            title = article.xpath(".//ArticleTitle/text()")
            title = title[0] if title else "N/A"

            pubmed_id = article.xpath(".//MedlineCitation/PMID/text()")
            pubmed_id = pubmed_id[0] if pubmed_id else "N/A"

            pub_date = article.xpath(".//PubDate/Year/text()")
            pub_date = pub_date[0] if pub_date else "N/A"

            authors = article.xpath(".//Author/LastName/text()")
            authors = ", ".join(authors) if authors else "N/A"

            affiliations = article.xpath(".//AffiliationInfo/Affiliation/text()")
            
            corresponding_email = extract_email_from_affiliation(affiliations)

            non_academic_authors, companies = detect_non_academic_authors(affiliations, authors.split(", "))

            articles.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Authors": authors,
                "Publication Date": pub_date,
                "Non-Academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "None",
                "Company Affiliations": ", ".join(companies) if companies else "None",
                "Corresponding Author Email": corresponding_email
            })

        return articles

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching article details: {e}")
        return []