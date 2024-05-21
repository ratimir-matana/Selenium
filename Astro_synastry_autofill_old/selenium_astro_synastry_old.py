import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re

x = 1

while x == 1:

    available_states = []

    first_p_name = input("Unesite ime prve osobe: ")
    first_p_bday = input("Unesite dan rođenja prve osobe: ")
    first_p_bday_month = input("Unesite mjesec rođenja prve osobe: ")
    first_p_bday_year = input("Unesite godinu rođenja prve osobe: ")
    first_p_state_country = input("Unesite državu/zemlju prve osobe: ")
    first_p_city = input("Unesite grad prve osobe: ")

    second_p_name = input("Unesite ime druge osobe: ")
    second_p_bday = input("Unesite dan rođenja druge osobe: ")
    second_p_bday_month = input("Unesite mjesec rođenja druge osobe: ")
    second_p_bday_year = input("Unesite godinu rođenja druge osobe: ")
    second_p_state_country = input("Unesite državu/zemlju druge osobe: ")
    second_p_city = input("Unesite grad druge osobe: ")

    # Specify the path to the GeckoDriver executable
    gecko_driver_path = '/usr/local/bin/geckodriver'

    # Create a Service object with the specified GeckoDriver executable path
    service = Service(gecko_driver_path)

    # Create a new instance of the Firefox driver using the Service object
    driver = webdriver.Firefox(service=service)

    # Test Selenium by opening a website
    driver.get("https://a*******.org/scripts/synastry_chart_acs.php")

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
    search_state = [state for state in available_states if re.search(first_p_state_country, state, re.IGNORECASE)]

    if search_state:
        print("State found:", search_state[0])
    else:
        print("No state found!")

    # For example, you can select an option by value
    select_field2.select_by_visible_text(search_state[0])

    # Find the input field by name attribute
    input_field6 = driver.find_element(By.NAME, "city1")

    # Clear any existing value in the input field
    input_field6.clear()

    # Enter your custom string value in the input field
    input_field6.send_keys(first_p_city)

    # Wait for the suggestions to appear
    try:
        suggestion_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "autoSuggestionsList1")))

        # Click on the first suggestion
        suggestion_item = WebDriverWait(suggestion_list, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
        suggestion_item.click()

    except TimeoutException:
        print("Timeout occurred while waiting for the suggestion list to appear.")

    # END OF FIRST PERSON FILLING
    ########################################################################################

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
    select_field3.select_by_value(second_p_bday_month)

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

    for state in select_field4.options:
        available_states.append(state.accessible_name)

    # Use regex to search for a case-insensitive match
    search_state = [state for state in available_states if re.search(second_p_state_country, state, re.IGNORECASE)]

    if search_state:
        print("State found:", search_state[0])
    else:
        print("No state found!")

    # For example, you can select an option by value
    select_field4.select_by_visible_text(search_state[0])

    # Find the input field by name attribute
    input_field12 = driver.find_element(By.NAME, "city2")

    # Clear any existing value in the input field
    input_field12.clear()

    # Enter your custom string value in the input field
    input_field12.send_keys(second_p_city)

    # Wait for the suggestions to appear
    try:
        suggestion_list2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "autoSuggestionsList2")))

        # Click on the first suggestion
        suggestion_item2 = WebDriverWait(suggestion_list2, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
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
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # Get the handles of all the open windows
    window_handles = driver.window_handles

    # Switch the focus to the newly opened window
    driver.switch_to.window(window_handles[-1])

    # Wait for the page to load including JavaScript-generated content
    wait = WebDriverWait(driver, 10)
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

    print(score_text)

    # Close the browser
    driver.quit()
