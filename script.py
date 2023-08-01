import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def scrape_domain_and_subdomains(base_url, file_path):
    visited_urls = set()

    def scrape(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            div_elements = soup.select("div.md-content")

            text = ""
            for div in div_elements:
                text += div.get_text()
            append_to_text_file(text, file_path)

            links = soup.find_all("a")
            for link in links:
                href = link.get("href")
                if href:
                    subdomain_url = urljoin(url, href)
                    parsed_url = urlparse(subdomain_url)
                    if (
                        parsed_url.netloc.endswith("docs.taipy.io")
                        and subdomain_url not in visited_urls
                    ):
                        visited_urls.add(subdomain_url)
                        scrape(subdomain_url)

    scrape(f"http://{base_url}")
    print(visited_urls)


def append_to_text_file(content, file_path):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)
        file.write("\n")


# Example usage:
base_url = "docs.taipy.io/en/latest/"  # Replace with the base domain to scrape (without the protocol)
file_path = "data/data_2.0.txt"  # Replace with the desired file path

scrape_domain_and_subdomains(base_url, file_path)
