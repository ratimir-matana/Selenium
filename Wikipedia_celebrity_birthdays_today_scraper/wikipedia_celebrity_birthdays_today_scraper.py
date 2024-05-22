import requests
from bs4 import BeautifulSoup


def scrape_celebrity_birthdays():
    url = "https://en.wikipedia.org/wiki/Wikipedia:Database_reports/Birthday_today"

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the celebrity birthdays
        table = soup.find("table", class_="wikitable")

        if table:
            # Find all the rows in the table
            rows = table.find_all("tr")

            # Iterate over the rows and extract the celebrity names and birthdays
            for row in rows[1:]:
                columns = row.find_all("td")
                if len(columns) >= 2:
                    name = columns[2].text.strip()
                    birthday = columns[1].text.strip()
                    print(f"{name}: {birthday}")
        else:
            print("No birthday table found on the page.")
    else:
        print("Failed to retrieve the webpage.")


def main():
    # Call the function to start scraping
    scrape_celebrity_birthdays()


if __name__ == '__main__':
    main()
