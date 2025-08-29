import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Read the CSV file
df = pd.read_csv("yc_summer2025_startups.csv")

# List to store all extracted data
data = []

print(f"Found {len(df)} startups to process")

# Loop through each YC link
for index, row in df.iterrows():
    company_name = row['Company']
    yc_link = row['YC Link']
    
    print(f"\n--- Processing {index + 1}/{len(df)}: {company_name} ---")
    
    try:
        # Navigate to the company page
        driver.get(yc_link)
        time.sleep(3)  # Wait for page to load
        
        
        # Try to get company website - with proper error handling
        try:
            link_element = driver.find_element(
                By.CSS_SELECTOR,
                'div.group.flex.flex-row.items-center.px-3.leading-none.text-linkColor a'
            )
            extracted_url = link_element.get_attribute('href')
        except Exception as e:
            continue

        founder_dict = {}
        
        # Try to get founder information
        try:
            # Wait until the "Active Founders" section loads
            founder_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Active Founders')]"))
            )
            
            # Get all founder cards
            founder_cards = driver.find_elements(By.CSS_SELECTOR, "div.ycdc-card-new")
            print(f"Found {len(founder_cards)} founder cards")

            # Initialize founder data
            founder_data = {}
            
            for idx, card in enumerate(founder_cards):
                # Indexing starts from 1 for cleaner output
                i = idx + 1

                # Get name
                try:
                    name = card.find_element(By.CSS_SELECTOR, "div.text-xl.font-bold").text.strip()
                    print(f"Founder {i} name: {name}")
                except Exception as e:
                    print(f"Founder {i} name not found: {str(e)}")
                    name = "N/A"

                # Get LinkedIn
                try:
                    linkedin = card.find_element(By.CSS_SELECTOR, "a[href*='linkedin.com/in/']").get_attribute("href")
                    print(f"Founder {i} LinkedIn: {linkedin}")
                except:
                    linkedin = "N/A"

                # Store in flat dict
                founder_data[f"founder{i}_name"] = name
                founder_data[f"founder{i}_linkedin"] = linkedin

        except Exception as e:
            print(f"Founder information not found: {str(e)}")
            founder_data = {}
        
        # Store the data - flatten the founder data into the main row
        row_data = [company_name, extracted_url]
        
        # Add founder data to the row - only for founders that exist
        for i in range(1, len(founder_cards) + 1):  # Loop based on actual founders found
            founder_name_key = f"founder{i}_name"
            founder_linkedin_key = f"founder{i}_linkedin"
            
            # Only add founder data if BOTH name and LinkedIn are available (not "N/A")
            founder_name = founder_data.get(founder_name_key)
            founder_linkedin = founder_data.get(founder_linkedin_key)
            
            if founder_name != "N/A" and founder_linkedin != "N/A":
                row_data.append(founder_name)
                row_data.append(founder_linkedin)
        
        data.append(row_data)
        print(f"Successfully extracted data for {company_name}")
        
    except Exception as e:
        print(f"Error processing {company_name}: {str(e)}")
        # Add empty data for failed entries
        row_data = [company_name, "N/A"]
        data.append(row_data)
 
    # Add delay to be respectful
    time.sleep(2)

driver.quit()

# Create dynamic columns based on the data
# Start with base columns
columns = ["Company", "URL"]

# Find the maximum number of founders across all rows
max_founders = 0
for row in data:
    # Count how many founder pairs we have in this row
    founder_count = (len(row) - 2) // 2  # Subtract Company and URL, divide by 2 (name + linkedin)
    max_founders = max(max_founders, founder_count)

# Add founder columns only for the actual founders found
for i in range(1, max_founders + 1):
    columns.append(f"founder{i}_name")
    columns.append(f"founder{i}_linkedin")

print(f"Creating CSV with columns: {columns}")
print(f"Maximum founders found: {max_founders}")

df = pd.DataFrame(data, columns=columns)
df.to_csv("yc_summer2025_startups_details.csv", index=False)
print("Scrape complete!")

   
  



    
