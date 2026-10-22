# Quick instructor runbook

Full step-by-step setup (Supabase, `.env`, credentials) is in `README.md` → **Instructor setup**. This is the checklist version.

- **2 days before:**
  - Create the Supabase Free project; save the DB password; confirm it is not paused.
  - From **Connect**, copy the project ref, the **Session pooler** URI (5432) and the **Transaction pooler** host (6543).
  - `cp sample.env .env` and fill pass 1: `SUPABASE_ADMIN_DATABASE_URL`, `LAB_PROJECT_REF`, `LAB_POOLER_HOST`, `OPENAI_API_KEY`, `TEAM_COUNT`.
  - Enable OpenAI billing; create one limited key per team (or a secured proxy). Rehearse the Kaggle download.
- **Day before:**
  - Run `00_instructor_setup.ipynb` **once** locally (re-running section E regenerates every password and breaks anything already sent).
  - Keep `instructor_team_credentials.csv` and `instructor_app_credentials.csv` in a private location (never package or share them).
  - Fill `.env` pass 2: `LAB_APP_DATABASE_URL` (viewer password from `instructor_app_credentials.csv`, port 6543) and `LAB_TEAM_SCHEMAS` (`team_01,...`).
  - Test one team via the Transaction pooler `6543`. Preload cleaned team_01 data by running solution notebook 1 if wanting an immediate dashboard demo.
  - Dry-run the per-team apps: `uv run --env-file .env python app/run_team_apps.py --dry-run`.
- **Class start:** Send each team ONLY its own row of `instructor_team_credentials.csv` (team number, password) plus the project ref, pooler hostname and its own OpenAI key. Students add them as Colab **Secrets** (`LAB_PROJECT_REF`, `LAB_POOLER_HOST`, `LAB_TEAM_NUMBER`, `LAB_DB_PASSWORD`, `OPENAI_API_KEY`). Never send the admin URI, your `.env`, `lab_app_viewer`, or your own OpenAI key.
- **At 90 minutes:** Check all groups have run notebook 1; teams needing help can execute the instructor answer snippet.
- **Streamlit demo:** Set `LAB_APP_DATABASE_URL` (readonly `lab_app_viewer`), `LAB_TEAM_SCHEMAS`, and optionally `OPENAI_API_KEY`; run locally with `streamlit run app/streamlit_app.py`, or `uv run --env-file .env python app/run_team_apps.py` for one app per team (`run_team_apps.py` does not read `.env` itself). Students preview their own app inside Colab from notebook 4 ("Preview" cells): it starts Streamlit in the Colab session with their team login and shows it in a private frame. If the frame stays blank for a student, `output.serve_kernel_port_as_window(8501)` opens it in a new tab.
- **After workshop:** Rotate/revoke passwords, drop team schemas if desired and remove app role. Delete both credential CSVs. Review OpenAI usage and dataset retention.

### Example pooled DB URL (do not use literal placeholders)
`postgresql://lab_app_viewer.PROJECT_REF:PASSWORD@YOUR_POOLER_HOST:6543/postgres?sslmode=require`

Student usernames are formatted `lab_team_01.PROJECT_REF` for Supabase's shared pooler, **not** just `lab_team_01`.

### Common problems
- Connection fails: check hostname, port 6543, project ref and pooled login format. The Free direct endpoint may be IPv6-only; pooler is compatible with IPv4.
- `permission denied`: rerun instructor grants and check the selected team schema.
- `vector does not exist`: check Supabase extension `vector` installed under schema `extensions`.
- `response_to_resolution_hours` mostly NULL: Kaggle's timestamp data can be incomplete/noisy; avoid filling missing values as zeros.
- `No cleaned data` in app: notebook 1 has not been run for that team; rerun the ETL UPSERT.
- API 429: stagger student LLM calls; monitor per-account budget/rate limits.
- Dataset download fails: confirm KaggleHub access; instructor can manually download the same Kaggle CSV and adapt notebook 0's file path rather than changing the dataset source.
