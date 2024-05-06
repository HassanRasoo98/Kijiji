# main.py
from fastapi import FastAPI
import uvicorn
from time import sleep
import selenium
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


app = FastAPI()

@app.get('/')
def home():
    return "welcome to kijiji bot"

@app.get('/flow/')
def flow():
    # Store the current directory
    original_dir = os.getcwd()
    original_dir

    url = 'https://www.kijiji.ca/'

    user = 'johnricky4549@gmail.com'
    password = 'Jamnager4549$'

    driver = webdriver.Chrome()
    # Maximize the browser window
    driver.maximize_window()
    driver.get(url)

    # Find the first option and click it
    first_option = driver.find_element(By.CSS_SELECTOR, ".locMenu.drop-down.level-1 li:first-child a")
    first_option.click()

    time.sleep(5)

    # Find the first option and click it
    first_option = driver.find_element(By.CSS_SELECTOR, ".locMenu.drop-down.level-2 li:first-child a")
    first_option.click()

    time.sleep(5)

    # Find the "Go" button and click it
    go_button = driver.find_element(By.ID, "LocUpdate")
    go_button.click()

    time.sleep(5)

    # Find the "Sign In" link and click it
    sign_in_link = driver.find_element(By.XPATH, "//a[@title='Sign In']")
    sign_in_link.click()

    time.sleep(5)

    # Find the email and password input fields and enter your credentials
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(user)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Click the sign in button
    sign_in_button = driver.find_element(By.ID, "login-submit")
    sign_in_button.click()

    # Navigate to the "KijijiBot" folder
    folder_path = "KijijiBot"
    os.chdir(folder_path)

    # Get a list of files in the folder
    files = os.listdir()

    # Filter Excel files
    excel_files = [file for file in files if file.endswith('.xlsx')]

    # Display Excel files found
    if excel_files:
        print("Excel files found in the 'KijijiBot' folder:")
        for file in excel_files:
            print(file)
        # Read the first Excel file into a DataFrame and display it
        first_excel_file = excel_files[0]
        df = pd.read_excel(first_excel_file)
        print("\nDataFrame extracted from the first Excel file:")
    else:
        print("No Excel files found in the 'KijijiBot' folder.")

    df

    # Deletion of ads automatically all 4 ads

    def deleteAds():
        for i in range(3):
            try:
                driver.get('https://www.kijiji.ca/m-my-ads/active/1')
                time.sleep(3)
                # Find the delete button element using its data-testid attribute
                delete_button = driver.find_element(By.XPATH, "//button[@data-testid='adDeleteButton']")

                # Click the delete button
                delete_button.click()
                time.sleep(2)

                # Find the button element by its data-testid attribute
                button = driver.find_elements(By.CSS_SELECTOR, "button[data-testid='pill-option']")[-1]

                # Click the button
                button.click()

                time.sleep(5)

                # Find the button element by its text
                button = driver.find_element(By.XPATH, "//button[text()='Delete My Ad']")

                # Click the button
                button.click()

                time.sleep(5)

                # Find the button element by its ID
                close_button = driver.find_element(By.ID, "modalCloseButton")

                # Click the button
                close_button.click()
            except:
                pass

    while True:
        for j in range(len(df) -1):
            # Find the "Post ad" link and click it
            post_ad_link = driver.find_element(By.XPATH, "//a[@aria-label='Post ad']")
            post_ad_link.click()
            # Assuming df is your DataFrame containing the 'Title' column
            first_title = df['Title'].iloc[j]

            # Find the textarea element and enter the text
            textarea_element = driver.find_element(By.ID, "AdTitleForm")
            textarea_element.clear()  # Clear any existing text
            textarea_element.send_keys(first_title)

            # Wait for the button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='CategorySuggestion']"))
            )

            # Click the button
            next_button.click()

            time.sleep(5)

            button_texts = df['Category'].iloc[j].split(',')[1:]
            # Loop through the list
            for text in button_texts:
                time.sleep(2)
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'categoryName-') and text()='{text}']/ancestor::button"))
                )

                # Click the button
                button.click()

            try:
                price = int(df['Price'].iloc[j])
                # Find the input field
                input_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "PriceAmount"))
                )

                # Clear the input field (in case there's any existing value)
                input_field.clear()

                # Input the price into the text field
                input_field.send_keys(price)
            except:
                pass

            # Assuming you have the description stored in a variable called 'description'
            description = df['Description'].iloc[j]  # Example description

            # Find the textarea field
            textarea_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pstad-descrptn"))
            )

            # Clear the textarea field (in case there's any existing value)
            textarea_field.clear()

            # Input the description into the textarea field
            textarea_field.send_keys(description)

            try:
                # Given text to match
                given_text = df['Condition'].iloc[j]

                # Find the select element
                select_element = driver.find_element(By.ID, "condition_s")

                # Get all options
                options = select_element.find_elements(By.TAG_NAME, "option")

                # Initialize variables to keep track of maximum similarity score and selected option
                max_score = -1
                selected_option = None

                # Iterate through each option
                for option in options:
                    # Get the text of the option
                    option_text = option.text

                    # Calculate similarity score between the option text and given text
                    score = fuzz.ratio(given_text.lower(), option_text.lower())

                    # Update selected option if the current score is higher
                    if score > max_score:
                        max_score = score
                        selected_option = option

                # Select the option with the highest similarity score
                selected_option.click()
            except:
                pass

            try:
                # Sample text to match
                given_text = df['PhoneBrand'].iloc[j]
                if pd.isna(given_text):
                    given_text = df['Tablet Brand'].iloc[j]
                    if pd.isna(given_text):
                        given_text = df['Laptop Brand'].iloc[j]
                        select_element = driver.find_element(By.ID, "laptopbrand_s")
                    else:
                        select_element = driver.find_element(By.ID, "tabletbrand_s")
                else:
                    select_element = driver.find_element(By.ID, "phonebrand_s")

                # Extract options and their values
                options = [(option.text, option.get_attribute("value")) for option in Select(select_element).options]

                # Find the option with the maximum similarity to the given text
                max_similarity = 0
                best_match = None
                for text, value in options:
                    similarity = fuzz.partial_ratio(given_text.lower(), text.lower())
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_match = (text, value)
                        # print(best_match[1])

                # Select the best matching option
                if best_match:
                    Select(select_element).select_by_value(best_match[1])
            except:
                try:
                    Select(select_element).select_by_value("other")
                except:
                    pass

            try:
                given_text = df['laptop Screen Size'].iloc[j]
                if pd.isna(given_text):
                    given_text = df['PhoneBrandCarrier'].iloc[j]
                    if pd.isna(given_text):
                        given_text = df['Job Type'].iloc[j]
                        select_element = driver.find_element(By.ID, "jobtype_s")
                        # Extract options and their values
                        options = [(option.text, option.get_attribute("value")) for option in Select(select_element).options]

                        # Find the option with the maximum similarity to the given text
                        max_similarity = 0
                        best_match = None
                        for text, value in options:
                            similarity = fuzz.partial_ratio(given_text.lower(), text.lower())
                            if similarity > max_similarity:
                                max_similarity = similarity
                                best_match = (text, value)
                                # print(best_match[1])

                        # Select the best matching option
                        if best_match:
                            Select(select_element).select_by_value(best_match[1])
                    else:
                        select_element = driver.find_element(By.ID, "phonecarrier_s")
                        # Extract options and their values
                        options = [(option.text, option.get_attribute("value")) for option in Select(select_element).options]

                        # Find the option with the maximum similarity to the given text
                        max_similarity = 0
                        best_match = None
                        for text, value in options:
                            similarity = fuzz.partial_ratio(given_text.lower(), text.lower())
                            if similarity > max_similarity:
                                max_similarity = similarity
                                best_match = (text, value)
                                # print(best_match[1])

                        # Select the best matching option
                        if best_match:
                            Select(select_element).select_by_value(best_match[1])
                else:
                    select_element = driver.find_element(By.ID, "laptopscreensize_s")
                    # Extract options and their values
                    options = [(option.text, option.get_attribute("value")) for option in Select(select_element).options]

                    # Find the option with the maximum similarity to the given text
                    max_similarity = 0
                    best_match = None
                    for text, value in options:
                        similarity = fuzz.partial_ratio(given_text.lower(), text.lower())
                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_match = (text, value)
                            # print(best_match[1])

                    # Select the best matching option
                    if best_match:
                        Select(select_element).select_by_value(best_match[1])
            except:
                pass

            os.chdir(original_dir)
            # Base directory where Kijiji folder is located
            base_dir = 'KijijiBot\\'
            # List to store image paths
            image_paths = []
            folder_name = df['Images_FolderName'].iloc[j]

            # Perform fuzzy matching to find the closest matching folder name
            matched_folder_name, score = process.extractOne(folder_name, os.listdir(base_dir))

            # Construct the full path to the folder
            folder_path = os.path.join(base_dir, matched_folder_name)

            # Check if the folder exists
            if os.path.exists(folder_path):
                # Iterate through files in the folder
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        # Assuming images have specific extensions like .jpg, .png, etc.
                        if file.endswith(('.jpg', '.jpeg', '.png')):
                            # Construct the full path to the image file
                            image_path = os.path.join(root, file)
                            # Append the image path to the list
                            image_paths.append(image_path)

            for imger in image_paths:
                time.sleep(1)

                # Wait for the parent div container to be present
                container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "moxie-shim-html5"))
                )

                # Find the input element within the container
                file_input = container.find_element(By.TAG_NAME, "input")

                # Provide the path to the image file you want to upload
                image_path = os.path.join(original_dir, imger)
                image_path = image_path.replace('\\\\', '\\')

                # Send the image file path to the file input field
                file_input.send_keys(image_path)

            # Assuming you have a DataFrame named df and it contains a column named "Phone"
            phone_number = int(df["Phone"].iloc[j]) # Assuming you want the first phone number from the DataFrame

            # Find the input field by ID
            phone_input = driver.find_element(By.ID, "PhoneNumber")

            # Clear any existing value in the input field
            phone_input.clear()

            # Enter the phone number from the DataFrame into the input field
            phone_input.send_keys(phone_number)

            # Assuming you have a list of tags named 'tags_list'
            tags_list = df['Tags'].iloc[j].split(',')  # Example list of tags

            # Find the input field for adding tags
            tags_input = driver.find_element(By.ID, "pstad-tagsInput")

            # Find the "Add" button
            add_button = driver.find_element(By.CLASS_NAME, "addButton-1177096964")

            # Loop through each tag in the list
            for tag in tags_list:
                # Clear any existing value in the input field
                tags_input.clear()

                # Enter the current tag into the input field
                tags_input.send_keys(tag)

                # Optionally, wait for a short while to allow suggestions to appear
                time.sleep(5)

                # Click the "Add" button
                add_button.click()

                # Optionally, wait for a moment before proceeding to the next tag entry
                time.sleep(5)


            # Find the button element using its data-testid attribute
            post_ad_button = driver.find_element(By.XPATH, "//button[@data-testid='checkout-post-btn']")

            # Click the button
            post_ad_button.click()

            time.sleep(3)
        
        time.sleep(21600) # This waits for 6 hours to post new same ads and deletes the previous after 6 hours...
        
        deleteAds() # This delete the first 3 ads only as 4th is not have full information...


if __name__ == '__main__':
    uvicorn.run(app, port=8000)