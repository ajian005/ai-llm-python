import asyncio
from LangGraph.LangGraphAppDir.my_LangGraph_App_001.src.agent.graph import graph

async def main():
    try:
        result = await graph.ainvoke({'changeme': 'test'})
        print(f"Test successful! Result: {result}")
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())