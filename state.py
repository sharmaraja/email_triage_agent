from typing import TypedDict, Annotated, Sequence
from langgraph.graph import add_messages, StateGraph

class AgentState(TypedDict):
    email_id: int
    original_email: str
    processed_email: str
    llm_output: dict  # JSON: {'sentiment', 'urgency', 'reasoning', 'draft_response'}
    human_feedback: dict  # {'approved': bool, 'corrected_sentiment': str|None, 'corrected_urgency': str|None, 'edited_draft': str|None}
    messages: Annotated[Sequence, add_messages]  # For LangGraph tracing (optional)