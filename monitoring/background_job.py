# monitoring/background_job.py

import time
from threading import Thread

CHECK_INTERVAL = 600  # 10 minutes

def monitor_jobs_loop(app, db, MonitoringRule, WatchlistMatch, scrape_jobs_func, extract_text_func, match_func):
    def _run_loop():
        with app.app_context():
            print("📡 Real-time job monitoring started...")
            while True:
                rules = MonitoringRule.query.all()
                for rule in rules:
                    print(f"🔄 Checking jobs for rule: {rule.job_title} (User ID: {rule.user_id})")

                    resume_text = extract_text_func(rule.resume.filepath)
                    job_df = scrape_jobs_func(rule.job_title, pages=1)
                    top_matches = match_func(resume_text, jobs_df=job_df, top_n=10)

                    for _, row in top_matches.iterrows():
                        already_exists = WatchlistMatch.query.filter_by(
                            rule_id=rule.id,
                            job_title=row["title"],
                            company=row["company"]
                        ).first()

                        if not already_exists:
                            match = WatchlistMatch(
                                rule_id=rule.id,
                                job_title=row["title"],
                                company=row["company"],
                                location=row["location"],
                                description=row["description"],
                                match_score=row["match_score"],
                                link=row["link"]
                            )
                            db.session.add(match)
                            db.session.commit()
                            print(f"✅ New match found: {row['title']} - {row['company']}")

                time.sleep(CHECK_INTERVAL)

    # Run in background thread
    thread = Thread(target=_run_loop, daemon=True)
    thread.start()
