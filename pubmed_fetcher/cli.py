import typer
import json
import sqlite3
import csv
from pubmed_fetcher.fetcher import fetch_pubmed_articles

app = typer.Typer()

@app.command()
def search(
    query: str, 
    max_results: int = 5, 
    json_file: str = "pubmed_results.json", 
    db_file: str = "pubmed_results.db",
    csv_file: str = "pubmed_results.csv"
):
    """
    CLI command to fetch and store PubMed articles.
    """
    typer.echo(f"🔍 Searching PubMed for: {query} with max results: {max_results}")
    results = fetch_pubmed_articles(query, max_results)

    if results:
        save_to_json(results, json_file)
        save_to_database(results, db_file)
        save_to_csv(results, csv_file)
        typer.echo(f"✅ Results saved to {json_file}, {db_file}, and {csv_file}")
    else:
        typer.echo("⚠️ No results found.")

def save_to_json(data, filename):
    """Saves articles to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_to_database(data, db_filename):
    """Saves articles to an SQLite database."""
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pubmed_id TEXT,
            title TEXT,
            authors TEXT,
            publication_date TEXT,
            non_academic_authors TEXT,
            company_affiliations TEXT,
            corresponding_author_email TEXT
        )
    """)

    for article in data:
        cursor.execute("""
            INSERT INTO papers (pubmed_id, title, authors, publication_date, 
            non_academic_authors, company_affiliations, corresponding_author_email) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                article["PubmedID"], article["Title"], article["Authors"], 
                article["Publication Date"], article["Non-Academic Authors"], 
                article["Company Affiliations"], article["Corresponding Author Email"]
            )
        )

    conn.commit()
    conn.close()

def save_to_csv(data, filename):
    """Saves articles to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    app()
