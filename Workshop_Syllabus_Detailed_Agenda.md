# From Data to AI: Building an Intelligent Customer Support Application

**Detailed workshop agenda and learning plan**  
**Duration:** 3 hours (180 minutes)  
**Delivery:** Instructor demonstrations, guided Jupyter notebooks, team exercises, and project review  
**Optional extension:** 30–45 minutes for AI Agents with LangChain

## Teaching approach

Students work through **four progressive lab notebooks** and a closing demonstration. Each module introduces the key ideas, asks students to complete selected code or SQL placeholders, and ends with a visible result. The instructor provisions Supabase, access credentials, and starter data beforehand. Students use **Google Colab** or local Jupyter, so no Docker or local PostgreSQL instance is required.

The project context is a **Customer Support Intelligence Platform**. The ticket dataset comes from Kaggle and is used for educational analytics; a separate, curated support knowledge base powers the RAG exercises.

### How the notebooks are written

Every notebook is a **guided, step-by-step walkthrough** rather than a bare exercise sheet:

- **Each step explains three things:** *what* the code does, *why* it is needed, and *what students should see* when it works, so they can check their own progress.
- **Diagrams support every module** (38 in total, loaded from the GitHub `assets/` folder so they display in Colab; students need internet access): data flow and architecture diagrams, before/after tables, annotated charts, flow charts and sequence diagrams.
- **Short coding tasks (TODOs)** are placed after the explanation, with hints that point to the idea without giving the answer. Complete solutions are provided separately in `solutions/`.
- **Real numbers from the reference run** (for example 600 tickets, 34.7 % closed) appear in the "what you should see" notes, so students can verify their results and practise reading them critically.
- **Every notebook ends with a recap table and discussion questions**, and the modules repeatedly stress caveats: missing values, small samples, the difference between a metric and an official SLA, and the limits of AI answers.

### Notebook overview

| Lab | Student coding tasks | Diagrams |
|---|---|---|
| `01_data_etl_sql.ipynb` | 5 TODOs: missing values, duplicates, derived duration, JOIN + GROUP BY, closed rate with FILTER | 7 |
| `02_dashboard_in_notebook.ipynb` | 4 TODOs: closed-rate KPI, bubble-chart mapping, box-plot data filter, heatmap crosstab; plus writing one finding and one caveat | 5 |
| `03_embeddings_rag_openai.ipynb` | 4 TODOs: nearest-vector scoring (Part 0), embedding, cosine-distance search, grounded prompt | 18 |
| `04_streamlit_app.ipynb` | Customisation exercises on the generated app (no blanks): KPI, default filters, explain the RAG function, title/chart | 4 |
| `05_bonus_langchain_agent.ipynb` (optional) | 2 TODOs: a question for the metrics tool, a question that needs both tools | 4 |

## Session 1 — Data Engineering & SQL Fundamentals

**Duration:** 45 minutes  
**Lab:** `01_data_etl_sql.ipynb`

**Students learn**
- How a raw dataset becomes reliable, queryable information through **ETL: Extract, Transform, Load, then Analyse**.
- The purpose of schemas, keys, relationships, and appropriate data types in relational databases.
- Why missing values must stay missing (`NULL`, never an invented `0`) and how that affects averages.
- How SQL filtering, joins, grouping, aggregations, and conditional aggregates (`FILTER`) answer operational questions.
- What a transaction and an idempotent **UPSERT** are, and why they make loading safe to repeat.

**Hands-on activities**
- Connect to Supabase with the provided helpers and inspect the schema through `information_schema`.
- Extract a sample of raw tickets and profile missing values before changing anything.
- Complete guided Pandas transformations in five small steps (types and text, missing keys and duplicates, dates, a derived resolution-time column, conversion of pandas missing values to database `NULL`).
- Read the prewritten UPSERT loader, load results into a team-specific PostgreSQL schema, and read the rows back from the database to verify.
- Write SQL for a JOIN with aggregation (average resolution time per ticket type) and a closed rate using `FILTER`.

