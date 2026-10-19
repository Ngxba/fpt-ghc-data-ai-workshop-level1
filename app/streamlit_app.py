# Support Intelligence — instructor-hosted Streamlit app
# Use one read-only DB login (lab_app_viewer) to view all team schemas.
# For students running locally, a team login works when LAB_TEAM_SCHEMAS lists only that team.
import os
import re
from contextlib import closing
import pandas as pd
import plotly.express as px
import psycopg
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Support Intelligence", page_icon="🎫", layout="wide")

DB_URL = os.getenv("LAB_APP_DATABASE_URL", "")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
TEAM_SCHEMAS = [x.strip() for x in os.getenv("LAB_TEAM_SCHEMAS", "team_01").split(",")]
TEAM_SCHEMAS = [x for x in TEAM_SCHEMAS if re.fullmatch(r"team_[0-9]{2}", x)]
if not TEAM_SCHEMAS:
    st.error("Set LAB_TEAM_SCHEMAS=team_01 (or a comma-delimited list).")
    st.stop()
if not DB_URL:
    st.error("Set LAB_APP_DATABASE_URL to an app-viewer/team PostgreSQL transaction pooler URL.")
    st.stop()

st.markdown("""<style>
.block-container {padding-top: 1.7rem; padding-bottom: 2rem;}
div[data-testid="stMetric"] {background: rgba(120,130,150,.09); border: 1px solid rgba(150,150,150,.18); border-radius: 12px; padding: 15px;}
</style>""", unsafe_allow_html=True)

@st.cache_data(ttl=40, show_spinner=False)
def select_df(query, params=()):
    with closing(psycopg.connect(DB_URL, sslmode="require", connect_timeout=12, prepare_threshold=None)) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return pd.DataFrame(cur.fetchall(), columns=[col.name for col in cur.description])

def embed(text):
    if not OPENAI_KEY:
        raise RuntimeError("Instructor must configure OPENAI_API_KEY on Streamlit server.")
    return OpenAI(api_key=OPENAI_KEY).embeddings.create(model="text-embedding-3-small",input=text).data[0].embedding

def vector_literal(values):
    assert len(values)==1536
    return "["+",".join(str(float(x)) for x in values)+"]"

def rag_answer(question, team):
    vector = vector_literal(embed(question))
    articles = select_df(f"""SELECT article_id,title,content,
          1-(embedding <=> %s::extensions.vector) AS similarity
        FROM (SELECT article_id,title,content,embedding FROM shared.knowledge_articles
              UNION ALL SELECT article_id,title,content,embedding FROM {team}.knowledge_articles) kb
        ORDER BY embedding <=> %s::extensions.vector LIMIT 3""",(vector,vector))
    ctx = "\n\n".join(f"[{r.article_id}] {r.title}: {r.content}" for r in articles.itertuples())
    answer = OpenAI(api_key=OPENAI_KEY).responses.create(
        model="gpt-4.1-mini",
        input=[
          {"role":"system","content":"Answer ONLY using the provided knowledge articles. Cite article IDs such as [KB-001]. If unsupported, say you do not know. Never invent company policies."},
          {"role":"user","content":f"Question: {question}\n\nKnowledge articles:\n{ctx}"},
        ],
    ).output_text
    return answer,articles

with st.sidebar:
    st.title("🎫 Support Intelligence")
    st.caption("Supabase · OpenAI · pgvector")
    team=st.selectbox("Student team", TEAM_SCHEMAS)
    st.markdown("---")
    st.info("Metrics are calculated from synthetic Kaggle tickets. This is an educational demonstration, not a live support system.")
    if st.button("Refresh database"):
        select_df.clear()
        st.rerun()

st.title("Customer Support Intelligence")
st.caption("Explore structured SQL analytics and grounded knowledge search in one application.")
tab_data, tab_ai, tab_docs = st.tabs(["📊 Dashboard", "💬 AI Support", "📚 Data & methodology"])

try:
    base=select_df(f"""SELECT ticket_id,ticket_type,status,priority,channel,product,
           satisfaction_rating,response_to_resolution_hours,first_response_at
         FROM {team}.clean_tickets""")
