"""
  How to create a custom Document Loader :  https://python.langchain.com/docs/how_to/document_loader_custom/
"""

""" Let's create an example of a standard document loader that loads a file and creates a document from each line in the file. """

from typing import AsyncIterator, Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class CustomDocumentLoader(BaseLoader):
    """An example document loader that reads a file line by line."""

    def __init__(self, file_path: str) -> None:
        """Initialize the loader with a file path.

        Args:
            file_path: The path to the file to load.
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:  # <-- Does not take any arguments
        """A lazy loader that reads a file line by line.

        When you're implementing lazy load methods, you should use a generator
        to yield documents one by one.
        """
        with open(self.file_path, encoding="utf-8") as f:
            line_number = 0
            for line in f:
                yield Document(
                    page_content=line,
                    metadata={"line_number": line_number, "source": self.file_path},
                )
                line_number += 1

    # alazy_load is OPTIONAL.
    # If you leave out the implementation, a default implementation which delegates to lazy_load will be used!
    async def alazy_load(
        self,
    ) -> AsyncIterator[Document]:  # <-- Does not take any arguments
        """An async lazy loader that reads a file line by line."""
        # Requires aiofiles
        # https://github.com/Tinche/aiofiles
        import aiofiles

        async with aiofiles.open(self.file_path, encoding="utf-8") as f:
            line_number = 0
            async for line in f:
                yield Document(
                    page_content=line,
                    metadata={"line_number": line_number, "source": self.file_path},
                )
                line_number += 1

# Test
with open("./meow.txt", "w", encoding="utf-8") as f:
    quality_content = "meow meow🐱 \n meow meow🐱 \n meow😻😻"
    f.write(quality_content)

loader = CustomDocumentLoader("./meow.txt")

# %pip install -q aiofiles
## Test out the lazy load interface
for doc in loader.lazy_load():
    print()
    print(type(doc))
    print(doc)

## Test out the async implementation
import asyncio
async def test_async_loader():
    async for doc in loader.alazy_load():
        print()
        print(type(doc))
        print(doc)
asyncio.run(test_async_loader())


""" ========================= Working with Files ==================================== """
# BaseBlobParser
from langchain_core.document_loaders import BaseBlobParser, Blob


class MyParser(BaseBlobParser):
    """A simple parser that creates a document from each line."""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Parse a blob into a document line by line."""
        line_number = 0
        with blob.as_bytes_io() as f:
            for line in f:
                line_number += 1
                yield Document(
                    page_content=line,
                    metadata={"line_number": line_number, "source": blob.source},
                )

blob = Blob.from_path("./meow.txt")
parser = MyParser()

list(parser.lazy_parse(blob))

blob = Blob(data=b"some data from memory\nmeow")
list(parser.lazy_parse(blob))

# Blob
blob = Blob.from_path("./meow.txt", metadata={"foo": "bar"})

blob.encoding

blob.as_bytes

blob.as_string

blob.as_bytes_io()

blob.metadata

blob.source

# Blob Loaders
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
filesystem_blob_loader = FileSystemBlobLoader(path=".", glob="*.mdx", show_progress=True)

# %pip install -q tqdm
parser = MyParser()
for blob in filesystem_blob_loader.yield_blobs():
    for doc in parser.lazy_parse(blob):
        print(doc)
        break

# Or, you can use CloudBlobLoader to load blobs from a cloud storage location (Supports s3://, az://, gs://, file:// schemes).

# %pip install -q 'cloudpathlib[s3]'

from cloudpathlib import S3Client, S3Path
from langchain_community.document_loaders.blob_loaders import CloudBlobLoader

client = S3Client(no_sign_request=True)
client.set_as_default_client()

path = S3Path(
    "s3://bucket-01", client=client
)  # Supports s3://, az://, gs://, file:// schemes.

cloud_loader = CloudBlobLoader(path, glob="**/*.pdf", show_progress=True)

for blob in cloud_loader.yield_blobs():
    print(blob)

# Generic Loader
from langchain_community.document_loaders.generic import GenericLoader

generic_loader_filesystem = GenericLoader(
    blob_loader=filesystem_blob_loader, blob_parser=parser
)
for idx, doc in enumerate(generic_loader_filesystem.lazy_load()):
    if idx < 5:
        print(doc)

print("... output truncated for demo purposes")

# Custom Generic Loader
from typing import Any


class MyCustomLoader(GenericLoader):
    @staticmethod
    def get_parser(**kwargs: Any) -> BaseBlobParser:
        """Override this method to associate a default parser with the class."""
        return MyParser()

loader = MyCustomLoader.from_filesystem(path=".", glob="*.mdx", show_progress=True)
for idx, doc in enumerate(loader.lazy_load()):
    if idx < 5:
        print(doc)
print("... output truncated for demo purposes")

