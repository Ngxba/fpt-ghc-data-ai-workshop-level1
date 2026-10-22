# Quick instructor runbook

- **2 days before:** Create Supabase Free and obtain Session pooler admin URI, enable vector, OpenAI billing. Rehearse Kaggle download.
- **Day before:** Run `00_instructor_setup.ipynb` locally. Preserve `instructor_team_credentials.csv` in a private location (never package it). Test one team via Transaction pooler `6543`. Preload cleaned team_01 data by running solution notebook 1 if wanting an immediate dashboard demo.
- **Class start:** Send each team ONLY its own password, pooler hostname, project ref and team number. Ensure OpenAI access via own budgeted per-team keys or managed gateway.
- **At 90 minutes:** Check all groups have run notebook 1; teams needing help can execute the instructor answer snippet.
- **Streamlit demo:** Set `LAB_APP_DATABASE_URL` (readonly `lab_app_viewer`), `LAB_TEAM_SCHEMAS`, and optionally `OPENAI_API_KEY`; run locally with `streamlit run app/streamlit_app.py`. Students preview their own app inside Colab from notebook 4 ("Preview" cells): it starts Streamlit in the Colab session with their team login and shows it in a private frame. If the frame stays blank for a student, `output.serve_kernel_port_as_window(8501)` opens it in a new tab.
- **After workshop:** Rotate/revoke passwords, drop team schemas if desired and remove app role. Review OpenAI usage and dataset retention.

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
