import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def discover_urls(base_url, urls=set(), visited=set()):
    url = base_url
    urls.add(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith('http') or href.startswith('//'):
                full_url = urljoin(base_url, href)
                if full_url not in visited:
                    yield full_url
                    visited.add(full_url)
                    yield from discover_urls(full_url, urls, visited)
    except requests.exceptions.HTTPError as e:
        print(f"Error {e.response.status_code} while accessing {url}")

if __name__ == "__main__":
    base_url = input("Enter the base URL to scan: ")
    urls = set()
    visited = set()
    for url in discover_urls(base_url, urls, visited):
        print(url)
