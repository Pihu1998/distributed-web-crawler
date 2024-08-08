# Web Crawler

## Overview
This project is a simple multithreaded web crawler designed to crawl all URLs within the same
domain as the starting url. It's implemented in python and uses Python’s requests library for making HTTP requests and BeautifulSoup for parsing HTML content. The code is thread-safe and supports concurrent crawling using Python's threading module.

It starts from a given URL and recursively visits all URLs found on the same domain, following a breadth-first search (BFS) strategy.

## Project Structure
- WebCrawler Class: The main class that encapsulates the crawling logic.

  - `__init__(self, start_url, max_threads=5, delay=1)`: Initializes the crawler with a starting URL, maximum number of threads, and a delay between requests.
  - `crawl(self)`: Starts the crawling process using multiple threads.
  - `worker(self)`: A worker method executed by each thread to fetch and process URLs.
  - `visit_url(self, url: str)`: Fetches the content of a given URL, extracts links, and adds them to a queue if they belong to the same domain. In addition, mark them as visited.
  - `extract_links(self, soup, base_url)`: Extracts and returns all valid links from the HTML content.
  - `is_same_domain(self, url)`: Checks if a given URL belongs to the same domain as the starting URL.

- Utilities:

  - Queue: A thread-safe queue used to manage URLs to be crawled, ensuring BFS order.
  - set: A set used to store visited URLs to avoid revisiting them.
  - logging: Configured to log crawler activities like visited URLs and errors.

- Threading: Python’s threading module is used to manage concurrent requests, allowing multiple pages to be crawled simultaneously.

## Getting Started
### Prerequisites
Make sure you have Python 3.6 or above installed. You will also need to install the Python libraries
from `requirements.txt` file:

You can install the necessary packages using pip:

```
pip install -r requirements.txt
```

### Running the Crawler
1. Clone the Repository (or download the script directly):

```
git clone https://github.com/your-repo/web-crawler.git
cd web-crawler
```

2. Edit the Start URL:

Open the script in a text editor and update the start_url in the __main__ block with the URL you wish to start crawling from:.

```
start_url = "https://monzo.com/"
```

3. Run the script:

```
python web_crawler.py
```
4. Output:
The script will print the URLs it visits and the links it finds on each page.

### Configuration
- max_threads: Controls the number of threads used for crawling. The default is 5. You can adjust this to control the level of concurrency.
- delay: Sets a delay (in seconds) between requests to avoid overwhelming the target server. Default is 1 second.

## Trade-offs and Design Decisions
- **Concurrency**: The crawler uses threading for concurrent requests. This is simpler to implement but may not be the most efficient for large-scale crawling due to Python’s Global Interpreter Lock (GIL). Alternatives like multiprocessing or using asynchronous I/O with asyncio could potentially offer better performance but would add complexity.

- **Breadth-First Search (BFS)**: The BFS approach ensures that all links on the current page are crawled before moving to the next level. This is a good approach for evenly distributed crawling but may not be as memory-efficient as depth-first search (DFS) in some scenarios.

- **Error Handling**: The current implementation handles network errors and continues crawling. However, more granular error handling could be implemented to handle specific HTTP errors differently (e.g., retrying on timeouts, skipping certain HTTP status codes).

- **Politeness**: The delay parameter is used to introduce politeness by controlling the rate of requests.  A more sophisticated approach might include checking for robots.txt and adhering to server rate limits.

## Some of the areas for Improvement
- **Logging Enhancements**: The logging could be expanded to include more detailed information such as timestamps, thread IDs, and even saving logs to a file for further analysis.

- **Testing**: While the code is structured for readability and maintainability, more comprehensive unit tests and possibly integration tests should be implemented to ensure robustness and correct behavior in various scenarios.

- **Prioritized URL Parsing**: Currently, a simple queue is used to extract urls in an order determined by it's basic FIFO architecture. URLs can be better prioritized based on factors like relevance, depth, or freshness of the page.

- **Circular loop detection**: An improvement could be made to detect circular loop for urls, where the crawler might repeatedly visit the same set of pages.

- **Duplicate content avoidance**: Sometimes multiple pages has similiar content posted. This could be avoided by using techniques to check for duplicates

- **Sitemap and Robots.txt Compliance**: Improve adherence to web standards.

