from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from preprocessor import preprocess_email
from llm import analyze_chain
from state import AgentState
from dataset import log_feedback

def preprocess_node(state: AgentState) -> AgentState:
    """Node: Preprocess email text."""
    processed = preprocess_email(state["original_email"])
    return {"processed_email": processed}

def analyze_node(state: AgentState) -> AgentState:
    """Node: Single LLM call for classification + draft."""
    from config import SENTIMENTS, URGENCIES
    result = analyze_chain.invoke({
        "sentiments": SENTIMENTS,
        "urgencies": URGENCIES,
        "email": state["processed_email"]
    })
    return {"llm_output": result}

def hitl_node(state: AgentState) -> AgentState:
    """Node: Human-in-the-Loop review (interactive CLI)."""
    print(f"\n--- Email ID: {state['email_id']} ---")
    print(f"Original: {state['original_email'][:200]}...")  # Truncated
    print(f"LLM Analysis:")
    print(f"- Sentiment: {state['llm_output']['sentiment']}")
    print(f"- Urgency: {state['llm_output']['urgency']}")
    print(f"- Reasoning: {state['llm_output']['reasoning']}")
    print(f"- Draft: {state['llm_output']['draft_response'] or 'No draft (spam/no-reply)'}")

    # HITL Input
    approved = input("Approve draft? (y/n): ").lower() == 'y'
    corrected_sentiment = None
    corrected_urgency = None
    edited_draft = None

    if not approved:
        print("Corrections:")
        corr_sent = input(f"Correct sentiment? ({'/'.join(['positive', 'neutral', 'negative'])}) or Enter: ").strip()
        if corr_sent in ['positive', 'neutral', 'negative']:
            corrected_sentiment = corr_sent
        corr_urg = input(f"Correct urgency? ({'/'.join(['urgent', 'non-urgent', 'spam'])}) or Enter: ").strip()
        if corr_urg in ['urgent', 'non-urgent', 'spam']:
            corrected_urgency = corr_urg
        edit = input("Edited draft (or Enter to skip): ").strip()
        if edit:
            edited_draft = edit

    feedback = {
        "approved": approved,
        "corrected_sentiment": corrected_sentiment,
        "corrected_urgency": corrected_urgency,
        "edited_draft": edited_draft
    }
    # Log to dataset
    log_feedback(state["email_id"], state["llm_output"], feedback)

    # Update state with feedback (for potential retrain/few-shot)
    updated_output = state["llm_output"].copy()
    if corrected_sentiment:
        updated_output["sentiment"] = corrected_sentiment
    if corrected_urgency:
        updated_output["urgency"] = corrected_urgency
    if edited_draft:
        updated_output["draft_response"] = edited_draft

    return {"human_feedback": feedback, "llm_output": updated_output}

# Conditional edge: Always go to HITL for this demo (in prod, skip if high confidence)
def should_hitl(state: AgentState) -> str:
    return "hitl"  # Always for simplicity

# Build Graph
workflow = StateGraph(state_schema=AgentState)
workflow.add_node("preprocess", preprocess_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("hitl", hitl_node)

workflow.set_entry_point("preprocess")
workflow.add_edge("preprocess", "analyze")
workflow.add_conditional_edges("analyze", should_hitl, {"hitl": "hitl"})
workflow.add_edge("hitl", END)

app = workflow.compile()