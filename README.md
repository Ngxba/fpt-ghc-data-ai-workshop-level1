# AI Customer Support Intelligence — Supabase Free + OpenAI workshop

**Five independent student notebooks**, instructor provisioning notebook, instructor solutions, and a runnable Streamlit application. Course: **3 hours core + 30–45 minute optional agent bonus**.

## Exact learning flow
| Section | File | Time | Outcome |
|---|---|---:|---|
| 1 | `notebooks/01_data_etl_sql.ipynb` | 45m | Real Kaggle sample in Supabase -> Pandas cleaning -> SQL table + joins |
| 2 | `notebooks/02_dashboard_in_notebook.ipynb` | 25m | Plotly metrics and charts directly in Colab/Jupyter |
| 3 | `notebooks/03_embeddings_rag_openai.ipynb` | 50m | OpenAI embedding -> team pgvector -> SQL retrieval -> grounded LLM |
| 4 | `notebooks/04_streamlit_app.ipynb` | 40m | Generate full Streamlit app and inspect UI; instructor runs locally |
| Review | Student demos, breaks, and discussion | 20m | Present database, charts, citations and limitations |
| 5 **bonus** | `notebooks/05_bonus_langchain_agent.ipynb` | +30–45m | LangChain agent chooses read-only metric or RAG tool |

## Instructor setup (do this before class)

Everything below is done **once, on your own computer**. Students never touch the admin database URL, your OpenAI key, or the `.env` file.