**Diagrams:** ETL pipeline, database/schema map, raw-to-clean transformation, resolution-time timeline, UPSERT flow chart, JOIN + GROUP BY with `AVG` skipping `NULL`, and closed-rate calculation.

**Checkpoint / outcome:** A repeatable small ETL process, populated team table, and working SQL queries that summarize customer support operations.

## Session 2 — Data Analytics & Interactive Dashboard

**Duration:** 25 minutes  
**Lab:** `02_dashboard_in_notebook.ipynb`

**Students learn**
- How to translate business questions into meaningful key performance indicators (KPIs) and label them honestly.
- When to aggregate in SQL and when in Pandas, and how to choose a chart type for each question.
- How to read a bubble chart, sunburst, box plot, and heatmap; why the median and outliers can matter more than the mean.
- How interactive visualization supports exploration, and how to state **one finding and one caveat** from a chart.

**Hands-on activities**
- Query team data from PostgreSQL, profile which columns are categorical or numeric and which have missing values.
- Build a KPI scorecard and complete the closed-rate calculation.
- Create Plotly charts: a bubble chart of resolution time versus satisfaction per ticket type, a channel/priority/status sunburst, a box plot of resolution time by priority, an issue-by-channel heatmap, and a bar chart with a dropdown that switches the measure.
- Use the chart-quality checklist, then write a finding and a caveat; identify one potential operational improvement.

**Diagrams:** dashboard workflow, chart-chooser guide, annotated bubble chart, sunburst anatomy, and box-plot anatomy.

**Checkpoint / outcome:** An interactive, database-backed dashboard inside Jupyter or Colab, and a written finding with its caveat.

## Session 3 — OpenAI Embeddings, Vector Search & RAG

**Duration:** 50 minutes  
**Lab:** `03_embeddings_rag_openai.ipynb`

**Students learn**
- What a **vector** and a **vector database** are, using a small two-dimensional toy example before the real 1,536-dimension embeddings.
- The difference between relational queries and semantic document retrieval, and between Euclidean distance, cosine similarity, and inner product.
- Why exact search does not scale and what approximate nearest-neighbour (ANN) indexes trade away.
- The **eight steps of a RAG system** in two phases: indexing (chunk, embed, store) and querying (question, embed the question, retrieve, optional re-rank, generate), and why the same embedding model must be used for both.
- How retrieval-augmented generation supplies contextual evidence to an LLM and why source grounding matters.

**Hands-on activities**
- **Part 0:** plot a toy embedding space, find nearest vectors by brute force, and run a small in-memory vector database.
- Observe chunking with a sentence-based chunker with overlap; compare the instructor's short articles (one article, one chunk).
- Compare cosine similarity for related and unrelated sentences using real OpenAI embeddings.
- Generate an embedding for a new knowledge article and store it in Supabase PostgreSQL with pgvector.
- Complete a top-k semantic-search query with the cosine-distance operator.
- Pass retrieved article content to an OpenAI model, requesting source-referenced answers.
- Test a question that is not addressed by the knowledge base and observe the system's limitations.

**Diagrams:** 18 in total, including the RAG architecture and the step-by-step RAG workflow, plus vector, embedding-space, vector-database and ANN-search illustrations. Several come from the Daily Dose of Data Science article *Foundations of RAG systems* and are credited in the notebook.

**Checkpoint / outcome:** A guided question-answering pipeline with embedding, vector retrieval, and a grounded LLM response.

## Session 4 — Streamlit: Integrating Analytics and AI

**Duration:** 40 minutes  
**Lab:** `04_streamlit_app.ipynb` and a prewritten Streamlit template

**Students learn**
- How a lightweight web interface connects to structured data and AI services, and why Streamlit is a **separate web server** that Colab can only generate a file for.
- How Streamlit works: the script reruns from top to bottom on every interaction, with `st.cache_data` and `st.session_state` providing memory.
- How to organize a prototype into configuration, data retrieval, analysis, presentation, and AI interaction components.
- Why secrets belong in environment variables, why the app uses a **read-only** database role, and why the schema name is validated.
- The difference between notebook experimentation and application delivery.

