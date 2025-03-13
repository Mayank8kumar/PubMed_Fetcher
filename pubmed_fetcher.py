import requests
import json
import sqlite3
import time
import logging
from lxml import etree
from typing import List, Dict
import typer

# Initialize Logging
logging.basicConfig(
    filename="pubmed_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# PubMed API Base URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Function to fetch data from PubMed
def fetch_pubmed_articles(query: str, max_results: int = 5, retries: int = 3) -> List[Dict]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    
    for attempt in range(retries):
        try:
            logging.info(f"Fetching PubMed results for query: {query} (Attempt {attempt+1})")
            response = requests.get(PUBMED_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse XML response
            root = etree.fromstring(response.content)
            article_ids = root.xpath("//IdList/Id/text()")

            if not article_ids:
                logging.warning(f"No results found for query: {query}")
                return []

            return fetch_article_details(article_ids)
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Network/API error on attempt {attempt+1}: {e}")
            time.sleep(2)  # Wait before retrying

    logging.error(f"Failed to fetch data for query '{query}' after {retries} attempts")
    return []

# Function to fetch detailed article data
def fetch_article_details(article_ids: List[str]) -> List[Dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(article_ids),
        "retmode": "xml"
    }

    try:
        response = requests.get(PUBMED_DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()
        root = etree.fromstring(response.content)
        
        articles = []
        for article in root.xpath("//PubmedArticle"):
            title = article.xpath(".//ArticleTitle/text()")[0] if article.xpath(".//ArticleTitle/text()") else "N/A"
            authors = ", ".join(article.xpath(".//Author/LastName/text()"))
            journal = article.xpath(".//Journal/Title/text()")[0] if article.xpath(".//Journal/Title/text()") else "N/A"
            pub_date = article.xpath(".//PubDate/Year/text()")[0] if article.xpath(".//PubDate/Year/text()") else "N/A"

            articles.append({
                "Title": title,
                "Authors": authors,
                "Journal": journal,
                "Publication Date": pub_date
            })
        
        return articles

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching article details: {e}")
        return []

# Function to save data in JSON format
def save_to_json(data: List[Dict], filename: str):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.write("\n")
        logging.info(f"Successfully saved {len(data)} articles to {filename}")
    except IOError as e:
        logging.error(f"Error saving data to JSON: {e}")

# Function to save data in SQLite database
def save_to_database(data: List[Dict], db_filename: str):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                authors TEXT,
                journal TEXT,
                publication_date TEXT
            )
        """)

        for article in data:
            # Check for duplicates based on both title and authors
            cursor.execute("SELECT COUNT(*) FROM papers WHERE title = ? AND authors = ?", 
                           (article["Title"], article["Authors"]))
            if cursor.fetchone()[0] == 0:  # Avoid duplicates
                cursor.execute("INSERT INTO papers (title, authors, journal, publication_date) VALUES (?, ?, ?, ?)", 
                               (article["Title"], article["Authors"], article["Journal"], article["Publication Date"]))
        
        conn.commit()
        conn.close()
        logging.info(f"Successfully saved {len(data)} articles to {db_filename}")

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")


# CLI Interface
app = typer.Typer()

@app.command()
def search(query: str, max_results: int = 5, json_file: str = "pubmed_results.json", db_file: str = "pubmed_results.db"):
    typer.echo(f"🔍 Searching PubMed for: {query} with max results: {max_results}")
    results = fetch_pubmed_articles(query, max_results)

    if results:
        save_to_json(results, json_file)
        save_to_database(results, db_file)
        typer.echo(f"✅ Results appended to {json_file}")
        typer.echo(f"✅ Results appended to {db_file}")
    else:
        typer.echo("⚠️ No results found.")

if __name__ == "__main__":
    app()
