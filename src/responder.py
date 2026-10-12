import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

def generate_response(email: dict) -> dict:
    """
    Agent 3: Takes classified email + relevant articles
    and generates a professional draft reply.
    """
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    
    # Build context from retrieved articles
    articles_context = ""
    for article in email.get("relevant_articles", []):
        articles_context += f"\n---\n{article['title']}:\n{article['content']}\n"
    
    prompt = PromptTemplate(
        template="""You are a professional customer service agent 
for an energy company.

Using ONLY the information in the knowledge base articles below,
write a helpful and professional reply to this customer email.

Always:
- Address the customer by name if available
- Be empathetic and professional
- Give specific steps or information from the knowledge base
- End with an offer to help further
- Keep the reply concise (max 150 words)

CUSTOMER EMAIL:
From: {email_from}
Subject: {subject}
Message: {body}

KNOWLEDGE BASE ARTICLES:
{articles_context}

Write the draft reply below:
Draft Reply:""",
        input_variables=["email_from", "subject", "body", "articles_context"]
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "email_from": email.get("from", "Customer"),
        "subject": email["subject"],
        "body": email["body"],
        "articles_context": articles_context
    })
    
    draft_reply = result.content.strip()
    
    return {
        **email,
        "draft_reply": draft_reply
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from data.sample_emails import SAMPLE_EMAILS
    from src.classifier import classify_email
    from src.retriever import setup_knowledge_base, retrieve_relevant_articles
    
    print("Setting up...")
    vector_store = setup_knowledge_base()
    
    print("\nTesting full pipeline on first email...")
    print("="*60)
    
    email = SAMPLE_EMAILS[0]
    
    # Agent 1: Classify
    classified = classify_email(email)
    
    # Agent 2: Retrieve
    retrieved = retrieve_relevant_articles(classified, vector_store)
    
    # Agent 3: Generate response
    final = generate_response(retrieved)
    
    print(f"\nORIGINAL EMAIL:")
    print(f"From: {final['from']}")
    print(f"Subject: {final['subject']}")
    print(f"Body: {final['body']}")
    print(f"\nCATEGORY: {final['category']}")
    print(f"\nDRAFT REPLY:")
    print(f"{final['draft_reply']}")
    print("="*60)
