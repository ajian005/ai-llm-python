"""
  How to load Microsoft Office files : https://python.langchain.com/docs/how_to/document_loader_office_file/
"""

""" Loading DOCX, XLSX, PPTX with AzureAIDocumentIntelligenceLoader """
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader

file_path = "<filepath>"
endpoint = "<endpoint>"
key = "<key>"
loader = AzureAIDocumentIntelligenceLoader(
    api_endpoint=endpoint, api_key=key, file_path=file_path, api_model="prebuilt-layout"
)

documents = loader.load()

