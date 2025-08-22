"""
  How to create a custom Retriever :  https://python.langchain.com/docs/how_to/custom_retriever/
"""

from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class ToyRetriever(BaseRetriever):
    """A toy retriever that contains the top k documents that contain the user query.

    This retriever only implements the sync method _get_relevant_documents.

    If the retriever were to involve file access or network access, it could benefit
    from a native async implementation of `_aget_relevant_documents`.

    As usual, with Runnables, there's a default async implementation that's provided
    that delegates to the sync implementation running on another thread.
    """

    documents: List[Document]
    """List of documents to retrieve from."""
    k: int
    """Number of top results to return"""

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Sync implementations for retriever."""
        matching_documents = []
        for document in self.documents:
            if len(matching_documents) > self.k:
                return matching_documents

            if query.lower() in document.page_content.lower():
                matching_documents.append(document)
        return matching_documents

    # Optional: Provide a more efficient native implementation by overriding
    # _aget_relevant_documents
    # async def _aget_relevant_documents(
    #     self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
    # ) -> List[Document]:
    #     """Asynchronously get documents relevant to a query.

    #     Args:
    #         query: String to find relevant documents for
    #         run_manager: The callbacks handler to use

    #     Returns:
    #         List of relevant documents
    #     """


documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"type": "dog", "trait": "loyalty"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"type": "cat", "trait": "independence"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"type": "fish", "trait": "low maintenance"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"type": "bird", "trait": "intelligence"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"type": "rabbit", "trait": "social"},
    ),
]
retriever = ToyRetriever(documents=documents, k=3)

retriever.invoke("that")
async def test_ainvoke():
    result = await retriever.ainvoke("that")
    print(result)
asyncio.run(test_ainvoke())

retriever.batch(["dog", "cat"])

async def test_abatch():
    result = await retriever.abatch(["dog", "cat"])
    print(result)
asyncio.run(test_abatch())




