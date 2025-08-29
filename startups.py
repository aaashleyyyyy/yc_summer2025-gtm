from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url= "https://www.ycombinator.com/companies?batch=Summer%202025"

driver.get(url)
time.sleep(5)

entries = driver.find_elements(By.CSS_SELECTOR, "a._company_i9oky_355")

data = []
for e in entries:
    try:
        name = e.find_element(By.CSS_SELECTOR, "span._coName_i9oky_470").text
    except:
        name = "N/A"
    
    try:
        # Try different selectors for description
        description = e.find_element(By.CSS_SELECTOR, "div.text-sm").text
    except:
        try:
            description = e.find_element(By.CSS_SELECTOR, "div[class*='text-sm']").text
        except:
            description = "N/A"
    
    # Industries (multiple tags)
    try:
        industry_tags = e.find_elements(By.CSS_SELECTOR, "a._tagLink_i9oky_1040")
        industry_list = [i.text for i in industry_tags if "Summer" not in i.text]
        industries = ", ".join(industry_list)
    except:
        industries = "N/A"
    
    # Get the href (link) to the company page
    try:
        href = e.get_attribute("href")
        # Convert relative URLs to full URLs
        if href and href.startswith("/"):
            href = "https://www.ycombinator.com" + href
    except:
        href = "N/A"
    
    data.append([name, description, industries, href])

driver.quit()

df = pd.DataFrame(data, columns=["Company", "Description", "Industries", "YC Link"])
df.to_csv("yc_summer2025_startups.csv", index=False)
print("Scrape complete!")
