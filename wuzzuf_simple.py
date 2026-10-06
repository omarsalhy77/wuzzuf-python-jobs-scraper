import csv
import requests
from bs4 import BeautifulSoup

url = "https://wuzzuf.net/search/jobs/?q=python&a=hpb"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
response = requests.get(url, headers=headers)
print("Status:", response.status_code)  

if response.status_code != 200:
    print("The site blocked the request, so nothing was saved.")
    exit()


soup = BeautifulSoup(response.text, "html.parser")

job_types = ["Full Time", "Part Time", "Internship", "Freelance / Project",
             "Work From Home", "Hybrid", "On-site", "Shift Based"]

all_jobs = []

for title in soup.select("h2 a"):
    name = title.get_text(strip=True)

    location = title.find_next("span", string=lambda text: text and "Egypt" in text)

    job_type = title.find_next(string=lambda text: text and text.strip() in job_types)

    skill_tags = title.find_all_next("a", href=lambda link: link and "/a/" in link, limit=4)
    skills = ", ".join(tag.get_text(strip=True) for tag in skill_tags)

    all_jobs.append([
        name,
        location.strip() if location else "N/A",
        job_type.strip() if job_type else "N/A",
        skills,
    ])

with open("wazzuf_python_jobs.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Location", "Job Type", "Description"])
    writer.writerows(all_jobs)

print("Done! Saved", len(all_jobs), "jobs to wazzuf_python_jobs.csv")