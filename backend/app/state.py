from typing import TypedDict, Dict, Any, Optional

class AgentState(TypedDict):
    user_input: Dict[str, Any]
    planner_output: Dict[str, Any]
    evidence: Dict[str, Any]

    # Output generation & evaluation
    draft_output: Dict[str, Any]
    evaluation: Optional[Dict[str, Any]]

    # Control fields for revision loop
    revision_count: int

    # Final accepted output
    final_report: Dict[str, Any]
