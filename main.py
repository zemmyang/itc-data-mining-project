import config as CFG
import time
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lib_search import LibrarySearch


def extract_urls(url_to_click: str, wait_time: int, pause_time: int):
    # selenium web scrapper for infinite scrolling page
    driver = webdriver.Chrome(executable_path=os.path.join(CFG.WEBDRIVER_LOCATION, CFG.WEBDRIVER_NAME))
    driver.get(url_to_click)
    time.sleep(wait_time)
    scroll_pause_time = pause_time
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page

        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height * i) > scroll_height:
            break

    urls = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for parent in soup.find_all("h3", class_="item-title"):
        a_tag = parent.find("a")
        base = url_to_click
        link = a_tag.attrs['href']
        url = urljoin(base, link)
        urls.append(url)

    driver.quit()
    return urls


def main():
    url_list = extract_urls(LibrarySearch.get_search_url("HUJI", "amos oz"), 5, 3)
    print(len(url_list))


if __name__ == "__main__":
    main()
