import requests
from bs4 import BeautifulSoup
import calendar
import csv


def prepare_month_day_data_for_url():
    # List of month names
    months = [
        'January'
    ]

    # Initialize an empty list to store the formatted dates
    formatted_dates = []

    # Iterate over each month
    for month_idx, month_name in enumerate(months, start=1):
        # Get the number of days in the current month
        num_days_in_month = calendar.monthrange(2024, month_idx)[1]

        # Iterate over each day in the month
        for day in range(1, num_days_in_month + 1):
            # Format the date string and add it to the list
            formatted_date = f"{month_name}_{day}"
            formatted_dates.append(formatted_date)

    # Display the list of formatted dates
    return formatted_dates


def url_to_soup_object(url, headers):
    if 'http' in url:
        pass
    else:
        url = 'https://www.wiki*****.org' + url
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Content
    content = response.content

    # Create a BeautifulSoup object with the response content
    soup = BeautifulSoup(content, "html.parser")

    return soup


def scrape_wiki_birthdays():
    month_day = prepare_month_day_data_for_url()
    all_hrefs = []
    for url_suffix in month_day:
        url = "https://www.wiki*****.org/wiki/"+url_suffix

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': url
        }

        soup = url_to_soup_object(url, headers)

        # links = list(soup.find("div", id="mw-content-text").contents[7].find_all("li"))
        links = list(soup.find("div", class_="mw-parser-output").contents[0].find_all("li"))

        # find links
        # links = list(soup.find_all("a", class_="new"))
        if links:
            hrefs = []
            for link in links:
                hrefs.append(str(link).split("href=")[1].split(" title")[0][1:-1])
            all_hrefs.extend(hrefs)
            hrefs.clear()

    # birthdate_dataset = []
    name_surname = []
    birthdate = []
    birth_location = []

    for url in all_hrefs:
        url_object = url_to_soup_object(url, headers)
        if len(url_object.text.split('F***** ')) > 1:
            if len(url_object.text.split('?title=')) > 1:
                name_surname.append(url_object.text.split('?title=')[2].split('&oldid')[0])
            if len(url_object.text.split('?title=')) == 1:
                name_surname.append(url_object.text.split('?title=')[0].split(' - Wiki')[0].strip('\n'))
            if len(url_object.text.split('Birthday:')) > 1:
                if len(url_object.text.split('Birthday:')[1].split('Astro')) == 1:
                    if len(url_object.text.split('Birthday:')[1].split('Birth location')[0]) <= 18:
                        birthdate.append(url_object.text.split('Birthday:')[1].split('Birth location')[0])
                    if len(url_object.text.split('Birthday:')[1].split('Birth location')[0]) > 18:
                        birthdate.append(url_object.text.split('Birthday:')[1].split('Birth location')[0])
                if len(url_object.text.split('Birthday:')[1].split('Astro')) > 1:
                    birthdate.append(url_object.text.split('Birthday:')[1].split('Astro')[0])
            if len(url_object.text.split('Birthday:')) == 1:
                birthdate.append('Unknown')
            if len(url_object.text.split('Birth location:')) > 1:
                    source = url_object.text.split('Birth location:')[1]
                    # delimiter = "Years"
                    other_delimiters = ["Height:", "Years ******", "M***********:", "Birth name:"]
                    # if delimiter in source[0:40]:
                    #     birth_location.append(source.split(delimiter)[0])
                    # else:
                    for pattern in other_delimiters:
                        if pattern in source[0:55]:
                            birth_location.append(source.split(pattern)[0])
                            break
            if len(url_object.text.split('Birth location:')) == 1:
                birth_location.append('Unknown')
    # Zip the lists together
    birth_data = zip(name_surname, birthdate, birth_location)
    # Define the filename for the CSV file
    filename = 'person_data.csv'
    # Write the data into the CSV file
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header
        csvwriter.writerow(['Name/Surname', 'Birthdate', 'Birth Location'])

        # Write the rows
        for row in birth_data:
            csvwriter.writerow(row)
    return print("CSV file has been created successfully.")


def main():
    # Call the function to start scraping
    scrape_wiki_birthdays()


if __name__ == '__main__':
    main()
