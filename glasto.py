from datetime import datetime
import random
import time

# You will need to run "pip3 install -U selenium" from the command line to install selenium
# You also need Chrome for Testing: https://googlechromelabs.github.io/chrome-for-testing/
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# If you know the full URL for the ticket sale put it in here and then start the script
# start the script from the command line by running "python glasto.py"
# event_url = 'https://glastonbury.seetickets.com/event/glastonbury-2024-deposits/worthy-farm/2500000'

# OR - start the script before the ticket sale using the below
#      ... and the script will atempt to click the main ticket sale link when it becomes active
event_url = 'https://glastonbury.seetickets.com/content/extras'

# Set this to True or False
# True will press the "Proceed" button for you once it fills in the registration details
# False will mean you will need to press it yourself
submit_form = True

# The list of your registration details
# You can have up to 6
registrations = [
            {
                "registration": "1234567890",
                "postcode": "AB12 3XY"
            }
            ,
            {
                "registration": "0987654321",
                "postcode": "AB12 3XY"
            }
        ]

def check(element_type:str, element: str, refresh: bool=True):
    try:

        driver.find_element(element_type, element)

        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} SUCCESS - Registration page detected!!')

        for count, value in enumerate(registrations):
            data = driver.find_element('name', f'registrations[{count}].RegistrationId')
            data.send_keys(value['registration'])
            data = driver.find_element('name', f'registrations[{count}].PostCode')
            data.send_keys(value['postcode'])

        if submit_form:
            driver.find_element(element_type, element).submit()

        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} My work is done. Good luck!')

    except NoSuchElementException:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Registration page not detected.')

        if not refresh:
            return False

        refresh_rate = random.uniform(1.1, 2.0)

        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Sleeping for {refresh_rate} seconds...')
        time.sleep(refresh_rate)
        driver.refresh()
        check(element_type=element_type, element=element)

print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Starting Up...')
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(event_url)

# Try and automatically accept the GDPR notice.
try:
    gdpr = driver.find_element(By.CLASS_NAME, 'g-button.secondary.gdpr-accept')
    gdpr.click()
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Accepted the GDPR banner.')
except NoSuchElementException:
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Could not find the GDPR banner to accept.')

# If we started on the homepage, try and automatically click the event url when it becomes live
while "glastonbury.seetickets.com/content/extras" in driver.current_url:
    try:
        site = driver.find_element(By.CLASS_NAME, 'g-button.primary.full')
        site.click()
        refresh_rate = random.uniform(1.1, 2.0)
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Sleeping for {refresh_rate} seconds...')
        time.sleep(refresh_rate)
        driver.refresh()
    except NoSuchElementException:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Something has gone wrong.')

# Check if the page we are on contains the registration form
check(element_type='name', element='registrations[0].RegistrationId')
