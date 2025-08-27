from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

def scrape_rozee_jobs_selenium(query="data scientist", pages=1):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  # set to False to debug visually

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    job_list = []

    for page in range(1, pages + 1):
        url = f"https://www.rozee.pk/job/jsearch/q/{query}/pn/{page}"
        driver.get(url)
        print(f"Loading page {page}...")

        time.sleep(6)  # allow JS content to load

        jobs = driver.find_elements(By.CSS_SELECTOR, "div.job")
        print(f"✅ Found {len(jobs)} jobs on page {page}")

        for job in jobs:
            try:
                lines = job.text.strip().split("\n")
                if len(lines) < 3:
                    continue

                title = lines[0]
                company_and_location = lines[1]
                description = lines[2]

                if "," in company_and_location:
                    company, location = company_and_location.split(",", 1)
                else:
                    company, location = company_and_location, "N/A"

                # 🔗 Extract the job link from anchor tag
                try:
                    link_element = job.find_element(By.CSS_SELECTOR, "a")
                    job_url = link_element.get_attribute("href")
                except:
                    job_url = ""

                job_list.append({
                    "title": title.strip(),
                    "company": company.strip(),
                    "location": location.strip(),
                    "description": description.strip(),
                    "link": job_url.strip()
                })

            except Exception as e:
                print("⚠️ Error parsing job:", e)

    driver.quit()

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(job_list)
    df.to_csv("data/rozee_jobs.csv", index=False)
    print(f"✅ Saved {len(df)} jobs to data/rozee_jobs.csv")

    return df
