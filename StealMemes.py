from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests
import shutil
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


os.system("cls" if os.name == "nt" else "clear")
date = datetime.now().strftime('%d.%m.%Y')


try:
    category = sys.argv[1] # (either day, week, month or year)  
except IndexError:
    print('Syntax invalid, missing category.')
    print('The syntax is: python ifunny.py [day|week|month|year]')
    sys.exit()
if category.lower() not in ['day', 'week', 'month', 'year']:
        print('Syntax invalid, given category not in available categories.')
        print('The syntax is: python ifunny.py [day|week|month|year]')
        sys.exit()


folder = f'{category} - {date}'

PATH = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(f"{PATH}/{folder}"):
    os.mkdir(f"{PATH}/{folder}")


def steal_memes():
    url = f"https://ifunny.co/top-memes/{category}"

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    for page in range(1, 5):  # There are 4 pages of memes, 1-4
        data = requests.get(f"{url}/page{page}")
        soup = BeautifulSoup(data.text, "lxml")
        meme_list = soup.find("ul", {"class", "stream js-playlist-container grid js-grid-container"})
        meme_list = [li for li in meme_list if type(li.find("img")) is not int]  # Filter to get meme list items
        for index, li in enumerate(meme_list, 1):
            if "Icon grid__icon grid__icon-big grid__icon_center" in str(li):  # Detects if video
                driver.get("https://ifunny.co" + li.find("a")["href"])
                driver.find_element_by_xpath("//*[@id=\"js-app\"]/div[2]/div[2]/div[2]/div[1]/ul/li[1]/div/div""[2]"
                                             "").click()  # Click executes video javascript
                try:
                    meme_link = WebDriverWait(driver, 2).until(ec.presence_of_element_located(
                        (By.TAG_NAME, "video"))).get_attribute("src")  # Waits at most 2 seconds for video to load
                except TimeoutException:
                    print(f"[{index + 50 * (page - 1)}] ERROR: Failed to download video.")
                    continue
                extension = meme_link.split(".")[-1]
                meme = requests.get(meme_link, stream=True)
                with open(f"{PATH}/{folder}/meme_{page}_{index}.{extension}", "wb") as f:
                    shutil.copyfileobj(meme.raw, f)
            else:  # Deal with image memes
                meme_link = li.find("img")["data-src"]
                extension = meme_link.split(".")[-1]
                meme = requests.get(meme_link, stream=True)
                with open(f"{PATH}/{folder}/meme_{page}_{index}.{extension}", "wb") as f:
                    shutil.copyfileobj(meme.raw, f)
            print(f"[{index + 50 * (page - 1)}] New Meme From {meme_link}!")  # Always 50 memes on pages 1-3
    print('All memes downloaded !')
    driver.quit()

steal_memes()
