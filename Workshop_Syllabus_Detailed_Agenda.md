# From Data to AI: Building an Intelligent Customer Support Application

**Detailed workshop agenda and learning plan**  
**Duration:** 3 hours (180 minutes)  
**Delivery:** Instructor demonstrations, guided Jupyter notebooks, team exercises, and project review  
**Optional extension:** 30–45 minutes for AI Agents with LangChain

## Teaching approach

Students work through **four progressive lab notebooks** and a closing demonstration. Each module introduces the key ideas, asks students to complete selected code or SQL placeholders, and ends with a visible result. The instructor provisions Supabase, access credentials, and starter data beforehand. Students use **Google Colab** or local Jupyter, so no Docker or local PostgreSQL instance is required.

The project context is a **Customer Support Intelligence Platform**. The ticket dataset comes from Kaggle and is used for educational analytics; a separate, curated support knowledge base powers the RAG exercises.

## Session 1 — Data Engineering & SQL Fundamentals

**Duration:** 45 minutes  
**Lab:** `01_data_etl_sql.ipynb`

**Students learn**
- How a raw dataset becomes reliable, queryable information through ETL.
- The purpose of schemas, keys, relationships, and appropriate data types in relational databases.
- How SQL filtering, joins, grouping, and aggregations answer operational questions.

**Hands-on activities**
- Inspect customer support ticket records and identify missing or inconsistent values.
- Complete guided Pandas transformations and validate the cleaned data.
- Load results into a team-specific PostgreSQL schema on Supabase.
- Inspect prepared DDL and write SQL queries for ticket volume, issue types, and resolution patterns.

**Checkpoint / outcome:** A repeatable small ETL process, populated team table, and working SQL queries that summarize customer support operations.

## Session 2 — Data Analytics & Interactive Dashboard

**Duration:** 25 minutes  
**Lab:** `02_dashboard_in_notebook.ipynb`

**Students learn**
- How to translate business questions into meaningful key performance indicators (KPIs).
- How to aggregate data consistently and choose suitable chart types.
- How interactive visualization supports exploration and comparison.

**Hands-on activities**
- Query team data from PostgreSQL and calculate ticket-related KPIs.
- Create Plotly charts for category volume, priority distribution, and selected response/resolution indicators.
- Interpret results and identify one potential operational improvement.

**Checkpoint / outcome:** An interactive, database-backed dashboard inside Jupyter or Colab.

## Session 3 — OpenAI Embeddings, Vector Search & RAG

**Duration:** 50 minutes  
**Lab:** `03_embeddings_rag_openai.ipynb`

**Students learn**
- The difference between relational queries and semantic document retrieval.
- How text embeddings represent meaning as vectors, and how pgvector supports similarity search.
- How retrieval-augmented generation (RAG) supplies contextual evidence to an LLM and why source grounding matters.

**Hands-on activities**
- Generate embeddings for a sample knowledge article using the OpenAI API.
- Store or inspect vectors in Supabase PostgreSQL with pgvector.
- Complete a top-k semantic-search query to retrieve relevant articles.
- Pass retrieved article content to an OpenAI model, requesting source-referenced answers.
- Test a question that is not addressed by the knowledge base and observe the system's limitations.

**Checkpoint / outcome:** A guided question-answering pipeline with embedding, vector retrieval, and a grounded LLM response.

## Session 4 — Streamlit: Integrating Analytics and AI

**Duration:** 40 minutes  
**Lab:** `04_streamlit_app.ipynb` and a prewritten Streamlit template

**Students learn**
- How a lightweight web interface connects to structured data and AI services.
- How to organize a prototype into data retrieval, analysis, presentation, and AI interaction components.
- The difference between notebook experimentation and application delivery.

**Hands-on activities**
- Examine and customize a provided Streamlit application.
- Connect the dashboard view to PostgreSQL-backed metrics.
- Connect an AI chat view to the existing RAG workflow.
- Test the application with several support questions; inspect the displayed data and cited sources.

**Checkpoint / outcome:** A functional application prototype combining interactive analytics and an AI support assistant. The instructor can host the final Streamlit demonstration to avoid requiring individual student deployments.

## Session 5 — Project Demonstration & Review

**Duration:** 20 minutes

**Activities**
- Walk through the completed application and the end-to-end data flow.
- Compare questions best answered by SQL with those better suited to document retrieval and RAG.
- Discuss data quality, AI reliability, source attribution, and practical next steps.
- Student demonstrations, questions, and feedback.

**Checkpoint / outcome:** Students can explain the roles of ETL, PostgreSQL, dashboards, embeddings, retrieval, and LLMs in the complete workflow.

## Optional bonus — AI Agents & Tool Calling with LangChain

**Duration:** Additional 30–45 minutes  
**Lab:** `05_bonus_langchain_agent.ipynb`

**Students learn**
- How an AI agent differs from a basic LLM prompt or fixed RAG pipeline.
- How tool calling lets a model choose from predefined, constrained actions.
- Why permission boundaries and validation matter when an AI system accesses external data.

**Hands-on activities**
- Explore an agent built with LangChain.
- Connect two predefined tools: SQL-based support analytics and the existing RAG retriever.
- Test different questions and observe tool selection, evidence retrieval, and final answers.

**Checkpoint / outcome:** An introductory agent that routes appropriate questions to analytics or knowledge retrieval tools. This is a bonus and not required for core workshop completion.

## Learning requirements and assessment

**Recommended preparation:** Basic Python skills and introductory familiarity with SQL. No prior AI, Supabase, or Streamlit experience is necessary.

**Technical setup:** Student laptop, internet access, browser, and Google Colab or local Jupyter. Instructor manages Supabase PostgreSQL/pgvector, database access, dataset preparation, and OpenAI access arrangements. No student-side Docker or database installation is needed.

**Assessment approach:** Informal, practical checkpoints after each module rather than a formal exam. Successful participation is demonstrated by transformed records, working queries, charts, an RAG response with source references, and participation in the final application review.

## Timing summary

| Core session | Minutes |
|---|---:|
| 1. Data Engineering & SQL | 45 |
| 2. Dashboard | 25 |
| 3. Embeddings & RAG | 50 |
| 4. Streamlit Application | 40 |
| 5. Demonstration & Review | 20 |
| **Total** | **180** |

*The optional LangChain agent lab adds 30–45 minutes beyond the core three-hour workshop.*
