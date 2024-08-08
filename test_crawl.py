from threading import Thread, Lock
import pytest
import responses
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from queue import Queue
from crawler import WebCrawler

# Fixture to create a WebCrawler instance
@pytest.fixture
def crawler():
    return WebCrawler("https://example.com", max_threads=1, delay=0)

def test_is_same_domain(crawler):
    assert crawler.is_same_domain("https://example.com/about") is True
    assert crawler.is_same_domain("https://sub.example.com") is False

def test_extract_links(crawler):
    html = '''
    <html><body>
    <a href="/about">About</a>
    <a href="https://example.com/contact">Contact</a>
    <a href="https://external.com">External</a>
    </body></html>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    links = crawler.extract_links(soup, "https://example.com")
    assert links == [
        "https://example.com/about",
        "https://example.com/contact"
    ]

@responses.activate
def test_visit_url(crawler):
    """
    Mocks the request for an example url and tests if new urls are added to visited set.
    """
    responses.add(responses.GET, "https://example.com",
                  body='<html><body><a href="/about">About</a></body></html>',
                  status=200)

    responses.add(responses.GET, "https://example.com/about",
                  body='<html><body><a href="/contact">Contact</a></body></html>',
                  status=200)

    crawler.visit_url("https://example.com")
    assert "https://example.com" in crawler.visited_urls
    assert "https://example.com/about" not in crawler.visited_urls

    crawler.visit_url("https://example.com/about")
    assert "https://example.com/about" in crawler.visited_urls
    assert "https://example.com/contact" not in crawler.visited_urls

if __name__ == "__main__":
    pytest.main()