import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

def classify_email(email: dict) -> dict:
    """
    Agent 1: Classifies email into category
    with confidence score.
    """
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    
    prompt = PromptTemplate(
        template="""You are an email classifier for an energy company.

Classify the following email into EXACTLY ONE of these categories:
- Billing (bill disputes, incorrect charges, billing questions)
- Metering (meter readings, meter issues)
- Prepayment (top up issues, prepayment meter problems)
- Account Management (moving house, account changes)
- Power Outage (no electricity, power cuts)
- Tariff Enquiry (switching tariffs, green energy, pricing)
- Payment (direct debits, payment methods)
- Smart Meter (smart meter installation, smart meter issues)
- Other (does not fit any category above)

Email Subject: {subject}
Email Body: {body}

Respond in JSON format only:
{{
    "category": "the category name",
    "confidence": 95,
    "reason": "one sentence explaining why"
}}""",
        input_variables=["subject", "body"]
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "subject": email["subject"],
        "body": email["body"]
    })
    
    # Parse JSON response
    try:
        parsed = json.loads(result.content.strip())
        category = parsed["category"]
        confidence = parsed["confidence"]
        reason = parsed["reason"]
    except:
        # Fallback if JSON parsing fails
        category = result.content.strip()
        confidence = 50
        reason = "Could not determine confidence"
    
    # Flag low confidence for human review
    needs_human_review = confidence < 70
    
    print(f"Email {email['id']}: '{email['subject']}'")
    print(f"→ {category} ({confidence}% confident)")
    if needs_human_review:
        print(f"⚠️  LOW CONFIDENCE — flagged for human review!")
    
    return {
        **email,
        "category": category,
        "confidence": confidence,
        "reason": reason,
        "needs_human_review": needs_human_review
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from data.sample_emails import SAMPLE_EMAILS
    
    print("Testing classifier with confidence scores...")
    print("="*60)
    for email in SAMPLE_EMAILS:
        result = classify_email(email)
        print(f"Reason: {result['reason']}")
        print("-"*40)
