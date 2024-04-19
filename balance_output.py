import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Specify the path to your Chromedriver executable
chrome_driver_path = 'chromedriver.exe'

# Create ChromeOptions object and set it to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Initialize the WebDriver with the Service object and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://allengroups.net/online-recharge/')
card_number = input("Enter your card number: ")
driver.find_element(By.NAME, 'cardno').send_keys(card_number)
password = input("Enter your password: ")
driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

try:
    # Switch to any iframes if present
    # driver.switch_to.frame("frame_name_or_id")  # Use this if you know the frame name or ID

    # Wait for the balance label element to be present in the DOM
    wait = WebDriverWait(driver, 20)  # Increased timeout to 20 seconds
    balance_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), "
                                                                         "'Smart Card Balance')]")))

    # Check if the balance label is visible
    if balance_label.is_displayed():
        # Extract the balance value from the label text
        balance_text = balance_label.text.strip()
        balance = balance_text.split('₹ ')[1] if '₹' in balance_text else None  # Extract the balance value

        if balance is not None:
            # Create a JSON object to store the balance
            balance_data = {
                "smart_card_balance": balance
            }

            # Convert the JSON object to a string and print it
            balance_json_str = json.dumps(balance_data, indent=4)
            # print(balance_json_str)
            # Print custom message with balance amount
            print(f"Your balance amount is ₹ {balance}.")
        else:
            print('Failed to retrieve balance.')
    else:
        print('Balance label is not visible.')

except TimeoutException:
    print("Timed out waiting for balance element to load.")
except NoSuchElementException:
    print("Balance label element not found.")

# Close the WebDriver
driver.quit()
