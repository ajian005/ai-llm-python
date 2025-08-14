"""
  How to load JSON: https://python.langchain.com/docs/how_to/document_loader_json/
"""

from langchain_community.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint
file_path='./example_data/facebook_chat.json'
data = json.loads(Path(file_path).read_text())
pprint(data)

""" Using JSONLoader """
loader = JSONLoader(
    file_path='./example_data/facebook_chat.json',
    jq_schema='.messages[].content',
    text_content=False)
data = loader.load()

""" JSON Lines file """
file_path = './example_data/facebook_chat_messages.jsonl'
pprint(Path(file_path).read_text())
loader = JSONLoader(
    file_path='./example_data/facebook_chat_messages.jsonl',
    jq_schema='.content',
    text_content=False,
    json_lines=True)
data = loader.load()

loader = JSONLoader(
    file_path='./example_data/facebook_chat_messages.jsonl',
    jq_schema='.',
    content_key='sender_name',
    json_lines=True)

data = loader.load()

""" JSON file with jq schema content_key """
file_path = './sample.json'
pprint(Path(file_path).read_text())

loader = JSONLoader(
    file_path=file_path,
    jq_schema=".data[]",
    content_key=".attributes.message",
    is_content_key_jq_parsable=True,
)

data = loader.load()

pprint(data)

""" Extracting metadata """
# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["sender_name"] = record.get("sender_name")
    metadata["timestamp_ms"] = record.get("timestamp_ms")
    return metadata

loader = JSONLoader(
    file_path='./example_data/facebook_chat.json',
    jq_schema='.messages[]',
    content_key="content",
    metadata_func=metadata_func
)

data = loader.load()


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["sender_name"] = record.get("sender_name")
    metadata["timestamp_ms"] = record.get("timestamp_ms")

    if "source" in metadata:
        source = metadata["source"].split("/")
        source = source[source.index("langchain"):]
        metadata["source"] = "/".join(source)

    return metadata


loader = JSONLoader(
    file_path='./example_data/facebook_chat.json',
    jq_schema='.messages[]',
    content_key="content",
    metadata_func=metadata_func
)

data = loader.load()