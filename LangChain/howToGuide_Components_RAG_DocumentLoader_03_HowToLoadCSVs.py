"""
How to load CSVs: https://python.langchain.com/docs/how_to/document_loader_csv/
"""

from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = "../integrations/document_loaders/example_data/mlb_teams_2012.csv"

loader = CSVLoader(file_path=file_path)
data = loader.load()

for record in data[:2]:
    print(record)