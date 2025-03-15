import csv
from typing import List, Tuple
import re


def extract_company_affiliation(affiliations: List[str]) -> Tuple[List[str], List[str]]:
    """Identifies non-academic authors and companies from affiliations."""
    company_keywords = ["pharma", "biotech", "inc", "ltd", "gmbh", "corporation", "company"]
    company_authors = []
    companies = []

    for aff in affiliations:
        if any(keyword in aff.lower() for keyword in company_keywords):
            company_authors.append(aff.split(",")[0])  # Extract author name
            companies.append(aff)

    return company_authors, companies

def extract_email_from_affiliation(affiliations: List[str]) -> str:
    """Extracts the email address from author affiliations if available."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    for aff in affiliations:
        email_match = re.search(email_pattern, aff)
        if email_match:
            return email_match.group(0)

    return "N/A"



def detect_non_academic_authors(affiliations: List[str], authors: List[str]) -> Tuple[List[str], List[str]]:
    """Identifies non-academic authors and extracts company affiliations."""

    academic_keywords = ["university", "college", "hospital", "institute", "research center", "lab"]
    company_authors = []
    company_names = []

    for author, aff in zip(authors, affiliations):
        if not any(keyword.lower() in aff.lower() for keyword in academic_keywords):  
            company_authors.append(author)
            company_names.append(aff)
    
    return company_authors, company_names

def save_to_csv(data: List[dict], filename: str):
    """Saves article data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
