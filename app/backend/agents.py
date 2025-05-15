from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from tavily import AsyncTavilyClient
from .prompts import *


def build_agent_workflow(index, llm):
    # Define functions
    def retrieve_database(query: str) -> str:
        retriever = index.as_retriever(similarity_top_k=10, vector_store_query_mode="hybrid", alpha=0.5)
        nodes = retriever.retrieve(query)
        return "\n".join([f'{node.metadata["document"]}; {node.get_content()}' for node in nodes])

    async def search_web(query: str) -> str:
        client = AsyncTavilyClient()
        result = await client.search(query, max_results=5)
        return str(result)
    
    
    # Create tools from functions
    tool_search = FunctionTool.from_defaults(
        fn=search_web,
        name="search_web",
        description="Search the web for information"
    )
    
    tool_retrieve = FunctionTool.from_defaults(
        fn=retrieve_database,
        name="retrieve_database",
        description="Retrieve relevant documents from the database using the query"
    )
        
        
    # Create agents
    filter_agent = FunctionAgent(
        name="Filter_Agent",
        description="You are a query classifier. Your task is take action correspond to each user queries",
        llm=llm,
        system_prompt=system_prompt_filter_agent,
        tools=[],
        can_handoff_to=["Retrieve_Agent"]
    )

    retrieve_agent = FunctionAgent(
        name="Retrieve_Agent",
        description="You are consultant and responsible for answering user questions by using retrieve database",
        llm=llm,
        system_prompt=system_prompt_retrieve_agent,
        tools=[tool_retrieve],
        can_handoff_to=['Search_Agent']
    )

    search_agent = FunctionAgent(
        name="Search_Agent",
        description="You are consultant and responsible for answering user questions by searching web for external information",
        llm=llm,
        system_prompt=system_prompt_search_agent,
        tools=[tool_search],
        can_handoff_to=[]
    )


    multi_agents = AgentWorkflow(
        agents=[filter_agent, retrieve_agent, search_agent],
        root_agent="Filter_Agent",
    )

    return multi_agents
