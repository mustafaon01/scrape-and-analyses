import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
from main.Logger import Logger
import logging

# Start log config
Logger.setup_logging()


class Scraper:
    def __init__(self, base_url, total_pages):
        """
        Initialize the scraper with base URL and total number of pages to scrape.
        :param base_url: Base URL of the website to scrape.
        :param total_pages: Total number of pages to scrape.
        """
        self.base_url = base_url
        self.total_pages = total_pages

    @staticmethod
    def scrape_news_details(news_url):
        """
        Scrape news details from a single news URL.
        :param news_url: URL of the news to scrape.
        :return: text, img_urls, publish_date, update_date of the news article.
        """
        try:
            response = requests.get(news_url)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                logging.warning(f"Failed to retrieve news from {news_url}: Status code {response.status_code}")
                return None, None, None, None

            soup = BeautifulSoup(response.content, 'html.parser')

            text = soup.find('div', class_='yazi_icerik').get_text(strip=True)
            img_urls = [img['src'] for img in soup.find_all('img', class_='onresim')]
            dates = soup.find('div', class_='yazibio').find_all('time')
            publish_date = dates[0]['datetime'] if dates else None
            update_date = dates[1]['datetime'] if len(dates) > 1 else None

            logging.info(f"Successfully scraped news details from {news_url}")
            return text, img_urls, publish_date, update_date

        except Exception as e:
            logging.error(f"Error while scraping news details from {news_url}: {e}")
            return None, None, None, None

    def scrape_news_page(self, url):
        """
        Scrape all news articles from a single page.
        :param url: URL of the page to scrape.
        :return: List of news items scraped from the page.
        """
        news_items = []
        try:
            response = requests.get(url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            for article in soup.find_all('article', class_='col-12'):
                header = article.find('h2', class_='haber-baslik').get_text(strip=True)
                summary = article.find('div', class_='haber-desc').get_text(strip=True)
                news_url = article.find('a')['href']

                text, img_url_list, publish_date, update_date = self.scrape_news_details(news_url)
                # Check if the news details were successfully scraped
                if text:
                    news_items.append({
                        'url': news_url,
                        'header': header,
                        'summary': summary,
                        'text': text,
                        'img_url_list': img_url_list,
                        'publish_date': publish_date,
                        'update_date': update_date
                    })
                # Wait
                time.sleep(0.2)

        except requests.exceptions.Timeout:
            logging.error(f"Timeout error for URL: {url}")
        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error for URL: {url}")

        return news_items

    def scrape_all_pages_concurrently(self):
        """
        Scrape all pages concurrently using ThreadPoolExecutor.
        :return: Tuple of all news items scraped and statistics.
        """
        start_time = time.time()
        all_news_items = []
        futures = []
        success_count = 0
        failure_count = 0

        with ThreadPoolExecutor(max_workers=5) as executor:
            for page in range(1, self.total_pages + 1):
                page_url = f"{self.base_url}page/{page}/"
                futures.append(executor.submit(self.scrape_news_page, page_url))

            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_news_items.extend(result)
                    success_count += len(result)
                else:
                    failure_count += 1

        end_time = time.time()
        elapsed_time = end_time - start_time
        scrape_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        stats = {
            'total_news': len(all_news_items),
            'elapsed_time': elapsed_time,
            'average_time_per_news': elapsed_time / len(all_news_items) if all_news_items else 0,
            'scrape_date': scrape_date,
            'success_count': success_count,
            'failure_count': failure_count
        }

        return all_news_items, stats
