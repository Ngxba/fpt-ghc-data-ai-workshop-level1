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

## Learning objectives

By the end of the workshop, students should be able to:

1. Explain a simple extract-transform-load (ETL) workflow and apply core data-cleaning steps using Python and Pandas.
2. Explore a relational schema and use SQL joins, filters, and aggregations to answer business questions.
3. Visualize database-backed metrics using interactive charts.
4. Explain embeddings, vector similarity search, and retrieval-augmented generation (RAG), and implement a guided RAG workflow.
5. Connect analytics and AI capabilities in a Streamlit application prototype.

## Agenda

| Time | Session | Main activity |
|---|---|---|
| **45 min** | **1. Data Engineering & SQL** | Explore the Kaggle customer support dataset; clean records; load team data into PostgreSQL; query with SQL. |
| **25 min** | **2. Analytics & Dashboard** | Define practical support metrics and build interactive Plotly charts in Jupyter. |
| **50 min** | **3. Embeddings & RAG** | Generate OpenAI embeddings; store and search vectors with pgvector; use retrieved articles to ground LLM answers. |
| **40 min** | **4. Streamlit Application** | Customize a provided application template that brings together dashboard data and an AI assistant. |
| **20 min** | **5. Demonstration & Review** | Demonstrate the workflow, discuss architecture, compare SQL analytics with RAG, and conduct Q&A. |
| **Optional: +30–45 min** | **AI Agents with LangChain** | Explore tool calling with predefined SQL analytics and RAG retrieval tools. |

**Core workshop total: 180 minutes.** The AI Agents activity is optional and is not included in the three-hour schedule.

## Prerequisites and logistics

**Recommended prior knowledge:** Basic Python (variables, functions, data structures). Familiarity with `SELECT`, `WHERE`, `JOIN`, and `GROUP BY` is helpful but not mandatory. No prior experience with RAG, vector databases, or Streamlit is required.

**Student requirements:** A laptop, stable internet connection, and a modern web browser. Google Colab is the primary environment; students may also use local Jupyter. **No Docker or local database installation is required.**

**Instructor-provided resources:** Guided notebooks and starter code, curated customer support data, a Supabase-hosted PostgreSQL/pgvector database with team access, a Streamlit application template, and managed instructions for OpenAI API access.

## Expected outcomes and deliverables

Students will produce or explore, with instructor guidance:

- A cleaned customer support dataset and its results stored in a team database schema.
- SQL analyses of ticket categories, statuses, response/resolution patterns, and satisfaction.
- A notebook-based interactive dashboard with business KPIs and charts.
- A RAG workflow that retrieves relevant knowledge articles and generates answers with source references.
- An integrated Streamlit prototype demonstrating analytics and AI in one interface.

**Educational emphasis:** understanding how structured data, SQL-based metrics, vector retrieval, and LLM responses solve different parts of a business problem—and how those parts fit into an end-to-end application.
