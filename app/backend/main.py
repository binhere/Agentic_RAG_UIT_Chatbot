# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.agent.workflow import ToolCallResult, AgentStream, AgentInput
from .agents import build_agent_workflow
from .utils import get_index, get_llm

# Define the input schema
class Query(BaseModel):
    query: str
    
app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize index, LLM, and agents
index = get_index()
llm = get_llm()
multi_agents = build_agent_workflow(index, llm)
memory = ChatMemoryBuffer.from_defaults(token_limit=40000) 

# Chat API
@app.post("/chat")
async def chat(input: Query):
    user_msg = input.query
    handler = multi_agents.run(user_msg, stream=True, memory=memory)

    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            print("\nTool called:", event.tool_name)
            print("\nArguments to the tool:", event.tool_kwargs)
            print("\nTool output:\n", event.tool_output)
        elif isinstance(event, AgentStream):
            print(event.delta, end="", flush=True)
        elif isinstance(event, AgentInput):
            print(f"\nAgent name: {event.current_agent_name}")

    final_response = await handler
    return {"server_response": final_response}


# Runs FastAPI directly if this file is executed without typing command manually
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