except Exception as exc:
    st.error("Cannot read team table. Run the ETL notebook first and verify this account has SELECT access.")
    st.exception(exc)
    st.stop()

with tab_data:
    if base.empty:
        st.warning("No cleaned rows. Complete notebook 1 then press Refresh database.")
    else:
        t1,t2=st.columns(2)
        with t1:
            type_filter=st.multiselect("Ticket type", sorted(base.ticket_type.dropna().unique().tolist()),
                                       default=sorted(base.ticket_type.dropna().unique().tolist()))
        with t2:
            channels=sorted(base.channel.dropna().unique().tolist())
            channel_filter=st.multiselect("Channel",channels,default=channels)
        data=base[base.ticket_type.isin(type_filter) & base.channel.isin(channel_filter)].copy()
        total=len(data)
        closed=int(data.status.eq("Closed").sum())
        avg_csat=data.satisfaction_rating.astype(float).mean()
        avg_hours=data.response_to_resolution_hours.astype(float).mean()
        a,b,c,d=st.columns(4)
        a.metric("Tickets",f"{total:,}")
        b.metric("Closed rate",f"{100*closed/total:.1f}%" if total else "—")
        c.metric("Avg satisfaction",f"{avg_csat:.2f}/5" if pd.notna(avg_csat) else "—")
        d.metric("Response → resolution",f"{avg_hours:.1f} h" if pd.notna(avg_hours) else "—")
        st.caption("Response → resolution is inferred from two Kaggle timestamps; it is NOT official SLA time.")
        if not data.empty:
            chart1,chart2=st.columns(2)
            types=data.groupby("ticket_type",dropna=False).size().reset_index(name="tickets")
            with chart1:
                st.plotly_chart(px.bar(types,x="ticket_type",y="tickets",title="Volume by issue type",text_auto=True),use_container_width=True)
            with chart2:
                priorities=data.groupby("priority",dropna=False).size().reset_index(name="tickets")
                st.plotly_chart(px.pie(priorities,names="priority",values="tickets",hole=.55,title="Priority mix"),use_container_width=True)
            st.subheader("Explore the records")
            st.dataframe(data.sort_values("ticket_id").head(150),use_container_width=True,hide_index=True)
        else:
            st.info("No tickets match these filters.")

with tab_ai:
    st.subheader("Grounded support assistant")
    st.write("Ask about billing, refunds, device setup, cancellations, or troubleshooting. Answers cite retrieved KB IDs.")
    if not OPENAI_KEY:
        st.warning("The instructor has not configured OPENAI_API_KEY on the Streamlit host. Dashboard works, but AI is disabled.")
    if "conversation" not in st.session_state or st.session_state.get("conversation_team") != team:
        st.session_state.conversation=[]
        st.session_state.conversation_team=team
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption("Retrieved KB IDs: "+", ".join(msg["sources"]))
    prompt=st.chat_input("Ask a question about support procedures...",disabled=not bool(OPENAI_KEY),max_chars=800)
    if prompt:
        st.session_state.conversation.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Retrieving articles and generating answer..."):
                    answer,articles=rag_answer(prompt,team)
                st.markdown(answer)
                sources=articles.article_id.tolist()
                st.caption("Retrieved KB IDs: "+", ".join(sources))
                st.session_state.conversation.append({"role":"assistant","content":answer,"sources":sources})
            except Exception as exc:
                st.error("AI request failed. Confirm OpenAI budget/credentials and database connectivity.")
                st.caption(str(exc)[:250])

with tab_docs:
    st.markdown("""### Under the hood
1. Kaggle CSV is downloaded and sanitized by the instructor.
2. Student notebook 1 cleans and loads a dedicated `team_NN.clean_tickets` table.
3. The dashboard uses SQL-backed ticket data with Pandas/Plotly.
4. A separate, fictional knowledge base is embedded with `text-embedding-3-small` and stored in `pgvector`.
5. Semantic search retrieves the top 3 articles and the OpenAI LLM answers from their text.

**Limitations:** Kaggle tickets are synthetic; missing resolution times are null; response-to-resolution is not SLA compliance. LLM-generated answers require human validation. This app is for workshop demonstrations—not a public production deployment.
""")
    st.code(f"SELECT COUNT(*) FROM {team}.clean_tickets;",language="sql")
