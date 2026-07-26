from datetime import datetime
import logging
from bs4 import BeautifulSoup
from base_scraper import BaseScrapper

logger= logging.getLogger(__name__)

class NairobiSpiders(BaseScrapper):
    def __init__(self):
        super().__init__()
        self.target_url("https//nairobi.go.ke/notices/")

    def Scrapers(self) -> list[dict]:
        extracted_record=[]
        try:
            logger.info= (f"Starting Nairobi data extraction pipeline targeting: {self.target_url}")
            html_content= self.fetch_html(self.target_url)

            if not html_content:
             return extracted_record

            soup= BeautifulSoup(html_content,"html_parser") 