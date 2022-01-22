""" Завдання_1

За допомогою браузера (Selenium) відкрити форму за наступним посиланням:

https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform?usp=sf_link

заповнити і відправити її.
Зберегти два скріншоти: заповненої форми і повідомлення про відправлення форми.
В репозиторії скріншоти зберегти.
"""

# from selenium import webdriver
from multiprocessing.connection import wait
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path


class SendFrom(object):

    # Browser parameters for startup
    options = ChromeOptions()
    options.add_argument("--no-sandbox")

    # Link to the form which must be filled.a
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform?usp=sf_link"

    # Select webdriver path and open browser
    webdriver_path = Path(Path.cwd(), "chromedriver")
    wd = Chrome(options=options, executable_path=webdriver_path)

    # Open form link, wait 10 sec and filled it: input name of user.
    wd.get(form_link)
    input_field = WebDriverWait(wd, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".quantumWizTextinputPaperinputInput")))
    input_field.send_keys("Karbivnychyi Volodymyr")

    # Make a first screenshot: as a pruf of filled form.
    first_screenshot = wd.save_screenshot("filled_form_screenshot.png")

    # Find send button and click to send from.
    send_button = WebDriverWait(wd, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".appsMaterialWizButtonPaperbuttonLabel")))
    send_button.click()

    # Make a second screenshot: as a pruf of sent form.
    second_screenshot = wd.save_screenshot("sent_form_screenshot.png")

    # Close the browser and finished scripts
    wd.quit()
