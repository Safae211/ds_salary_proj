import asyncio
from urllib.parse import urlencode, urlparse
from playwright.async_api import async_playwright, Playwright

async def scrape_data(playwright: Playwright):
    # Launch a Chromium browser instance
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    # Define the base URL and query parameters for the Glassdoor search
    base_url = "https://www.glassdoor.com/Explore/browse-companies.htm?"
    query_params = {
        "overall_rating_low": "3.5",
        "locId": "1132348",
        "locType": "C",
        "locName": "New York, NY (US)",
        "occ": "Machine Learning Engineer",
        "filterType": "RATING_OVERALL",
    }

    # Construct the full URL with query parameters and navigate to it
    url = f"{base_url}{urlencode(query_params)}"
    await page.goto(url)

    # Initialize a counter for the records extracted
    record_count = 0

    # Locate all company cards on the page and iterate through them to extract data
    company_cards = await page.locator('[data-test="employer-card-single"]').all()
    for card in company_cards:
        try:
            # Extract relevant data from each company card
            company_name = await card.locator('[data-test="employer-short-name"]').text_content(timeout=2000) or "N/A"
            rating = await card.locator('[data-test="rating"]').text_content(timeout=2000) or "N/A"
            location = await card.locator('[data-test="employer-location"]').text_content(timeout=2000) or "N/A"
            global_company_size = await card.locator('[data-test="employer-size"]').text_content(timeout=2000) or "N/A"
            industry = await card.locator('[data-test="employer-industry"]').text_content(timeout=2000) or "N/A"

            # Construct the URL for job listings
            jobs_url_path = await card.locator('[data-test="cell-Jobs-url"]').get_attribute("href", timeout=2000) or "N/A"
            parsed_url = urlparse(base_url)
            jobs_url_path = f"{parsed_url.scheme}://{parsed_url.netloc}{jobs_url_path}"

            # Extract additional data about jobs, reviews, and salaries
            jobs_count = await card.locator('[data-test="cell-Jobs"] h3').text_content(timeout=2000) or "N/A"
            reviews_count = await card.locator('[data-test="cell-Reviews"] h3').text_content(timeout=2000) or "N/A"
            salaries_count = await card.locator('[data-test="cell-Salaries"] h3').text_content(timeout=2000) or "N/A"

            # Print the extracted data
            print({
                "Company": company_name,
                "Rating": rating,
                "Jobs URL": jobs_url_path,
                "Jobs Count": jobs_count,
                "Reviews Count": reviews_count,
                "Salaries Count": salaries_count,
                "Industry": industry,
                "Location": location,
                "Global Company Size": global_company_size,
            })

            record_count += 1
        except Exception as e:
            print(f"Error extracting company data: {e}")
    print(f"Total records extracted: {record_count}")

    # Close the browser
    await browser.close()

# Entry point for the script
async def main():
    async with async_playwright() as playwright:
        await scrape_data(playwright)

if __name__ == "__main__":
    asyncio.run(main())