**Hands-on activities**
- Generate the complete app in eight explained pieces (imports and settings, database helper, AI helpers, sidebar and tabs, data loading, dashboard tab, AI chat tab, methodology tab) and check that the file is valid Python.
- Examine and customize the application: rename or add a KPI, change the default filters, explain why the question embedding is sent to PostgreSQL, adjust the title or donut chart.
- Instructor starts the app from a terminal using the environment variables, with a table of the app's error messages and fixes.
- Test the application with several support questions; inspect the displayed data and cited sources.

**Diagrams:** system architecture, the Streamlit rerun model, a numbered wireframe of the app mapped to its Streamlit functions, and a sequence diagram of one chat question.

**Checkpoint / outcome:** A functional application prototype combining interactive analytics and an AI support assistant. The instructor can host the final Streamlit demonstration to avoid requiring individual student deployments.

## Session 5 — Project Demonstration & Review

**Duration:** 20 minutes

**Activities**
- Walk through the completed application and the end-to-end data flow.
- Compare questions best answered by SQL with those better suited to document retrieval and RAG.
- Compare a notebook dashboard with a standalone web application.
- Discuss data quality, AI reliability, source attribution, and practical next steps, using the discussion questions at the end of each notebook.
- Student demonstrations, questions, and feedback.

**Checkpoint / outcome:** Students can explain the roles of ETL, PostgreSQL, dashboards, embeddings, retrieval, and LLMs in the complete workflow.

## Optional bonus — AI Agents & Tool Calling with LangChain

**Duration:** Additional 30–45 minutes  
**Lab:** `05_bonus_langchain_agent.ipynb`

**Students learn**
- How an AI agent differs from a basic LLM prompt or fixed RAG pipeline: the LLM **decides** which tool to call, in a loop.
- How tool calling lets a model choose from predefined, constrained actions, and how a tool's name, arguments, and docstring are what the model sees.
- Why permission boundaries and validation matter when an AI system accesses external data: the model can only choose from three fixed, read-only queries and cannot write SQL.
- When a fixed pipeline is simpler, cheaper, and more predictable than an agent.

**Hands-on activities**
- Reuse the Notebook 3 retrieval function as a tool, and define a second tool for SQL-based support analytics.
- Test each tool directly, including an unsafe input that is refused, before any LLM is involved.
- Create the agent and ask a counting question, then a troubleshooting question, and inspect the message trace: tool requested, arguments, tool result, final answer.
- Write a question that needs both tools; compare the agent's answer with plain RAG.

**Diagrams:** RAG versus agent, the agent loop alongside the real message list, the anatomy of a tool, and the guardrail design.

**Checkpoint / outcome:** An introductory agent that routes appropriate questions to analytics or knowledge retrieval tools. This is a bonus and not required for core workshop completion.

## Learning requirements and assessment

**Recommended preparation:** Basic Python skills and introductory familiarity with SQL. No prior AI, Supabase, or Streamlit experience is necessary.

**Technical setup:** Student laptop, internet access, browser, and Google Colab or local Jupyter. Instructor manages Supabase PostgreSQL/pgvector, database access, dataset preparation, and OpenAI access arrangements. No student-side Docker or database installation is needed. On Colab, students keep credentials in **Colab Secrets** (read with `google.colab.userdata`); on local Jupyter in a `.env` file (loaded with `python-dotenv`); otherwise they type them in. Never inside the notebook.

**Assessment approach:** Informal, practical checkpoints after each module rather than a formal exam. Successful participation is demonstrated by transformed records, working queries, charts with a written finding and caveat, an RAG response with source references, and participation in the final application review.

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

### Timing note for instructors

The notebooks now contain explanations, diagrams, and short check cells in addition to the coding tasks, and they have **not yet been timed with a student group**. The schedule above is unchanged, so please do a dry run before the workshop. If time is short, these are the safest places to save it:

- **Session 3, Part 0** (vectors and the toy vector database) can be shown as an instructor demonstration instead of a student activity.
- **Session 4** can focus on the dashboard and AI tabs and the customisation exercises, treating the code-reading sections as a guided tour.
- Students can read the "why" paragraphs after the session; the notebooks are written to be re-read on their own.
