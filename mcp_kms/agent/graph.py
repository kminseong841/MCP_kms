from typing import Dict, Optional
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.typing import StateT, ContextT, InputT, OutputT
from typing import Callable


def build_graph(
        nodes: Dict[str, Callable], 
        edges: Dict[str, str], 
        conditional_edges: Optional[Dict[str, Callable]]) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]:
    builder = StateGraph(MessagesState)

    # 1) add node
    for node_info in nodes.keys():
        action = nodes[node_info]
        builder.add_node(node_info, action)
    # 2) add edge
    for start_node in edges.keys():
        end_node = edges[start_node]
        builder.add_edge(start_node, end_node)
    # 3) add condtional edge
    for start_node in conditional_edges.keys():
        path_func = conditional_edges[start_node]
        builder.add_conditional_edges(source=start_node, path=path_func)

    graph = builder.compile()
    return graph