### Step 1 · Install the tools
- Needs **Python 3.13+** (`.python-version`) and [`uv`](https://docs.astral.sh/uv/).
- From the repo root: `uv sync`, then `uv run jupyter lab`. This installs Jupyter, `kagglehub`, `pandas`, `psycopg`, `openai`, and `python-dotenv` from `pyproject.toml`.
- For the Streamlit demo (Step 10) also run `uv pip install -r app/requirements.txt`; `streamlit` and `plotly` are not in `pyproject.toml`.

### Step 2 · Create the Supabase project
1. Sign in at https://supabase.com/dashboard and click **New project** (Free plan). Pick a region close to the class.
2. Set a **database password** and **save it now** (password manager). You need it for the admin URI. If you lose it: **Project Settings → Database → Reset database password**.
3. Wait until the project shows as healthy. Free projects **pause after about a week of inactivity**, so open the dashboard the day before class and restore it if needed.
4. Click **Connect** (top of the dashboard) and keep the page open. You will copy three things from it:
   - **Project ref**: the short ID in the dashboard URL (`supabase.com/dashboard/project/<ref>`), also under **Project Settings → General → Reference ID**.
   - **Session pooler** connection string (port **5432**). This is your *admin* URI.
   - **Transaction pooler** host (port **6543**). Copy the host exactly as shown (for example `aws-0-<region>.pooler.supabase.com`). Do not guess it from your region.
5. Do **not** use the `service_role` / `anon` API keys as database passwords. They are not database credentials.

You do not need to enable `pgvector` by hand: `00_instructor_setup.ipynb` runs `CREATE EXTENSION vector`. If that cell fails, enable it under **Database → Extensions → vector**.

### Step 3 · Get an OpenAI API key
Create a key at https://platform.openai.com/api-keys on an account with billing enabled. This is **your** key: it is used only by the setup notebook (about 18 embeddings, a few cents) and optionally by the instructor-run Streamlit app. Students need their own limited keys (see Step 7).

### Step 4 · Create `.env` from `sample.env`
```bash
cp sample.env .env      # .env is git-ignored; never commit or share it
```
Fill it in **in two passes**, because some values only exist after the setup notebook has run.

**Pass 1: before running `00_instructor_setup.ipynb`**

| Variable | What to put | Where to get it |
|---|---|---|
| `SUPABASE_URL` | `https://<ref>.supabase.co` | **Project Settings → API**. Informational only; no notebook or app reads it. |
| `LAB_PROJECT_REF` | `abcdefghijklmnop` (the project ref) | Dashboard URL, or **Project Settings → General** |
| `LAB_POOLER_HOST` | Host name only, e.g. `aws-0-eu-west-1.pooler.supabase.com` | **Connect → Transaction pooler** (no `postgresql://`, no port) |
| `SUPABASE_ADMIN_DATABASE_URL` | `postgresql://postgres.<ref>:<PASSWORD>@<host>:5432/postgres` | **Connect → Session pooler**. Replace `[YOUR-PASSWORD]` with your DB password. URL-encode special characters in the password (`@` → `%40`, `/` → `%2F`, `#` → `%23`). Must be port **5432**. |
| `OPENAI_API_KEY` | `sk-...` | Step 3 |
| `TEAM_COUNT` | `8` | Number of student groups (1–40) |

`.env` format rules: one `NAME=value` per line, **each value on a single line** (a key wrapped onto a second line breaks parsing), no spaces around `=`, no duplicate names (`sample.env` already contains each name once), and keep the file out of git.

**Pass 2: after the setup notebook has finished** (it writes two CSV files next to the notebook, see Step 6)

| Variable | What to put | Where to get it |
|---|---|---|
| `LAB_APP_DATABASE_URL` | `postgresql://lab_app_viewer.<ref>:<PASSWORD>@<transaction-pooler-host>:6543/postgres?sslmode=require` | Password is in `instructor_app_credentials.csv`. Port is **6543**. Needed only for the single shared Streamlit app. |
| `LAB_TEAM_SCHEMAS` | `team_01,team_02,team_03` | One `team_NN` per team, comma-separated, matching `TEAM_COUNT` |
| `LAB_TEAM_NUMBER`, `LAB_DB_PASSWORD` | e.g. `1` and that team's password | A row of `instructor_team_credentials.csv`. Only needed if you want to **test as a student** in a notebook on your machine; leave blank otherwise. |

`python app/run_team_apps.py` does **not** read `.env` itself. Load it for that command: `uv run --env-file .env python app/run_team_apps.py`.

### Step 5 · Run the setup notebook
1. `uv run jupyter lab`, open `00_instructor_setup.ipynb`, and run cells top to bottom. It reads `.env`; any missing value is asked for with a hidden prompt.
2. It downloads the Kaggle dataset `suraj520/customer-support-ticket-dataset` with `kagglehub`. If it asks for Kaggle credentials, set `KAGGLE_USERNAME` / `KAGGLE_KEY` or run `kagglehub.login()`.
3. It creates the `shared` tables (up to 600 tickets, 18 embedded KB articles), one `team_NN` schema + `lab_team_NN` login per team, and the read-only `lab_app_viewer` login.
4. The last cell prints row counts: `shared.raw_tickets` (up to 600), `shared.ticket_types`, and `shared.knowledge_articles` (18).

> **Re-running section E ("Team schemas, least-privilege roles, and Streamlit viewer") generates new passwords** for every team and for `lab_app_viewer` (`ALTER ROLE ... PASSWORD`) and overwrites both CSVs. Anything you already sent to students stops working. Run it once, and only hand out credentials afterward.

### Step 6 · Get the team credentials
The notebook writes two files in the repo root (both git-ignored, `chmod 600`):

| File | Columns | Use |
|---|---|---|
| `instructor_team_credentials.csv` | `team_number, schema, database_role, password` | One row per team. Source of each team's password. Also read by `app/run_team_apps.py`. |
| `instructor_app_credentials.csv` | `database_role, password` | The `lab_app_viewer` password, for `LAB_APP_DATABASE_URL`. |

Back both up somewhere private. Never email or post the whole CSV.

**Send each team only its own five values** (use a separate private message per team):

| Value | Source |
|---|---|
| Team number | `team_number` column, e.g. `3` |
| Database password | `password` column in that team's row |
| Project ref | `LAB_PROJECT_REF` in your `.env` |
| Pooler host | `LAB_POOLER_HOST` in your `.env` (transaction pooler, host only) |
| OpenAI API key | Their own limited key (Step 7) |

The login the notebooks build from these is `lab_team_03.<project-ref>`. Students do **not** receive the `postgres` admin URI, `lab_app_viewer`, or your OpenAI key.

### Step 7 · Plan student OpenAI access
Notebooks 3 and 5 call OpenAI. Either create one **restricted, budget-capped key per team** (OpenAI dashboard → project → limits), or provide a separately secured proxy (not included). Never hand out your instructor key. Check the budget and rate limits before class; stagger calls if you see HTTP 429.

### Step 8 · How students enter the credentials
- **Google Colab (default):** **Secrets** (key icon, left sidebar) → **Add new secret** for each of `LAB_PROJECT_REF`, `LAB_POOLER_HOST`, `LAB_TEAM_NUMBER`, `LAB_DB_PASSWORD`, and `OPENAI_API_KEY` (notebooks 3/5), with **Notebook access** switched on. Each notebook's "Colab secrets" cell copies them into environment variables.
- **Local Jupyter:** student copies `sample.env` to `.env` and fills in only those five variables. They must **not** receive your `.env`.
- Otherwise notebooks ask for any missing value with a prompt. Notebook 1 must run first; the others are standalone but need the credentials again in a new session.

### Step 9 · Test before class
1. Open notebook 1 on Colab with team 1's values. It should print `Connected to: team_01`.
2. Run `solutions/01_data_etl_sql.ipynb` for team 1 if you want an immediate dashboard demo.
3. Confirm the OpenAI key works in notebook 3.
4. Dry-run the demo apps: `uv run --env-file .env python app/run_team_apps.py --dry-run`.

### Step 10 · Run the final Streamlit demo (locally)
- **One shared app** (all teams selectable): set `LAB_APP_DATABASE_URL`, `LAB_TEAM_SCHEMAS`, optional `OPENAI_API_KEY` in `.env`, then `uv run streamlit run app/streamlit_app.py`.
- **One app per team** (each team sees only its own data): `uv run --env-file .env python app/run_team_apps.py`. Needs `LAB_PROJECT_REF`, `LAB_POOLER_HOST` (and optional `OPENAI_API_KEY`) in the environment, and `instructor_team_credentials.csv`. Teams are served on ports 8501, 8502, ... Options: `--teams 1,3`, `--host 0.0.0.0`, `--dry-run`. The apps have no login screen; share each port only with its team.

### Step 11 · After class
Rotate or revoke the team passwords and the `lab_app_viewer` password (or drop the `team_NN` schemas and roles), delete the CSVs, and review OpenAI usage. See `reference/instructor_runbook.md` for a checklist and troubleshooting.

## Security & teaching assumptions
- Only instructor manages DDL, roles, extension and common data.
- Each team login can **read `shared` and read/write its own two tables**, not create tables or access other teams' data.
- Streamlit uses a **read-only app viewer** for class demos. Do not publish an unauthenticated app with an instructor-funded OpenAI key on the internet; use private access and rate limits.
- Direct identifiers (customer name/email/age/gender) are excluded when instructor loads Kaggle data. Free-text descriptions can still contain synthetic contact details; sanitize before sharing to audiences.
- `First Response Time` and `Time to Resolution` are timestamps; difference is **response-to-resolution proxy**, **not total resolution time nor SLA**. Missing/outlier/negative values become NULL. KPI calculations exclude null durations.
- Kaggle source is a **synthetic teaching dataset**; KB articles are fictional and separate. Model answers may still be wrong. Human review essential.
- Embeddings use `text-embedding-3-small` **1536D**, LLM uses `gpt-4.1-mini`, and `pgvector` exact cosine search (`<=>`) for tiny KB. No vector index needed for 18 articles.
- All notebook connections use Supabase's transaction pooler with psycopg prepared statements disabled; each operation closes connections. Team roles use schema-qualified queries.
- Generated credentials CSV stays on instructor machine; it is not packaged; rotate/revoke after class. Supabase Free can pause after inactivity, verify project alive before class.

## Structure
```
00_instructor_setup.ipynb  # instructor-only provisioning (reads .env)
sample.env                 # template: cp sample.env .env, then fill in
instructor_team_credentials.csv / instructor_app_credentials.csv   # generated, git-ignored
notebooks/01_data_etl_sql.ipynb
notebooks/02_dashboard_in_notebook.ipynb
notebooks/03_embeddings_rag_openai.ipynb
notebooks/04_streamlit_app.ipynb
notebooks/05_bonus_langchain_agent.ipynb
solutions/                # fully filled answer notebooks for each section
app/streamlit_app.py      # identical to code generated by notebook 4
app/requirements.txt
app/run_team_apps.py      # one Streamlit app per team
reference/schema_reference.sql
reference/instructor_runbook.md
README.md
```

## Limitations and testing
Source data download, Supabase login, OpenAI requests, and running Streamlit require **your real credentials/network** and are not verified live by this offline build. All notebook structures and static Python syntax are validated; see `validation_report.txt` for QA details.

## Official docs
- Dataset: https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset
- KaggleHub: https://github.com/Kaggle/kagglehub
- Supabase connection: https://supabase.com/docs/guides/database/connecting-to-postgres
- pgvector: https://supabase.com/docs/guides/database/extensions/pgvector
- OpenAI API: https://developers.openai.com/api/docs/libraries
- Streamlit: https://docs.streamlit.io/develop/api-reference/chat
- LangChain: https://reference.langchain.com/python/langchain/agents/factory/create_agent
