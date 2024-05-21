import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
import csv
from countryinfo import CountryInfo


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


def main():
    search_state1 = []
    search_state2 = []
    available_states = []
    alternate_state_names = {'England': 299, 'NE': 16, 'USA': 81}
    filename = '/home/*****/Wiki Celebrity Birthdays/person_data.csv'
    # Open the data in the CSV file
    with open(filename, 'r', newline='') as csvfile:
        csv_read = csv.reader(csvfile)
        # Skip the first row (header)
        next(csv_read)
        for row in csv_read:
            available_states.clear()
            search_state1.clear()
            search_state2.clear()
            csv_name = row[0].replace('_', ' ') if '_' in row[0] else row[0]
            # csv_birthdate = row[1]
            if row[1] in ['Unknown']:
                continue
            csv_birthmonth = month_to_number(row[1].split(' ')[0])
            csv_birthday = row[1].split(' ')[1].split(',')[0]
            csv_birthyear = row[1].split(',')[1][1:]
            csv_location = row[2]

            first_p_name = "FirstPerson"
            first_p_bday = "21"
            first_p_bday_month = "1"
            first_p_bday_year = "1989"
            first_p_state_country = "Croatia"
            first_p_city = "Zagreb"

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
            driver.get("https://a****.org/scripts/synastry_chart_acs.php")

            # Find the input field by name attribute
            input_field1 = driver.find_element(By.NAME, "name1")

            # Clear any existing value in the input field
            input_field1.clear()

            # Enter your custom string value in the input field
            input_field1.send_keys(first_p_name)

            # Find the select field by name attribute
            select_field1 = Select(driver.find_element(By.NAME, "month1"))

            # Use the select field as needed
            # For example, you can select an option by value
            select_field1.select_by_value(first_p_bday_month)

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
            input_field4.send_keys("12")

            # Find the input field by name attribute
            input_field5 = driver.find_element(By.NAME, "minute1")

            # Clear any existing value in the input field
            input_field5.clear()

            # Enter your custom string value in the input field
            input_field5.send_keys("00")

            # Find the select field by name attribute
            select_field2 = Select(driver.find_element(By.NAME, "soc1"))

            for state in select_field2.options:
                available_states.append(state.accessible_name)

            # Use regex to search for a case-insensitive match
            search_state1 = [state for state in available_states if re.search(first_p_state_country, state, re.IGNORECASE)]

            if search_state1:
                print("State found:", search_state1[0])
            else:
                print("No state found!")

            # For example, you can select an option by value
            select_field2.select_by_visible_text(search_state1[0])

            # Find the input field by name attribute
            input_field6 = driver.find_element(By.NAME, "city1")

            # Clear any existing value in the input field
            input_field6.clear()

            # Enter your custom string value in the input field
            input_field6.send_keys(first_p_city)

            # Wait for the suggestions to appear
            try:
                suggestion_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "autoSuggestionsList1")))

                # Click on the first suggestion
                suggestion_item = WebDriverWait(suggestion_list, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "li")))
                suggestion_item.click()

            except TimeoutException:
                print("Timeout occurred while waiting for the suggestion list to appear.")

            # END OF FIRST PERSON FILLING
            ########################################################################################

            second_p_name = csv_name
            second_p_bday = csv_birthday
            second_p_bday_month = csv_birthmonth
            second_p_bday_year = csv_birthyear
            second_p_state_country = csv_location if not ',' in csv_location else csv_location.split(',')[1][1:]
            second_p_city = csv_location if not ',' in csv_location else csv_location.split(',')[0]

            first_check = check_csv_data(csv_birthday, csv_birthmonth, csv_birthyear)
            second_check = location_check(csv_location)
            if first_check and second_check:

                # Find the input field by name attribute
                input_field7 = driver.find_element(By.NAME, "name2")

                # Clear any existing value in the input field
                input_field7.clear()

                # Enter your custom string value in the input field
                input_field7.send_keys(second_p_name)

                # Find the select field by name attribute
                select_field3 = Select(driver.find_element(By.NAME, "month2"))

                # Use the select field as needed
                # For example, you can select an option by value
                select_field3.select_by_value(str(second_p_bday_month))

                # Find the input field by name attribute
                input_field8 = driver.find_element(By.NAME, "day2")

                # Clear any existing value in the input field
                input_field8.clear()

                # Enter your custom string value in the input field
                input_field8.send_keys(second_p_bday)

                # Find the input field by name attribute
                input_field9 = driver.find_element(By.NAME, "year2")

                # Clear any existing value in the input field
                input_field9.clear()

                # Enter your custom string value in the input field
                input_field9.send_keys(second_p_bday_year)

                # Find the input field by name attribute
                input_field10 = driver.find_element(By.NAME, "hour2")

                # Clear any existing value in the input field
                input_field10.clear()

                # Enter your custom string value in the input field
                input_field10.send_keys("12")

                # Find the input field by name attribute
                input_field11 = driver.find_element(By.NAME, "minute2")

                # Clear any existing value in the input field
                input_field11.clear()

                # Enter your custom string value in the input field
                input_field11.send_keys("00")

                # Find the select field by name attribute
                select_field4 = Select(driver.find_element(By.NAME, "soc2"))

                # for state in select_field4.options:
                #     available_states.append(state.accessible_name)

                # Use regex to search for a case-insensitive match
                search_state2 = [state for state in available_states if re.search(second_p_state_country, state, re.IGNORECASE)]

                if len(search_state2) == 1:
                    print("State found:", search_state2[0])
                else:
                    print("No state found!")

                # For example, you can select an option by value
                if search_state2:
                    if len(search_state2) == 1:
                        select_field4.select_by_visible_text(search_state2[0])
                    else:
                        if second_p_state_country in alternate_state_names:
                            country_code = alternate_state_names[second_p_state_country]
                            select_field4.select_by_visible_text(available_states[country_code])
                else:
                    if not ',' in csv_location:
                        if csv_location in alternate_state_names:
                            country_code = alternate_state_names[csv_location]
                            select_field4.select_by_visible_text(available_states[country_code])
                    if ',' in csv_location:
                        if second_p_state_country in alternate_state_names:
                            country_code = alternate_state_names[second_p_state_country]
                            select_field4.select_by_visible_text(available_states[country_code])

                # Find the input field by name attribute
                input_field12 = driver.find_element(By.NAME, "city2")

                # Clear any existing value in the input field
                input_field12.clear()

                # Take the capital of country
                if not search_state2 and available_states[country_code]:
                    country_get = available_states[country_code].split('|')[0]
                    country = CountryInfo(country_get)
                    if country_get in american_states_capitals():
                        second_p_city = country_get
                    else:
                        second_p_city = country.capital()

                if second_p_state_country == second_p_city:
                    if second_p_city not in american_states_capitals():
                        country = CountryInfo(second_p_city)
                        if country:
                            second_p_city = country.capital()

                    if second_p_city in american_states_capitals():
                        state_capitals = american_states_capitals()
                        state_capital = state_capitals[second_p_city]
                        input_field12.send_keys(state_capital)

                # Enter your custom string value in the input field
                input_field12.send_keys(second_p_city)

                # Wait for the suggestions to appear
                try:
                    suggestion_list2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "autoSuggestionsList2")))

                    # Click on the first suggestion
                    suggestion_item2 = WebDriverWait(suggestion_list2, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "li")))
                    suggestion_item2.click()

                except TimeoutException:
                    print("Timeout occurred while waiting for the suggestion list to appear.")

                # END OF SECOND PERSON FILLING
                ########################################################################################

                # Wait for the submit button to be clickable for 3 seconds
                time.sleep(3)

                # Locate the submit button using its value attribute
                submit_button = driver.find_element(By.XPATH, "//input[@value='Submit above data']")

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
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

                # Storing the whole source of the page
                page_source = driver.page_source

                # Create a BeautifulSoup object to parse the HTML
                soup = BeautifulSoup(page_source, "html.parser")

                # Look for tables
                tables = soup.find_all("table")

                # Look for table with final score
                if len(tables) > 1:
                    score_text = tables[3].text.split('Negative')[0]

                # # Keep the browser open for viewing
                # input("Press any key to close the browser...")

                if len(score_text) < 100:
                    print(score_text)
                    row.append(score_text)

                # Close the browser
                driver.quit()

            else:
                driver.quit()

    # TODO write the final scores in new csv file
    # filename = 'person_data_score.csv'
    # with open(filename, 'w', newline='') as csvfile_score:
    #     csv_writer = csv.writer(csvfile_score)
    #     csv_writer.writerow(row)


if __name__ == '__main__':
    main()
