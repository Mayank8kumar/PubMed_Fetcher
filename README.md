# 📚 **PubMed Research Paper Fetcher**  
**A command-line tool to fetch PubMed research papers, filter non-academic authors, and save results in JSON, CSV, and SQLite database formats.**  

---

## 🚀 **Project Overview**  
This Python-based command-line tool retrieves research papers from **PubMed** based on a user-specified query. It identifies papers with at least one author affiliated with a **pharmaceutical** or **biotech company** and saves the results in:  

✔ **CSV file**  
✔ **JSON file**  
✔ **SQLite database**  

The tool supports PubMed's **full query syntax** and ensures efficient, organized storage of retrieved data.  

---

## 🔥 **Features**  

✅ Fetch research papers using the **PubMed API**  
✅ Identify **non-academic authors** based on affiliations  
✅ Extract **corresponding author emails** (if available)  
✅ Save results in **CSV, JSON, and SQLite database formats**  
✅ **Command-line interface (CLI)** for easy execution  
✅ **Efficient and robust error handling**  
✅ **Uses Poetry for dependency management**  

---

## 🏗 **Tech Stack**  

| Component        | Technology Used          |
|-----------------|-------------------------|
| **Backend**     | Python 3.11+              |
| **Data Fetching** | PubMed API (Entrez E-utilities) |
| **Storage**     | JSON, CSV, SQLite        |
| **CLI**         | Typer (Python)           |
| **Dependency Management** | Poetry         |
| **Testing**     | Pytest                    |
| **Version Control** | Git & GitHub         |

---

## 📂 **Project Structure**  

```
PubMedFetcher/
│── pubmed_fetcher/                   # Main package
│   ├── __init__.py
│   ├── cli.py                         # CLI Command handler
│   ├── config.py                      # Stores API URLs
│   ├── fetcher.py                      # Handles PubMed API requests
│   ├── utils.py                        # Helper functions (e.g., extracting emails)
│
│── tests/                             # Unit tests
│   ├── test_fetcher.py                 # Pytest test cases
│
│── results.csv                         # Output CSV file
│── pubmed_results.json                 # Output JSON file
│── pubmed_results.db                    # SQLite database file
│── pubmed_fetcher.log                   # Log file
│── README.md                           # Documentation (You are here)
│── pyproject.toml                       # Poetry configuration
│── poetry.lock                          # Poetry dependency lock file
```

---

## 🔧 **Installation & Setup**  

Follow these steps to install and run the PubMed Fetcher:  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Mayank8kumar/PubMed_Fetcher.git
cd PubMed_Fetcher
```

### **2️⃣ Install Poetry** (If not already installed)  
```bash
pip install poetry
```

### **3️⃣ Install Dependencies**  
```bash
poetry install
```

### **4️⃣ Activate Virtual Environment**  
```bash
poetry shell
```

---

## 🎯 **How to Use the Tool?**  

### **Basic Command**  
Run the following command to fetch research papers from PubMed:  
```bash
poetry run python pubmed_fetcher/cli.py "<search_query>" --max-results=<N>
```

🔹 Example: Searching for "cancer treatment" with 10 results:  
```bash
poetry run python pubmed_fetcher/cli.py "cancer treatment" --max-results=10
```

### **Output Formats:**  
- **CSV File:** `results.csv`  
- **JSON File:** `pubmed_results.json`  
- **Database File:** `pubmed_results.db`  

---

## ⚡ **Command-Line Options**  

| Option              | Description  |
|--------------------|-------------|
| `--help`          | Display usage instructions |
| `--max-results=N` | Set the maximum number of research papers to fetch |
| `--json-file`     | Specify the JSON file name |
| `--csv-file`      | Specify the CSV file name |
| `--db-file`       | Specify the SQLite database file name |

---

## ✅ **Example Output (CSV & JSON)**  

### **CSV Example (`results.csv`)**  
```
PubmedID,Title,Authors,Publication Date,Non-Academic Authors,Company Affiliations,Corresponding Author Email
40086967,"Eco-friendly production of D-tagatose","Wen, Lin, Liu",2025,"Lin","Qingdao Biotech Ltd.","songx@sdu.edu.cn"
40086617,"Diagnostic tests for tuberculosis","Alonzi, Petruccioli",2025,None,None,"delia.goletti@inmi.it"
```

### **JSON Example (`pubmed_results.json`)**  
```json
[
    {
        "PubmedID": "40086967",
        "Title": "Eco-friendly production of D-tagatose",
        "Authors": "Wen, Lin, Liu",
        "Publication Date": "2025",
        "Non-Academic Authors": "Lin",
        "Company Affiliations": "Qingdao Biotech Ltd.",
        "Corresponding Author Email": "songx@sdu.edu.cn"
    }
]
```

---

## 🧪 **Running Tests**  

To run tests using `pytest`, execute:  
```bash
poetry run pytest -v
```

🔹 **Expected Output (All Tests Passed ✅)**  
```bash
tests/test_fetcher.py::test_fetch_pubmed_articles PASSED  
tests/test_fetcher.py::test_fetch_article_details PASSED  
tests/test_fetcher.py::test_sample PASSED  
```

---

## 🔥 **Contributing**  

1️⃣ **Fork the repository**  
2️⃣ **Create a new branch** (`feature-branch`)  
3️⃣ **Commit your changes** (`git commit -m "New Feature Added"`)  
4️⃣ **Push the changes** (`git push origin feature-branch`)  
5️⃣ **Open a Pull Request**  


---

## 🌟 **Future Enhancements**  

🔹 Deploy as a **Python package on PyPI**  
🔹 Implement **a Web Interface using Flask/FastAPI**  
🔹 Enhance **data filtering** with additional criteria  
🔹 Add **support for more metadata fields from PubMed**  

---

## 👤 **Author**  

Developed by **Mayank Kumar**  
🔗 [GitHub Profile](https://github.com/Mayank8kumar)  

---

🚀 **Happy Researching!** 🚀
