import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
from countryinfo import CountryInfo
import requests
from requests.exceptions import ConnectionError
import PyPDF2
import os
from retrying import retry


# Define a retry decorator with exponential backoff
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
def fetch_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.content


def month_to_number(month):
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }
    # Convert input to lowercase to handle case insensitivity
    month = month.lower()
    return months.get(month)


def check_csv_data(birth_day, birth_month, birth_year):
    birthday_correct = False
    birth_month_correct = False
    birth_year_correct = False
    birthday_check = birth_day.isdigit() and int(birth_day) in list(range(1, 32))
    birth_month_check = str(birth_month).isdigit() and birth_month in list(range(1, 13))
    birth_year_check = birth_year.isdigit()
    if birthday_check:
        birthday_correct = True
    if birth_month_check:
        birth_month_correct = True
    if birth_year_check:
        birth_year_correct = True
    return birthday_correct and birth_month_correct and birth_year_correct


def location_check(location):
    return isinstance(location, str) and location not in ['Unknown']


def american_states_capitals():
    state_capitals = {
        "Alabama": "Montgomery",
        "Alaska": "Juneau",
        "Arizona": "Phoenix",
        "Arkansas": "Little Rock",
        "California": "Sacramento",
        "Colorado": "Denver",
        "Connecticut": "Hartford",
        "Delaware": "Dover",
        "Florida": "Tallahassee",
        "Georgia": "Atlanta",
        "Hawaii": "Honolulu",
        "Idaho": "Boise",
        "Illinois": "Springfield",
        "Indiana": "Indianapolis",
        "Iowa": "Des Moines",
        "Kansas": "Topeka",
        "Kentucky": "Frankfort",
        "Louisiana": "Baton Rouge",
        "Maine": "Augusta",
        "Maryland": "Annapolis",
        "Massachusetts": "Boston",
        "Michigan": "Lansing",
        "Minnesota": "St. Paul",
        "Mississippi": "Jackson",
        "Missouri": "Jefferson City",
        "Montana": "Helena",
        "Nebraska": "Lincoln",
        "Nevada": "Carson City",
        "New Hampshire": "Concord",
        "New Jersey": "Trenton",
        "New Mexico": "Santa Fe",
        "New York": "Albany",
        "North Carolina": "Raleigh",
        "North Dakota": "Bismarck",
        "Ohio": "Columbus",
        "Oklahoma": "Oklahoma City",
        "Oregon": "Salem",
        "Pennsylvania": "Harrisburg",
        "Rhode Island": "Providence",
        "South Carolina": "Columbia",
        "South Dakota": "Pierre",
        "Tennessee": "Nashville",
        "Texas": "Austin",
        "Utah": "Salt Lake City",
        "Vermont": "Montpelier",
        "Virginia": "Richmond",
        "Washington": "Olympia",
        "West Virginia": "Charleston",
        "Wisconsin": "Madison",
        "Wyoming": "Cheyenne"
    }
    return state_capitals


def american_states_short():
    state_short = {
        "Nevada": "NV"
    }
    return state_short


