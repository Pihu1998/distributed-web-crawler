import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
from queue import Queue
import time
import logging

class WebCrawler:
    def __init__(self, start_url, max_threads=5, delay=1): 
        """
        Initializes a web crawler object with the provided parameters.

        Args:
            start_url (str): The starting URL for the web crawler.
            max_threads (int): The maximum number of threads to be used for crawling (default is 5).
            delay (int): The delay between HTTP requests to be polite to the server (default is 1).

        Attributes:
            start_url (str): The starting URL for the web crawler.
            base_domain (str): The base domain extracted from the starting URL.
            visited_urls (set): A set to store visited URLs and avoid duplicates.
            url_queue (Queue): A queue to manage URLs to be crawled.
            max_threads (int): The maximum number of threads to be used for crawling.
            delay (int): The delay between HTTP requests.
            lock (Lock): A threading lock for synchronization.
        """
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc 
        self.visited_urls = set() 
        self.url_queue = Queue() 
        self.url_queue.put(start_url)
        self.max_threads = max_threads
        self.delay = delay 
        self.lock = threading.Lock()    
        self.logger = logging.getLogger(__name__) 

    def crawl(self) -> None:
        """
        Initiates a multi-threaded crawling process.

        Args:
            self.max_threads (int): The maximum number of threads to be created.
            self.worker (method): The method to be executed by each thread.

        Returns:
            None    
        """
        threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            
    def worker(self) -> None:
        """
        Processes URLs from the queue and add them in visit set.

        Args: 
            None,
            
        Returns: 
            None    
        """
        while not self.url_queue.empty():
            current_url = self.url_queue.get()
            self.visit_url(current_url)
            time.sleep(self.delay)
            self.url_queue.task_done()

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> list:
        """
        Extracts and returns a list of urls within the same domain.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML content.
            base_url (str): The base URL to resolve relative links.

        Returns:
            list: A list of full URLs that are within the same domain as the base URL.
        """
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            full_url = urljoin(base_url, href)
            if self.is_same_domain(full_url):
                links.append(full_url)
        return links

    def visit_url(self, url: str) -> None:
        """
        Visits the given URL, fetches its content, and extracts links from it.

        Args:
            url (str): The URL to visit.

        Returns:
            None
        """
        if url in self.visited_urls:
            return

        with self.lock:
            self.visited_urls.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.logger.info(f"Visited: {url}")
            links = self.extract_links(soup, url)
            self.logger.info(f"Links found: {links}\n")
            for link in links:
                if link not in self.visited_urls and self.is_same_domain(link):
                    self.url_queue.put(link)
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")

    def is_same_domain(self, url: str) -> bool:
        """
        Checks if the given URL belongs to the same domain as the base domain.
        
        Args:
            url (str): The URL to check.

        Returns:    
            bool: True if the URL belongs to the same domain, False otherwise.
        """
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.base_domain
    
if __name__ == "__main__":
    start_url = "https://monzo.com/"
    crawler = WebCrawler(start_url)
    crawler.crawl()