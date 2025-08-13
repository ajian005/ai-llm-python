import langgraph

print(f"Langgraph version: {langgraph.__version__}")

try:
    from langgraph.prebuilt import create_react_agent
    print("Successfully imported create_react_agent from langgraph.prebuilt")
except ImportError as e:
    print(f"Import error: {e}")