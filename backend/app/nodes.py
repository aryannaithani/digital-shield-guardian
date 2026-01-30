from app.state import AgentState
from app.agents.planner import planner_agent_llm
from app.agents.gatherer import information_gathering_agent
from app.agents.generator import output_generator_agent
from app.agents.evaluator import evaluator_agent

MAX_REVISIONS = 2

def planner_node(state: AgentState) -> AgentState:
    state["planner_output"] = planner_agent_llm(state["user_input"])
    state["revision_count"] = 0
    state["evaluation"] = None
    return state


def gather_node(state: AgentState) -> AgentState:
    state["evidence"] = information_gathering_agent(state["planner_output"])
    return state


def generate_node(state: AgentState) -> AgentState:
    """
    Generate or revise draft output.
    If evaluator feedback exists, pass it to the generator.
    """
    feedback = None
    if state.get("evaluation") and state["evaluation"].get("verdict") == "revise":
        feedback = state["evaluation"]

    state["draft_output"] = output_generator_agent(
        state["evidence"],
        feedback=feedback
    )
    return state


def evaluate_node(state: AgentState) -> AgentState:
    """
    Evaluate the draft output.
    Decide accept vs revise.
    Increment revision counter on revise.
    """
    evaluation = evaluator_agent(
        state["evidence"],
        state["draft_output"]
    )

    state["evaluation"] = evaluation

    if evaluation["verdict"] == "accept":
        state["final_report"] = state["draft_output"]
    else:
        state["revision_count"] += 1

        # Force accept if max revisions reached
        if state["revision_count"] >= MAX_REVISIONS:
            state["final_report"] = state["draft_output"]

    return state
