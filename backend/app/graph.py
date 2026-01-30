from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import (
    planner_node,
    gather_node,
    generate_node,
    evaluate_node,
)

graph = StateGraph(AgentState)

# Nodes
graph.add_node("planner", planner_node)
graph.add_node("gather", gather_node)
graph.add_node("generate", generate_node)
graph.add_node("evaluate", evaluate_node)

# Entry point
graph.set_entry_point("planner")

# Linear flow up to evaluation
graph.add_edge("planner", "gather")
graph.add_edge("gather", "generate")
graph.add_edge("generate", "evaluate")

# Conditional routing after evaluation
def evaluation_router(state: AgentState) -> str:
    if state.get("final_report"):
        return END
    return "generate"

graph.add_conditional_edges(
    "evaluate",
    evaluation_router,
    {
        "generate": "generate",
        END: END
    }
)

app = graph.compile()