def get_key_from_value(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return False


def main():
    alternate_characters = {'í': 'i'}
    alternate_state_names = {'England': 'United Kingdom', 'NE': 'Nevada', 'USA': 'Washington', 'NY': 'New York',
                             'U.S.A.': 'USA', 'TX': 'Texas', 'California': 'CA', 'Southern California': 'California',
                             'North Carolina': 'NC'}
    alternate_city_names = {'Ontario': 'Toronto', 'San Gabriel Valley': 'San Gabriel',
                            'City of Industry': 'Rowland Heights', 'South Yorkshire': 'Swinton', 'Oahu': 'Honolulu',
                            'Yorkshire': 'Leeds'}
    filename = '/home/Documents/***********/person_data.csv'
    filename_out = '/home/Documents/**********/person_data_score.csv'
    with open(filename_out, 'w', newline='') as csvfile_score:
        csv_writer = csv.writer(csvfile_score)
        # Write the header
        csv_writer.writerow(['Name/Surname', 'Birthdate', 'Birth Location', 'Birth Location Check', 'Score'])
        # Open the data in the CSV file
        with open(filename, 'r', newline='') as csvfile:
            csv_read = csv.reader(csvfile)
            # Skip the first row (header)
            next(csv_read)
            for row in csv_read:
                # Check if the current row is empty (end of file)
                if not row:
                    break  # Break out of the loop if the row is empty
                csv_name = row[0].replace('_', ' ') if '_' in row[0] else row[0]
                # csv_birthdate = row[1]
                if row[1] in ['Unknown']:
                    continue
                if '!' in row[1] or '/' in row[1]:
                    continue
                csv_birthmonth = month_to_number(row[1].split(' ')[0])
                csv_birthday = row[1].split(' ')[1].split(',')[0]
                csv_birthyear = row[1].split(',')[1][1:]
                csv_location = row[2]

                first_p_name = "FirstPersonX"
                first_p_bday = "1"
                first_p_bday_month = "1"
                first_p_bday_year = "1989"

                # Specify the path to the GeckoDriver executable
                gecko_driver_path = '/usr/local/bin/geckodriver'

                # Create a Service object with the specified GeckoDriver executable path
                service = Service(gecko_driver_path)

                # Set Firefox options for headless mode
                options = Options()
                options.add_argument('-headless')

                # Create a new instance of the Firefox driver using the Service object
                driver = webdriver.Firefox(options=options, service=service)

                # Test Selenium by opening a website
                driver.get("https://***********.org/php_gn/synastry/index.php")

                # Find the input field by name attribute
                input_field6 = driver.find_element(By.NAME, "city1")

                # Clear any existing value in the input field
                input_field6.clear()

                # Send individual key events to input the string 'zagreb'
                for char in 'zagreb':
                    input_field6.send_keys(char)
                    # Simulate a keydown event for each character
                    input_field6.send_keys(Keys.DOWN)
                    # Wait time in seconds
                    time.sleep(0.3)

                # Wait for the suggestions to appear
                try:
                    suggestion_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "autoSuggestionsList1")))

                    # Click on the first suggestion
                    suggestion_item = WebDriverWait(suggestion_list, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
                    suggestion_item[0].click()

                except StaleElementReferenceException:
                    # Element is stale, refresh the reference
                    suggestion_item = WebDriverWait(suggestion_list, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
                    suggestion_item[0].click()

                except TimeoutException:
                    print("Timeout occurred while waiting for the suggestion list to appear.")

                # Find the input field by name attribute
                input_field1 = driver.find_element(By.NAME, "name1")

                # Clear any existing value in the input field
                input_field1.clear()

                # Enter your custom string value in the input field
                input_field1.send_keys(first_p_name)

                # Find the input field by name attribute
                input_field_month1 = driver.find_element(By.NAME, "month1")

                # Send custom string in input_field
                input_field_month1.send_keys(first_p_bday_month)

                # Find the input field by name attribute
                input_field2 = driver.find_element(By.NAME, "day1")

                # Clear any existing value in the input field
                input_field2.clear()

                # Enter your custom string value in the input field
                input_field2.send_keys(first_p_bday)

                # Find the input field by name attribute
                input_field3 = driver.find_element(By.NAME, "year1")

                # Clear any existing value in the input field
                input_field3.clear()

                # Enter your custom string value in the input field
                input_field3.send_keys(first_p_bday_year)

                # Find the input field by name attribute
                input_field4 = driver.find_element(By.NAME, "hour1")

                # Clear any existing value in the input field
                input_field4.clear()

                # Enter your custom string value in the input field
                input_field4.send_keys("11")

                # Find the input field by name attribute
                input_field5 = driver.find_element(By.NAME, "minute1")

                # Clear any existing value in the input field
                input_field5.clear()

                # Enter your custom string value in the input field
                input_field5.send_keys("35")

                # Find the select field by name attribute
                select_field_amorpm1 = Select(driver.find_element(By.NAME, "amorpm1"))

                # Use the select field as needed
                # For example, you can select an option by value
                select_field_amorpm1.select_by_value('AM')

                # END OF FIRST PERSON FILLING
                ########################################################################################

                second_p_name = csv_name.split('_') if '_' in csv_name else csv_name
                second_p_bday = csv_birthday
                second_p_bday_month = csv_birthmonth
                second_p_bday_year = csv_birthyear
                second_p_state_country = csv_location if not ',' in csv_location else csv_location.split(',')[1][1:]
                second_p_city = csv_location if not ',' in csv_location else csv_location.split(',')[0]

                first_check = check_csv_data(csv_birthday, csv_birthmonth, csv_birthyear)
                second_check = location_check(csv_location)

                if first_check and second_check:

                    # Ako osoba ima upisan alternativni naziv zemlje (npr. England umjesto UK),
                    # uzmi originalni naziv
                    if second_p_state_country in alternate_state_names:
                        country = alternate_state_names[second_p_state_country]
                        second_p_state_country = country
                        second_p_city = country

                    # Ako imamo neameričku državu/zemlju (npr. England), uzmi kao grad glavni grad zemlje
                    if second_p_state_country == second_p_city:
                        if second_p_city not in american_states_capitals():
                            country = CountryInfo(second_p_city)
                            if country:
                                second_p_city = country.capital()
                                # Fix - ako se u imenu države nalaze dijakritički znakovi iz drugih jezika
                                for key, value in alternate_characters.items():
                                    if key in second_p_city:
                                        second_p_city = second_p_city.replace(key, value)

                    # Ako se radi samo o državi
                    if not ',' in csv_location:
                        # ako ta država ima iznimku (drugi naziv)
                        if csv_location in alternate_state_names:
                            country = alternate_state_names[csv_location]
                            second_p_state_country = country
                        if csv_location in american_states_capitals():
                            second_p_city = american_states_capitals()[csv_location]

                    # ako se radi o američkoj državi (npr. Houston, Texas)
                    if ',' in csv_location:
                        # država je prisutna u iznimci (drugi naziv)
                        if second_p_state_country in alternate_state_names:
                            country = alternate_state_names[second_p_state_country]
                            second_p_state_country = country
                        second_p_city = csv_location.split(',')[0]
                        # ako je grad prisutan u iznimci (drugi naziv)
                        if second_p_city in alternate_city_names:
                            second_p_city = alternate_city_names[second_p_city]

                    # Slučaj kada je država USA (Amerika), uzima se Washington kao glavni grad
                    if second_p_state_country == second_p_city and second_p_state_country == 'USA' and second_p_city == 'USA':
                        if second_p_city in american_states_capitals() and second_p_city in alternate_state_names.values():
                            second_p_state_country = 'USA'

                    if second_p_city in american_states_capitals() and second_p_city in alternate_state_names.values():
                        second_p_state_country = 'USA'

                    # Find the input field by name attribute
                    input_field13 = driver.find_element(By.NAME, "city2")

                    # Clear any existing value in the input field
                    input_field13.clear()

                    # Send individual key events to input the string of city
                    for char in second_p_city:
                        input_field13.send_keys(char)
                        # Simulate a keydown event for each character
                        input_field13.send_keys(Keys.DOWN)
                        # Wait time in seconds
                        time.sleep(5)

                    index = None
                    american_state_flag = 'empty'
                    # Wait for the suggestions to appear
                    try:
                        suggestion_list2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "autoSuggestionsList2")))
                        city_state2 = list(suggestion_list2.text.split('\n'))
                        second_p_state_country2 = ''
                        for item in city_state2:
                            # if not ',' in csv_location:
                            alternate_state_string = get_key_from_value(alternate_state_names, second_p_state_country)
                            # Exclusion for USA only
                            if second_p_state_country == 'USA':
                                alternate_state_string = second_p_state_country
                            if second_p_state_country in american_states_capitals() or csv_location in american_states_capitals() or alternate_state_string in american_states_capitals():
                                american_state_flag = 'US'
                            if alternate_state_string:
                                alternate_state_string2 = alternate_state_string[:3].upper()
                                alternate_state_string3 = alternate_state_string[:2].upper()
                                if second_p_state_country == 'USA' and second_p_city == 'Washington':
                                    # Set country as DC (Washington DC) - District of Columbia
                                    second_p_state_country2 = 'DC'

                                if second_p_state_country in american_states_short():
                                    if second_p_city in item and american_states_short()[second_p_state_country] in item and american_state_flag in item:
                                        if second_p_state_country2 in item:
                                            index = city_state2.index(item)
                                else:
                                    if second_p_city in item and second_p_state_country[:2] in item and american_state_flag in item:
                                        if second_p_state_country2 in item:
                                            index = city_state2.index(item)
                                if second_p_state_country in item:
                                    if second_p_city in item and alternate_state_string in item:
                                        if second_p_state_country2 in item:
                                            index = city_state2.index(item)
                                if second_p_city in item and alternate_state_string2 in item:
                                    if second_p_state_country2 in item:
                                        index = city_state2.index(item)
                                if second_p_city in item and alternate_state_string3 in item:
                                    if second_p_state_country2 in item:
                                        index = city_state2.index(item)
                                if second_p_city in item and american_state_flag in item and second_p_state_country[:2] in item and second_p_city in item and american_state_flag in item:
                                    if second_p_state_country2 in item:
                                        index = city_state2.index(item)
                            else:
                                if second_p_city in item and second_p_state_country[:2].upper() in item or second_p_city in item and american_state_flag in item:
                                    index = city_state2.index(item)
                                    break
                            # if ',' in csv_location:
                            #     if second_p_state_country in item:
                            #         index = city_state2.index(item)
                            #         break
                        # Find all suggestion items
                        suggestion_item2 = WebDriverWait(suggestion_list2, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
                        # Click on the suggestion linked by index
                        if str(index).isdigit():
                            suggestion_item2[index].click()
                        else:
                            suggestion_item2[0].click()

                    except TimeoutException:
                        print("Timeout occurred while waiting for the suggestion list to appear.")

                    # Print check for data
                    if str(index).isdigit():
                        print('Country: %s, City: %s,   ==> %s' % (second_p_state_country, second_p_city, city_state2[index]))
                        # row.append('Country: %s, City: %s,   ==> %s' % (second_p_state_country, second_p_city, city_state2[index]))
                    else:
                        if len(city_state2) != 0:
                            print('Country: %s, City: %s,   ==> %s' % (second_p_state_country, second_p_city, city_state2[0]))
                            # row.append('Country: %s, City: %s,   ==> %s' % (second_p_state_country, second_p_city, city_state2[0]))

                    # Find the input field by name attribute
                    input_field7 = driver.find_element(By.NAME, "name2")

                    # Clear any existing value in the input field
                    input_field7.clear()

                    # Enter your custom string value in the input field
                    input_field7.send_keys(second_p_name)

                    # Find the input field by name attribute
                    input_field_month2 = driver.find_element(By.NAME, "month2")

                    # Send custom string in input_field
                    input_field_month2.send_keys(str(second_p_bday_month))

                    # Find the input field by name attribute
                    input_field9 = driver.find_element(By.NAME, "day2")

                    # Clear any existing value in the input field
                    input_field9.clear()

                    # Enter your custom string value in the input field
                    input_field9.send_keys(second_p_bday)

                    # Find the input field by name attribute
                    input_field10 = driver.find_element(By.NAME, "year2")

                    # Clear any existing value in the input field
                    input_field10.clear()

                    # Enter your custom string value in the input field
                    input_field10.send_keys(second_p_bday_year)

                    # Find the input field by name attribute
                    input_field11 = driver.find_element(By.NAME, "hour2")

                    # Clear any existing value in the input field
                    input_field11.clear()

                    # Enter your custom string value in the input field
                    input_field11.send_keys("12")

                    # Find the input field by name attribute
                    input_field12 = driver.find_element(By.NAME, "minute2")

                    # Clear any existing value in the input field
                    input_field12.clear()

                    # Enter your custom string value in the input field
                    input_field12.send_keys("00")

                    # Find the select field by name attribute
                    select_field_amorpm2 = Select(driver.find_element(By.NAME, "amorpm2"))

                    # Use the select field as needed
                    # For example, you can select an option by value
                    select_field_amorpm2.select_by_value('AM')

                    # END OF SECOND PERSON FILLING
                    ########################################################################################

                    # Wait for the submit button to be clickable for 3 seconds
                    time.sleep(3)

                    # Locate the submit button using its value attribute
                    submit_button = driver.find_element(By.XPATH, "//input[@value='Process the above data']")

                    # Click on the submit button to submit the form
                    # submit_button.submit()

                    # Execute JavaScript to submit the form
                    driver.execute_script("arguments[0].click();", submit_button)

                    # Wait for the new window to open and switch to it
                    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

                    # Get the handles of all the open windows
                    window_handles = driver.window_handles

                    # Switch the focus to the newly opened window
                    driver.switch_to.window(window_handles[-1])

                    # Wait for the page to load including JavaScript-generated content
                    wait = WebDriverWait(driver, 20)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))

                    # Storing the whole source of the page
                    page_source = driver.page_source

                    # Create a BeautifulSoup object to parse the HTML
                    soup = BeautifulSoup(page_source, "html.parser")

                    # Look for links
                    links = soup.find_all("a")[0]

                    # get link url
                    url = links.get('href')

                    pdf_url = url

                    # Download the PDF file
                    try:
                        result = fetch_url(pdf_url)
                        # print(result)
                    except ConnectionError as e:
                        print(f"Connection error - Failed to fetch URL after multiple retries: {e}")

                    with open("downloaded_pdf.pdf", "wb") as pdf_file:
                        pdf_file.write(result)

                    # Open and read the PDF file
                    with open("downloaded_pdf.pdf", "rb") as pdf_file:
                        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

                        # Extract text from each page
                        for page_num in range(1):
                            page = pdf_reader.getPage(page_num)
                            text = page.extractText()

                            # Process the extracted text as needed
                            final_score = text.split('The dual ')[1].split('Negative')[0]
                            print(final_score.replace('_', ' '))

                    # Upis u csv file person_data_score.csv
                    # row.append(final_score)
                    # csv_writer.writerow(row)

                    # Optionally, delete the downloaded PDF file after processing
                    os.remove("downloaded_pdf.pdf")

                    # # Keep the browser open for viewing
                    # input("Press any key to close the browser...")

                    # Close the browser
                    driver.quit()

                else:
                    driver.quit()


if __name__ == '__main__':
    main()
