import streamlit as st
import sys
import os
sys.path.insert(0, '.')
from dotenv import load_dotenv
from src.pipeline import process_email
from src.retriever import setup_knowledge_base
from data.sample_emails import SAMPLE_EMAILS

load_dotenv()

st.set_page_config(
    page_title="Email Intelligence System",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Intelligence System")
st.markdown("*Powered by Multi-Agent AI — Classify → Retrieve → Respond*")
st.divider()

with st.sidebar:
    st.header("⚙️ System Info")
    st.success("✅ Agent 1: Email Classifier")
    st.success("✅ Agent 2: Knowledge Retriever")
    st.success("✅ Agent 3: Response Generator")
    st.divider()
    st.markdown("**Confidence Threshold**")
    threshold = st.slider(
        "Flag for human review below:",
        min_value=50,
        max_value=90,
        value=70,
        step=5,
        help="Emails below this confidence are flagged"
    )
    st.divider()
    st.markdown("**Built by Soorya Prabhu**")
    st.markdown("MSc AI, Brunel University London")
    st.markdown("LangGraph + Pinecone + OpenAI")

if "results" not in st.session_state:
    st.session_state.results = []
if "vector_store" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        st.session_state.vector_store = setup_knowledge_base()
    st.success("Knowledge base loaded!")

st.subheader("📨 Process an Email")

col1, col2 = st.columns(2)

with col1:
    input_method = st.radio(
        "Choose input method:",
        ["Use sample email", "Write your own email"]
    )

with col2:
    if input_method == "Use sample email":
        sample_options = {
            f"{e['id']}: {e['subject']}": e
            for e in SAMPLE_EMAILS
        }
        selected = st.selectbox(
            "Select a sample email:",
            list(sample_options.keys())
        )
        selected_email = sample_options[selected]

if input_method == "Use sample email":
    email_from = selected_email["from"]
    subject = selected_email["subject"]
    body = selected_email["body"]
    st.text_input("From:", value=email_from, disabled=True)
    st.text_input("Subject:", value=subject, disabled=True)
    st.text_area("Email body:", value=body, height=100, disabled=True)
else:
    email_from = st.text_input("From:", placeholder="customer@email.com")
    subject = st.text_input("Subject:", placeholder="Enter email subject")
    body = st.text_area("Email body:", placeholder="Enter email content here...", height=150)

st.divider()

if st.button("🚀 Process Email", type="primary"):
    if subject and body:
        with st.spinner("Processing through multi-agent pipeline..."):
            email = {
                "id": "custom-001",
                "from": email_from,
                "subject": subject,
                "body": body
            }
            result = process_email(email)

        st.success("✅ Pipeline Complete!")

        # Show confidence with colour coding
        confidence = result.get("confidence", 0)
        needs_review = result.get("needs_human_review", False)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Category", result["category"])
        with col2:
            if confidence >= 70:
                st.metric("Confidence", f"{confidence}% ✅")
            else:
                st.metric("Confidence", f"{confidence}% ⚠️")
        with col3:
            st.metric("Articles Found", len(result["relevant_articles"]))
        with col4:
            if needs_review:
                st.metric("Status", "⚠️ Review Needed")
            else:
                st.metric("Status", "✅ Ready")

        # Warning banner for low confidence
        if needs_review:
            st.warning(
                f"⚠️ **Low confidence ({confidence}%)** — "
                f"This email has been flagged for human review. "
                f"Reason: {result.get('reason', 'Uncertain classification')}"
            )
        else:
            st.info(
                f"💡 Classification reason: {result.get('reason', '')}"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📧 Original Email")
            st.write(f"**From:** {result['email_from']}")
            st.write(f"**Subject:** {result['subject']}")
            st.write(f"**Category:** 🏷️ {result['category']}")
            st.write(f"**Confidence:** {confidence}%")
            st.text_area(
                "Email body:",
                value=result["body"],
                height=150,
                disabled=True
            )

            st.subheader("📚 Knowledge Base Articles Used")
            for article in result["relevant_articles"]:
                with st.expander(f"📄 {article['title']}"):
                    st.write(article["content"])

        with col2:
            st.subheader("✍️ AI Draft Reply")
            st.text_area(
                "Draft reply (human reviews before sending):",
                value=result["draft_reply"],
                height=300
            )

            if needs_review:
                st.error("⚠️ Low confidence — please review carefully!")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.button("✅ Send Reply", type="primary")
            with col_b:
                st.button("✏️ Edit Reply")
            with col_c:
                st.button("❌ Reject")

            st.info(
                "👤 Human reviews and approves before sending. "
                "This ensures accountability and quality control."
            )

        st.session_state.results.append(result)

    else:
        st.error("Please enter a subject and email body!")

if st.session_state.results:
    st.divider()
    st.subheader(f"📊 Processed Today: {len(st.session_state.results)} emails")

    for i, r in enumerate(st.session_state.results):
        conf = r.get('confidence', 0)
        flag = "⚠️" if r.get('needs_human_review') else "✅"
        with st.expander(
            f"{flag} Email {i+1}: {r['subject']} → "
            f"{r['category']} ({conf}%)"
        ):
            st.write(f"**From:** {r['email_from']}")
            st.write(f"**Category:** {r['category']}")
            st.write(f"**Confidence:** {conf}%")
            st.write(f"**Draft:** {r['draft_reply'][:100]}...")

st.divider()
st.markdown(
    "Built by **Soorya Prabhu** | "
    "MSc AI, Brunel University London | "
    "LangGraph + Pinecone + OpenAI"
)
