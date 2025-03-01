from playwright.sync_api import sync_playwright,Playwright
from rich import print
def run(playwright: Playwright):
    chrome= playwright.chromium
    browser=chrome.launch(headless=True)
    page=browser.new_page()
    start_url="https://www.seek.com.au/jobs-in-science-technology/environmental-earth-geosciences/in-All-Australia"
    page.goto(start_url)
    page.wait_for_load_state("domcontentloaded")
    with open("jobs.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>Job Listings</title></head><body>")
        f.write("<h1>Job Listings</h1>")
        while True:
            job_titles = page.query_selector_all('[data-automation="jobTitle"]')
            job_companies = page.query_selector_all('[data-automation="jobCompany"]')
            job_locations = page.query_selector_all('[data-automation="jobCardLocation"]')
            job_subclassifications = page.query_selector_all('[data-automation="jobSubClassification"]')
            job_descriptions = page.query_selector_all('[data-automation="jobShortDescription"]')
            job_buttons = page.query_selector_all('//div[@class="gepq850 eihuid4v eihuid51"]/a')
            
            print("jobbbbbbbbbbbbbbbbbbbbbbbb", len(job_titles))
            print("-" * 30)
            for i in range(len(job_titles)):
                title = job_titles[i].inner_text() if i < len(job_titles) else 'N/A'
                company = job_companies[i].inner_text() if i < len(job_companies) else 'N/A'
                location = job_locations[i].inner_text() if i < len(job_locations) else 'N/A'
                subclass = job_subclassifications[i].inner_text() if i < len(job_subclassifications) else 'N/A'
                description = job_descriptions[i].inner_text() if i < len(job_descriptions) else 'N/A'
                href = job_buttons[i].get_attribute('href') if i < len(job_buttons) else 'N/A'
                f.write(f"<div><h2>{title}</h2>")
                f.write(f"<p><strong>Company:</strong> {company}</p>")
                f.write(f"<p><strong>Location:</strong> {location}</p>")
                f.write(f"<p><strong>Subclassification:</strong> {subclass}</p>")
                f.write(f"<p><strong>Description:</strong> {description}</p></div>")
                f.write(f'<a href="https://www.seek.com.au{href}">Know More</a>')
                f.write("<hr>")
                # print(href)
            next_page = page.query_selector("//li[@class='gepq850 eihuidbb eihuidb0 eihuidx']/a")
            if next_page:
                next_page.click()
                page.wait_for_timeout(7000)
                page.wait_for_load_state("domcontentloaded")
            else:
                print("No more pages")
                break
        f.write("</body></html>")
    browser.close()
with sync_playwright() as p:
    run(p)