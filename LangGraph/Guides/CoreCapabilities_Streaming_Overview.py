"""
    Streaming : https://langchain-ai.github.io/langgraph/concepts/streaming/

    Streaming
        LangGraph implements a streaming system to surface real-time updates, allowing for responsive and transparent user experiences.

        LangGraph’s streaming system lets you surface live feedback from graph runs to your app.
        There are three main categories of data you can stream:

        Workflow progress — get state updates after each graph node is executed.
        LLM tokens — stream language model tokens as they’re generated.
        Custom updates — emit user-defined signals (e.g., “Fetched 10/100 records”).


        What’s possible with LangGraph streaming¶
        Stream LLM tokens — capture token streams from anywhere: inside nodes, subgraphs, or tools.
        Emit progress notifications from tools — send custom updates or progress signals directly from tool functions.
        Stream from subgraphs — include outputs from both the parent graph and any nested subgraphs.
        Use any LLM — stream tokens from any LLM, even if it's not a LangChain model using the custom streaming mode.
        Use multiple streaming modes — choose from values (full state), updates (state deltas), messages (LLM tokens + metadata), custom (arbitrary user data), or debug (detailed traces).

"""