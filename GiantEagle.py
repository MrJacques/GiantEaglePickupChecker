# MIT License
#
# Copyright (c) 2020 Jacques Parker  copyright@judyandjacques.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import logging
import sys
import time
from os import path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twilio.rest import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# If this file exist then the script will exit immediately
DISABLE_FILE_NAME = "GiantEagle.disable"

check_count = 0

with open('GiantEagle.json') as f:
    data = json.load(f)

assert (len(data['giant eagle']['login']) > 0)
assert (len(data['giant eagle']['password']) > 0)
assert (len(data['twilio']['account_sid']) > 0)
assert (len(data['twilio']['auth_token']) > 0)
assert (len(data['twilio']['from_phone']) > 0)
assert (len(data['twilio']['to_phones']) > 0)
assert (len(data['store']) > 0)
assert (data['mode'] in ['continuous', 'single'])
if data['mode'] == 'continuous':
    assert (data['delay'] >= 0)

giant_eagle_login = data['giant eagle']['login']
giant_eagle_password = data['giant eagle']['password']
twilio_sid = data['twilio']['account_sid']
twilio_token = data['twilio']['auth_token']
twilio_from_phone = data['twilio']['from_phone']
twilio_to_phones = data['twilio']['to_phones']
# twilio_test_sid = data['twilio']['test']['account_sid']
# twilio_test_token = data['twilio']['test']['auth_token']
# twilio_test_from = data['twilio']['test']['test_from']

# mode should be "continuous" or "single"
mode = data['mode']
logging.info("mode: %s" % mode)

# delay between attempts
delay_seconds = data['delay']
if mode == 'continuous':
    logging.info("Delay: %d seconds" % delay_seconds)

store_url = "https://curbsideexpress.gianteagle.com/store/%s#/landing" % data['store']
logging.info("Store landing URL: %s" % store_url)

options = Options()
options.headless = False
if options.headless:
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)  # seconds
wait = WebDriverWait(driver, 60)
wait_short = WebDriverWait(driver, 15)

while True:
    if path.exists(DISABLE_FILE_NAME):
        logging.critical("Disabled")
        sys.exit(0)

    check_count += 1
    logging.info("Open web page %d" % check_count)

    driver.get(store_url)

    if check_count > 1:
        logging.info("Get rid of leave confirmation")
        leave_alert = driver.switch_to.alert
        leave_alert.accept()

    logging.info("Wait for pop-up")
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[1]/div[2]/div[1]/button')))

    logging.info("Get rid of pop up")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    logging.info("Click reserve button")
    reserve_button = driver.find_elements_by_xpath('//*[@id="js-topHeader"]/div/div[2]/div/div[6]/div[1]/button')
    reserve_button[0].click()

    logging.info("Switch to login")
    login_window_found = False
    try:
        wait_short.until(EC.number_of_windows_to_be(2))
        login_window_found = True
    except TimeoutException:
        logging.info("No login window")

    if login_window_found:
        parent = driver.window_handles[0]
        child = driver.window_handles[1]
        driver.switch_to.window(child)

        email = driver.find_element_by_id("UserName")
        email.send_keys(giant_eagle_login)

        password = driver.find_element_by_id("Password")
        password.send_keys(giant_eagle_password)
        password.send_keys(Keys.ENTER)

        logging.info("Logged in...")
        driver.switch_to.window(parent)

    logging.info("Click pickup")
    pickup = driver.find_element_by_xpath('//*[@id="fulfillment"]/section/div[2]/div[1]/button[1]/span')
    pickup.click()

    logging.info("Click Monthly View")
    monthly_view = driver.find_element_by_xpath('//*[@id="fulfillment"]/div/section[1]/div[1]/div[2]/a[1]')
    monthly_view.click()

    logging.info("Click view list of dates")
    view_list = driver.find_element_by_xpath('//*[@id="fulfillment"]/div/section[1]/div[2]/div[1]/a')
    view_list.click()

    logging.info("Waiting for drop down")
    time.sleep(15)

    date_picker = driver.find_element_by_xpath('//*[@id="fulfillment"]/div/section[1]/div[2]/div[2]/select')

    options = [x for x in date_picker.find_elements_by_tag_name("option")]
    logging.info("Options:")

    values = []
    for element in options:
        value = element.get_attribute("value")
        if len(value) > 1:
            logging.info("-", value)
            values.append(value)

    logging.info("Number of Options: %d" % len(values))

    if len(values) > 0 or len(options) > 1:
        logging.critical("Found options.  Disabling future checks")
        with open(DISABLE_FILE_NAME, 'w') as fp:
            pass

        logging.critical("Sending text")

        # live creds
        client = Client(twilio_sid, twilio_token)

        # test credentials
        # client = Client(twilio_test_sid, twilio_test_token)
        # twilio_from_phone = twilio_test_from

        for to_phone in twilio_to_phones:
            client.messages.create(
                to=to_phone,
                from_=twilio_from_phone,
                body="Giant Eagle Alert, Pickups for the following dates found: " + ",".join(values))

        break

    if mode == "single":
        break

    if delay_seconds > 0:
        logging.info("Sleeping between attempts (%d seconds)" % delay_seconds)
        time.sleep(delay_seconds)

driver.close()
