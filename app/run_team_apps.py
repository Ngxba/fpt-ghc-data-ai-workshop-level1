"""Start one Streamlit app per team, so each team can show only its own project.

Every instance connects with that team's own database login (lab_team_NN) and lists only that team's
schema, so the database itself refuses to show any other team's data, even if someone edits the URL or settings.

Needs (environment variables, never written in code):
    LAB_PROJECT_REF   Supabase project reference
    LAB_POOLER_HOST   Transaction pooler host (not a full URL)
    OPENAI_API_KEY    Optional. Without it the dashboard works and the AI tab is disabled.

Reads instructor_team_credentials.csv (written by 00_instructor_setup.ipynb):
    team_number,schema,database_role,password

Examples:
    python app/run_team_apps.py --dry-run                 # show the plan, start nothing
    python app/run_team_apps.py                           # all teams, ports 8501, 8502, ...
    python app/run_team_apps.py --teams 1,3 --host 0.0.0.0   # teams 1 and 3, reachable from the network
"""
import argparse
import csv
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


def load_teams(csv_path, wanted):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    missing = {"team_number", "schema", "database_role", "password"} - set(rows[0].keys() if rows else [])
    if missing:
        sys.exit(f"{csv_path} is missing columns: {', '.join(sorted(missing))}")
    teams = []
    for r in rows:
        number = int(r["team_number"])
        if wanted and number not in wanted:
            continue
        teams.append({"number": number, "schema": r["schema"], "role": r["database_role"], "password": r["password"]})
    if wanted:
        unknown = wanted - {t["number"] for t in teams}
        if unknown:
            sys.exit(f"Teams not found in {csv_path}: {sorted(unknown)}")
    return sorted(teams, key=lambda t: t["number"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--credentials", default=str(ROOT / "instructor_team_credentials.csv"), help="path to the team credentials CSV")
    ap.add_argument("--teams", default="", help="comma-separated team numbers (default: all teams in the CSV)")
    ap.add_argument("--base-port", type=int, default=8500, help="team N is served on base-port + N (default 8500, so team 1 is 8501)")
    ap.add_argument("--host", default="127.0.0.1", help="address to listen on; use 0.0.0.0 to let other computers connect")
    ap.add_argument("--app", default=str(ROOT / "app" / "streamlit_app.py"), help="path to streamlit_app.py")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and exit without starting anything")
    args = ap.parse_args()

    project_ref = os.getenv("LAB_PROJECT_REF", "").strip()
    pooler_host = os.getenv("LAB_POOLER_HOST", "").strip()
    if not project_ref or not pooler_host:
        sys.exit("Set LAB_PROJECT_REF and LAB_POOLER_HOST in your environment first.")
    if not Path(args.credentials).exists():
        sys.exit(f"Credentials file not found: {args.credentials}")
    wanted = {int(x) for x in args.teams.split(",") if x.strip()} if args.teams else set()
    teams = load_teams(args.credentials, wanted)
    if not teams:
        sys.exit("No teams to start.")

    print(f"{'Team':<6}{'Schema':<10}{'Login':<34}URL")
    for t in teams:
        t["port"] = args.base_port + t["number"]
        shown_host = "localhost" if args.host in ("127.0.0.1", "localhost") else "<this computer's address>"
        print(f"{t['number']:<6}{t['schema']:<10}{t['role'] + '.' + project_ref:<34}http://{shown_host}:{t['port']}")
    if not os.getenv("OPENAI_API_KEY"):
        print("\nOPENAI_API_KEY is not set: the AI Support tab will be disabled.")
    if args.host not in ("127.0.0.1", "localhost"):
        print("\nWarning: the apps have no login screen. Anyone who can reach a port sees that one team's project, "
              "so share each port only with its team.")
    if args.dry_run:
        print("\nDry run: nothing started.")
        return

    procs = []
    try:
        for t in teams:
            user = quote(f"{t['role']}.{project_ref}", safe="")
            url = f"postgresql://{user}:{quote(t['password'], safe='')}@{pooler_host}:6543/postgres?sslmode=require"
            env = dict(os.environ, LAB_APP_DATABASE_URL=url, LAB_TEAM_SCHEMAS=t["schema"])
            cmd = [sys.executable, "-m", "streamlit", "run", args.app, "--server.port", str(t["port"]), "--server.address", args.host,
                   "--server.headless", "true", "--browser.gatherUsageStats", "false"]
            procs.append((t, subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(ROOT))))
        print("\nStarted. Press Ctrl+C to stop all apps.")
        while True:
            time.sleep(2)
            for t, p in procs:
                if p.poll() is not None:
                    print(f"Team {t['number']} app stopped (exit code {p.returncode}).")
                    procs = [(x, q) for x, q in procs if q is not p]
                    break
            if not procs:
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        for _, p in procs:
            if p.poll() is None:
                p.send_signal(signal.SIGTERM)
        for _, p in procs:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()


if __name__ == "__main__":
    main()
