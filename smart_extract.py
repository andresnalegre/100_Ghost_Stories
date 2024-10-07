import logging
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

# Logger setup to track script progress and errors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def download_image(url, save_path):
    """
    Downloads an image from a given URL and saves it to the specified path.
    """
    try:
        logging.info(f"Downloading image from: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        logging.info(f"Image saved successfully: {save_path}")
    except Exception as e:
        logging.error(f"Error downloading image from {url}. Error details: {e}")

def get_carousel_images(driver):
    """
    Extracts image URLs from a carousel on the current page.
    """
    try:
        logging.info("Looking for all relevant images in the manga carousel.")
        driver.execute_script("document.querySelectorAll('#carousel .carousel-item img').forEach(img => img.src = img.dataset.src);")
        time.sleep(3)

        carousel_images = driver.find_elements(By.CSS_SELECTOR, "#carousel .carousel-item img")
        image_urls = [img.get_attribute('src') for img in carousel_images if img.get_attribute('src')]

        logging.info(f"Found {len(image_urls)} images in the carousel.")
        return image_urls
    
    except Exception as e:
        logging.error("Couldn't find images in the carousel.")
        logging.error(f"Error details: {e}")
        return []

def get_chapter_links(driver):
    """
    Retrieves all chapter links from the manga's main page.
    """
    try:
        logging.info("Fetching all chapter links from main page.")
        chapter_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'list-chapter')]")
        chapter_links = [chapter.get_attribute('href') for chapter in chapter_elements if chapter.get_attribute('href')]

        # Reverses to start from the last chapter
        chapter_links.reverse()

        logging.info(f"Total chapters found: {len(chapter_links)}")
        return chapter_links
    
    except Exception as e:
        logging.error("Couldn't fetch chapters.")
        logging.error(f"Error details: {e}")
        return []

def download_chapter_images(driver, chapter_url, chapter_dir):
    """
    Downloads all images from a given manga chapter.
    """
    try:
        driver.get(chapter_url)

        max_wait_time = 15
        elapsed_time = 0
        loaded = False

        # Waits for the chapter page to fully load
        while not loaded and elapsed_time < max_wait_time:
            try:
                driver.find_element(By.ID, "carousel")
                loaded = True
            except NoSuchElementException:
                logging.warning(f"Waiting for page to load... {elapsed_time}/{max_wait_time} seconds.")
                time.sleep(1)
                elapsed_time += 1
        
        if not loaded:
            logging.error(f"Failed to load chapter after {max_wait_time} seconds: {chapter_url}")
            return

        current_url = driver.current_url
        logging.info(f"Current chapter URL: {current_url}")

        # Fetch all images from the chapter's carousel
        image_urls = get_carousel_images(driver)

        # Create a directory for the chapter's images and download them
        os.makedirs(chapter_dir, exist_ok=True)
        for index, image_url in enumerate(image_urls, start=1):
            image_filename = f"img_{index:02d}.jpg"
            image_save_path = os.path.join(chapter_dir, image_filename)
            download_image(image_url, image_save_path)

        logging.info(f"Downloaded {len(image_urls)} images for this chapter.")

    except TimeoutException as e:
        logging.error(f"Timeout loading chapter: {chapter_url}")
        logging.error(f"Error details: {e}")

    except Exception as e:
        logging.error(f"Error processing chapter. Details: {e}")

def main(base_dir):
    """
    Sets up the web driver and controls the flow of downloading chapters from the manga site.
    """
    try:
        logging.info("Setting up ChromeDriver.")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service("/opt/homebrew/bin/chromedriver")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("ChromeDriver started successfully.")

        base_url = 'https://vyvymanga.net/manga/hundred-ghost-stories-of-my-own-death'
        logging.info(f"Accessing URL: {base_url}")
        driver.get(base_url)

        driver.implicitly_wait(10)

        # Get all chapter links from the main page
        chapter_links = get_chapter_links(driver)

        # Download each chapter individually
        for chapter_index, chapter_url in enumerate(chapter_links, start=1):
            logging.info(f"Processing chapter {chapter_index}")
            chapter_dir = os.path.join(base_dir, f"chapter_{chapter_index}")
            download_chapter_images(driver, chapter_url, chapter_dir)

    except Exception as e:
        logging.error("Error during main execution.")
        logging.error(f"Details: {e}")

    finally:
        try:
            driver.quit()
            logging.info("ChromeDriver closed successfully.")
        except Exception as e:
            logging.error("Error closing ChromeDriver.")
            logging.error(f"Details: {e}")

if __name__ == "__main__":
    base_dir = os.path.expanduser("~/Desktop/100_Ghost_Stories")
    main(base_dir)
