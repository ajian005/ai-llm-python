"""
  How to load HTML: https://python.langchain.com/docs/how_to/document_loader_html/
"""

"""  Loading HTML with Unstructured  """
from langchain_community.document_loaders import UnstructuredHTMLLoader
file_path = "../../docs/integrations/document_loaders/example_data/fake-content.html"
loader = UnstructuredHTMLLoader(file_path)
data = loader.load()
print(data)

""" Loading HTML with BeautifulSoup4 """
from langchain_community.document_loaders import BSHTMLLoader
loader = BSHTMLLoader(file_path)
data = loader.load()
print(data)