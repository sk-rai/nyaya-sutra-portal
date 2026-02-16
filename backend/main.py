# scraper/court_scraper.py

import pdfplumber
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class CourtScraper:
    def __init__(self):
        self.courts = {
            'aft_delhi': 'https://aftdelhi.nic.in/index.php/reg-benches/mumbai/mumbai-cause-list',
            'cgat': 'https://cis.cgat.gov.in/catlive/pdf/'
        }
    
    def scrape_daily(self):
        """Run daily to fetch and parse PDFs"""
        cases = []
        
        # Scrape AFT Delhi
        aft_cases = self.scrape_aft_delhi()
        cases.extend(aft_cases)
        
        # Scrape CGAT
        cgat_cases = self.scrape_cgat()
        cases.extend(cgat_cases)
        
        return cases
    
    def scrape_aft_delhi(self):
        """Scrape AFT Delhi cause lists"""
        response = requests.get(self.courts['aft_delhi'])
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find PDF links
        pdf_links = soup.find_all('a', href=lambda x: x and '.pdf' in x.lower())
        
        cases = []
        for link in pdf_links:
            pdf_url = link['href']
            if not pdf_url.startswith('http'):
                pdf_url = 'https://aftdelhi.nic.in' + pdf_url
            
            # Download and parse PDF
            pdf_cases = self.parse_aft_pdf(pdf_url)
            cases.extend(pdf_cases)
        
        return cases
    
    def parse_aft_pdf(self, pdf_url):
        """Parse AFT PDF and extract case metadata"""
        response = requests.get(pdf_url)
        pdf_content = response.content
        
        cases = []
        
        with pdfplumber.open(BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                
                # Parse case entries (regex-based)
                # Example pattern: "AFT/DEL/2023/1234 | 15 Feb 2026 | ..."
                case_pattern = r'([A-Z]+/[A-Z]+/\d+/\d+)\s+\|\s+(\d+\s+[A-Za-z]+\s+\d+)'
                
                matches = re.findall(case_pattern, text)
                
                for match in matches:
                    case_number = match[0]
                    hearing_date = match[1]
                    
                    cases.append({
                        'case_number': case_number,
                        'hearing_date': datetime.strptime(hearing_date, '%d %b %Y'),
                        'court': 'AFT Delhi',
                        'source_pdf': pdf_url
                    })
        
        return cases