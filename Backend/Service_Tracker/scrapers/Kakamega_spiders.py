from datetime import datetime,deltatime
import logging
from bs4 import BeautifulSoup
from base_scraper import BaseScrapper

logger= logging.getLogger(__name__)

class kakamegaSpider(BaseScrapper):
    def __init__(self):
        super().__init__()
        self.target_urls = "https//kakamega.co.ke/category/announcements"

    def scrape(self) -> list[dict]:
        extracted_records = []
        try:
            logger.info(f"Starting Mombasa data extraction pipeline targeting: {self.target_url}")
            html_content = self.fetch_html(self.target_url)
            
            if not html_content:
                return extracted_records

            soup = BeautifulSoup(html_content, "html.parser")
            table_rows = soup.find_all("tr", class_="announcement-row")

            for row in table_rows:
            try:
                columns=row.find_all("td")
                if len(columns) < 3:
                 continue

            title_text= columns[0].get_text(strip=True)

            if "LAND" in title_text.upper() or "RATE" in title_text.upper()
             service= "LAND_RATE"

            elif "HEALTH" in title_text.upper():
             service = "HEALTH_CERTICICATE"

            else:
              continue

