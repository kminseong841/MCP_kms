from langchain_core.runnables.base import Runnable
from langgraph.graph import MessagesState
from typing import Callable

def CallModelNode(model_with_tools: Runnable) -> Callable[[MessagesState], dict]:
    def call_model(state: MessagesState) -> dict:
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    return call_model