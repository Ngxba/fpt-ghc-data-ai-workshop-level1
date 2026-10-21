# From Data to AI: Building an Intelligent Customer Support Application

**Workshop syllabus | High-level overview**

| Item | Details |
|---|---|
| **Duration** | 3 hours (180 minutes) |
| **Format** | Instructor-led, hands-on workshop using guided Jupyter notebooks |
| **Audience** | University students in Computer Science, IT, Data Science, Software Engineering, and related disciplines |
| **Level** | Beginner to intermediate |
| **Optional extension** | 30–45 minutes: Introduction to AI Agents with LangChain |

## Workshop overview

This project-based workshop introduces students to the practical connections between **relational databases, data engineering, analytics, and generative AI**. Students work toward a **Customer Support Intelligence Platform**: a prototype that transforms customer support ticket data into business insights and answers support questions using an external knowledge base.

Instead of configuring infrastructure from scratch, participants complete short, guided programming exercises that progressively build on one another. The instructor prepares the shared database, dataset, application template, and access details in advance.

**Notebooks that teach, not just test.** Each lab is a step-by-step walkthrough: every step explains what the code does, why it is needed, and what students should see. About 40 diagrams (data flows, annotated charts, flow charts, architecture and sequence diagrams) are built into the notebooks, and each lab ends with a recap and discussion questions. Students complete short coding tasks with hints; full solutions are kept separately for the instructor.

## Learning objectives

By the end of the workshop, students should be able to:

1. Explain a simple extract-transform-load (ETL) workflow and apply core data-cleaning steps using Python and Pandas, keeping missing values missing.
2. Explore a relational schema and use SQL joins, filters, and aggregations to answer business questions.
3. Visualize database-backed metrics using interactive charts, and state a finding together with its caveat.
4. Explain vectors, embeddings, vector databases, similarity search, and retrieval-augmented generation (RAG), and implement a guided RAG workflow.
5. Connect analytics and AI capabilities in a Streamlit application prototype, and explain how it differs from a notebook.
6. *(Optional extension)* Explain how an AI agent chooses between predefined tools, and why guardrails matter.

## Agenda

| Time | Session | Main activity |
|---|---|---|
| **45 min** | **1. Data Engineering & SQL** | Explore the Kaggle customer support dataset; extract, clean, and load team data into PostgreSQL; query with SQL joins and aggregates. |
| **25 min** | **2. Analytics & Dashboard** | Define practical support metrics and build interactive Plotly charts (KPIs, bubble chart, sunburst, box plot, heatmap) in Jupyter. |
| **50 min** | **3. Embeddings & RAG** | Learn what vectors and vector databases are; generate OpenAI embeddings; store and search vectors with pgvector; use retrieved articles to ground LLM answers. |
| **40 min** | **4. Streamlit Application** | Build and customize a Streamlit application that brings together dashboard data and an AI assistant. |
| **20 min** | **5. Demonstration & Review** | Demonstrate the workflow, discuss architecture, compare SQL analytics with RAG, and conduct Q&A. |
| **Optional: +30–45 min** | **AI Agents with LangChain** | Explore tool calling with predefined SQL analytics and RAG retrieval tools, and inspect the agent's decisions. |

**Core workshop total: 180 minutes.** The AI Agents activity is optional and is not included in the three-hour schedule.

*The notebooks include extra explanations and diagrams and have not yet been timed with a student group; the detailed agenda lists where time can be saved after a dry run.*

## Lab materials

| Lab | Student tasks | What students see and do |
|---|---|---|
| **1 · Data ingestion, ETL & SQL** | 5 TODOs | Clean tickets in pandas, load them into a team schema, and query them with JOIN, GROUP BY, and FILTER. |
| **2 · Interactive dashboard** | 4 TODOs | KPI scorecard and five chart types, ending with a written finding and caveat. |
| **3 · Embeddings, vectors & RAG** | 4 TODOs | A toy vector space, then the 8-step RAG pipeline with real embeddings and pgvector. |
| **4 · Streamlit app** | Customisation exercises | The app is generated in eight explained pieces, then customised and run by the instructor. |
| **5 · LangChain agent (bonus)** | 2 TODOs | Two safe tools, an agent that chooses between them, and a trace of its decisions. |

## Prerequisites and logistics

**Recommended prior knowledge:** Basic Python (variables, functions, data structures). Familiarity with `SELECT`, `WHERE`, `JOIN`, and `GROUP BY` is helpful but not mandatory. No prior experience with RAG, vector databases, or Streamlit is required.

**Student requirements:** A laptop, stable internet connection, and a modern web browser. Google Colab is the primary environment; students may also use local Jupyter. **No Docker or local database installation is required.**

**Instructor-provided resources:** Guided notebooks and starter code, curated customer support data, a Supabase-hosted PostgreSQL/pgvector database with team access, a Streamlit application template, and managed instructions for OpenAI API access.

## Expected outcomes and deliverables

Students will produce or explore, with instructor guidance:

- A cleaned customer support dataset and its results stored in a team database schema.
- SQL analyses of ticket categories, statuses, response/resolution patterns, and satisfaction.
- A notebook-based interactive dashboard with business KPIs and charts, and a written finding with its caveat.
- A RAG workflow that retrieves relevant knowledge articles and generates answers with source references.
- An integrated Streamlit prototype demonstrating analytics and AI in one interface.
- *(Optional)* An introductory agent that routes questions to analytics or knowledge-retrieval tools.

**Educational emphasis:** understanding how structured data, SQL-based metrics, vector retrieval, and LLM responses solve different parts of a business problem—and how those parts fit into an end-to-end application.
