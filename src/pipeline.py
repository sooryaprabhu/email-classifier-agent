import os
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from src.classifier import classify_email
from src.retriever import retrieve_relevant_articles, setup_knowledge_base
from src.responder import generate_response

load_dotenv()

class EmailState(TypedDict):
    id: str
    email_from: str
    subject: str
    body: str
    category: str
    confidence: int
    reason: str
    needs_human_review: bool
    relevant_articles: List[Dict]
    draft_reply: str
    status: str

def classification_node(state: EmailState) -> EmailState:
    print(f"\n🔍 Agent 1: Classifying email...")
    email = {
        "id": state["id"],
        "from": state["email_from"],
        "subject": state["subject"],
        "body": state["body"]
    }
    result = classify_email(email)
    return {
        **state,
        "category": result["category"],
        "confidence": result["confidence"],
        "reason": result["reason"],
        "needs_human_review": result["needs_human_review"],
        "status": "classified"
    }

def retrieval_node(state: EmailState) -> EmailState:
    print(f"\n📚 Agent 2: Retrieving relevant articles...")
    vector_store = setup_knowledge_base()
    email = {
        "id": state["id"],
        "from": state["email_from"],
        "subject": state["subject"],
        "body": state["body"],
        "category": state["category"]
    }
    result = retrieve_relevant_articles(email, vector_store)
    return {
        **state,
        "relevant_articles": result["relevant_articles"],
        "status": "retrieved"
    }

def response_node(state: EmailState) -> EmailState:
    print(f"\n✍️ Agent 3: Generating draft reply...")
    email = {
        "id": state["id"],
        "from": state["email_from"],
        "subject": state["subject"],
        "body": state["body"],
        "category": state["category"],
        "relevant_articles": state["relevant_articles"]
    }
    result = generate_response(email)
    return {
        **state,
        "draft_reply": result["draft_reply"],
        "status": "completed"
    }

def build_pipeline():
    graph = StateGraph(EmailState)
    graph.add_node("classify", classification_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("respond", response_node)
    graph.set_entry_point("classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", END)
    return graph.compile()

def process_email(email: dict) -> dict:
    pipeline = build_pipeline()
    initial_state = EmailState(
        id=email.get("id", "001"),
        email_from=email.get("from", "customer@email.com"),
        subject=email["subject"],
        body=email["body"],
        category="",
        confidence=0,
        reason="",
        needs_human_review=False,
        relevant_articles=[],
        draft_reply="",
        status="pending"
    )
    result = pipeline.invoke(initial_state)
    return result


if __name__ == "__main__":
    from data.sample_emails import SAMPLE_EMAILS
    print("🚀 Testing pipeline with confidence scores")
    print("="*60)
    for email in SAMPLE_EMAILS[:3]:
        print(f"\n📧 Processing: {email['subject']}")
        result = process_email(email)
        print(f"Category: {result['category']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Needs Review: {result['needs_human_review']}")
        print(f"Reason: {result['reason']}")
        print("="*60)
