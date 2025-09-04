"""
    Run a local server : https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/
"""

"""
    Prerequisites
      An API key for LangSmith - free to sign up
"""

"""
    1. Install the LangGraph CLI
        # Python >= 3.11 is required.
        # pip install --upgrade "langgraph-cli[inmem]"
"""

"""
    2. Create a LangGraph app
    langgraph new path/to/your/app --template new-langgraph-project-python
    example: langgraph new ./my-LangGraph-App-001 --template new-langgraph-project-python
"""

"""
    3. Install dependencies
    cd path/to/your/app
    pip install -e .
"""


"""
    4. Create a .env file
    LANGSMITH_API_KEY=lsv2...
"""

"""
    5. Launch LangGraph Server
    langgraph dev
"""

"""
    6. Test your application in LangGraph Studio
"""

"""
    7. Test the API
      7.1 Python SDK(async)
      7.2 Python SDK(sync)
      7.3 Rest API
"""