import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

    
def main():
    # to run Chrome in headless mode
    options = Options()
    options.add_argument("--headless")

    # initialize a Chrome WerbDriver instance with the specified options
    driver = webdriver.Chrome(
        service=ChromeService(),
        options=options
    )
    
    # to avoid issues with responsive content
    driver.maximize_window()

    # get URL of target page
    url = input("Enter a valid URL: ")
    driver.get(url)

    # select the node images on the page
    image_html_nodes = driver.find_elements(
        By.cssSelector, "")
    urls = []  # list to store image URLs
    for image_html_node in image_html_nodes:
        try:
            # use the URL in the "src" as the default behavior
            image_url = image_html_node.get_attribute("src")

            # extract the URL of the largest image from "srcset",
            # if this attribute exists
            srcset =  image_html_node.get_attribute("srcset")
            if srcset is not None:
                # get the last element from the "srcset" value
                srcset_last_element = srcset.split(", ")[-1]
                # get the first element of the value,
                # which is the image URL
                image_url = srcset_last_element.split(" ")[0]

            # add the image URL to the list
            image_urls.append(image_url)
        except StaleElementReferenceException as e:
            continue

    for url in urls:
        print(url)

    # close the browser and free up its resources
    driver.quit()


if __name__ == "__main__":
    main()
