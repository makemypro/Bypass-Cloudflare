from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import random
from selenium.webdriver.common.by import By

# User agent for real time user
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
url='https://nowsecure.nl'


def start_browser(url,  user_agent):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=options)
    retries = 5
    try:
        driver.get(url)
        for attempt in range(retries):
            try:

                # Wait randomly until cloudflare pass
                wait_time = random.uniform(15, 30)
                print(f"Wait {wait_time}s until cloudflare pass")

                time.sleep(wait_time)
                iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
                driver.switch_to.frame(iframe)
                text = driver.find_element(By.XPATH, "//span[contains(text(), 'Success!')]").text
                if (text and text.lower() == "success!") or ("Success!" in driver.page_source):
                    print("Cloudflare passed!")
                    break

            except Exception as e:
                print("Did not find the elements")
                if attempt < retries:
                    time.sleep(wait_time)

    finally:
        driver.quit()

def start_thread(url, user_agent, max_worker=2):
    threads = []
    for _ in range(max_worker):
        thread = threading.Thread(target=start_browser, args=(url, user_agent))
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(1, 3))

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start_thread(url, user_agent)