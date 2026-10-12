import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from pinecone import Pinecone, ServerlessSpec
import time
import sys
sys.path.insert(0, '.')

load_dotenv()

def setup_knowledge_base():
    """
    Load knowledge base articles into Pinecone.
    This only needs to run once.
    """
    from data.knowledge_base import KNOWLEDGE_BASE
    
    pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
    index_name = "email-classifier-agent"
    
    # Create index if it doesn't exist
    if index_name not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"Created Pinecone index: {index_name}")
        time.sleep(5)
    else:
        print(f"Using existing index: {index_name}")
    
    # Convert knowledge base to documents
    documents = []
    for article in KNOWLEDGE_BASE:
        doc = Document(
            page_content=article["content"],
            metadata={
                "id": article["id"],
                "category": article["category"],
                "title": article["title"]
            }
        )
        documents.append(doc)
    
    # Store in Pinecone
    embeddings = OpenAIEmbeddings(
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=os.environ.get('PINECONE_API_KEY')
    )
    
    vector_store.add_documents(documents)
    print(f"Stored {len(documents)} articles in Pinecone!")
    
    return vector_store


def retrieve_relevant_articles(email: dict, vector_store) -> dict:
    """
    Agent 2: Takes classified email and finds relevant knowledge base articles.
    """
    
    # Search for relevant articles using email content
    query = f"{email['subject']} {email['body']}"
    
    results = vector_store.similarity_search(
        query,
        k=2  # Get top 2 most relevant articles
    )
    
    articles = []
    for doc in results:
        articles.append({
            "title": doc.metadata["title"],
            "category": doc.metadata["category"],
            "content": doc.page_content
        })
        print(f"Found article: {doc.metadata['title']}")
    
    return {
        **email,
        "relevant_articles": articles
    }


if __name__ == "__main__":
    print("Setting up knowledge base...")
    vector_store = setup_knowledge_base()
    
    print("\nTesting retrieval...")
    from data.sample_emails import SAMPLE_EMAILS
    from src.classifier import classify_email
    
    # Test with first email
    email = SAMPLE_EMAILS[0]
    classified = classify_email(email)
    result = retrieve_relevant_articles(classified, vector_store)
    
    print(f"\nEmail: {result['subject']}")
    print(f"Category: {result['category']}")
    print(f"Relevant articles found: {len(result['relevant_articles'])}")
    for article in result['relevant_articles']:
        print(f"  → {article['title']}")
