
import requests
import csv
from bs4 import BeautifulSoup

# Website URLs
HEADLINES_URL = "https://www.bbc.com/news"
QUOTES_URL = "https://quotes.toscrape.com/"

# Function to fetch website content
def get_soup(url):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        print("Website error:", error)
        return None


# Function to scrape headlines
def scrape_headlines():
    print("\nFetching Headlines...")

    soup = get_soup(HEADLINES_URL)

    if soup is None:
        return

    headlines = soup.select("h2, h3")

    data = []

    for headline in headlines:
        title = headline.get_text(strip=True)

        if title:
            data.append([title])

    with open("headlines.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Headline"])
        writer.writerows(data)

    print("Headlines saved successfully!")
    print("Total headlines:", len(data))


# Function to scrape quotes
def scrape_quotes():
    print("\nFetching Quotes...")

    soup = get_soup(QUOTES_URL)

    if soup is None:
        return

    quotes = soup.select(".quote")

    data = []

    for item in quotes:
        quote = item.select_one(".text")
        author = item.select_one(".author")

        if quote and author:
            data.append([
                quote.get_text(strip=True),
                author.get_text(strip=True)
            ])

    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author"])
        writer.writerows(data)

    print("Quotes saved successfully!")
    print("Total quotes:", len(data))


# Main program
if __name__ == "__main__":
    print("WEB SCRAPER - HEADLINES & QUOTES")

    scrape_headlines()
    scrape_quotes()

    print("\nScraping Completed!")
