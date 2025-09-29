# Install dependencies first if needed
# pip install selenium webdriver-manager pandas

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_jobs(keyword, num_jobs=20, verbose=True, slp_time=2):
    """
    Scrapes Glassdoor job listings into a pandas DataFrame.
    """
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment to run in background

    # Initialize ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)

    # Open Morocco Glassdoor page
    url = 'https://www.glassdoor.com/Job/morocco-data-scientist-jobs-SRCH_IL.0,7_IN162_KO8,22.htm'
    print("Opening Glassdoor Morocco...")
    driver.get(url)
    time.sleep(slp_time)

    jobs = []

    while len(jobs) < num_jobs:
        time.sleep(slp_time)

        # Close signup pop-up if it appears
        try:
            popup_close = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))
            )
            popup_close.click()
            if verbose:
                print("Signup popup closed")
        except TimeoutException:
            if verbose:
                print("No signup popup found")

        # Wait until job cards are visible
        try:
            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-test="jobListing"]'))
            )
        except TimeoutException:
            print("No job listings found on this page.")
            break

        for card in job_cards:
            if len(jobs) >= num_jobs:
                break
            try:
                # Scroll card into view
                driver.execute_script("arguments[0].scrollIntoView(true);", card)
                time.sleep(0.5)

                job_title = card.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').text
                company_name = card.find_element(By.CSS_SELECTOR, 'span.EmployerProfile_compactEmployerName__9MGcV').text
                location = card.find_element(By.CSS_SELECTOR, 'div[data-test="emp-location"]').text
                try:
                    salary = card.find_element(By.CSS_SELECTOR, 'div[data-test="detailSalary"]').text
                except NoSuchElementException:
                    salary = None
                job_link = card.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').get_attribute('href')

                jobs.append({
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Location": location,
                    "Salary": salary,
                    "Job Link": job_link
                })

                if verbose:
                    print(f"Scraped: {job_title} at {company_name}")

            except Exception as e:
                if verbose:
                    print("Error scraping a card:", e)
                continue

        # Try to go to next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li[aria-label="Next"] a')
            next_button.click()
            time.sleep(slp_time)
        except NoSuchElementException:
            print("No more pages or reached scraping limit")
            break

    driver.quit()
    print(f"Scraping finished. Total jobs collected: {len(jobs)}")
    return pd.DataFrame(jobs)

# Example usage:
if __name__ == "__main__":
    df = get_jobs("data-scientist", num_jobs=20)
    print(df)
    df.to_csv("glassdoor_jobs_morocco.csv", index=False)