import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from loguru import logger as logging


async def async_screenshot(wallet):
    chromedriver_path = '/usr/local/bin/chromedriver'
    service = Service(chromedriver_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    service = Service(chromedriver_path, log_path='chromedriver.log')

    driver = webdriver.Chrome(service=service, options=options)

    print("screen")
    url = f'https://debank.com/profile/{wallet}'
    css_selector_for_click = "#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9 > div.AssetsOnChain_totalChain__2zo3y > div.AssetsOnChain_item__qONfR.flex_flexRow__2Uu_s.AssetsOnChain_unfoldBtn__PWA-9"
    css_selector_for_screen = '#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9'
    css_selector_for_sum = "#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9 > div.Portfolio_projectGrid__ZYks1 > div:nth-child(1) > div > div.ProjectCell_assetsItemName__dqjfm > div.ProjectCell_assetsItemWorth__o2_hJ"
    
    try:
        driver.get(url)
    
    # Создаем объект WebDriverWait с ожиданием до 10 секунд
        wait = WebDriverWait(driver, 10)
    
    # Ожидаем появления элемента для клика
        element_to_click = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_for_click)))
        element_to_click.click()
    
    # Ожидаем появления элемента для скриншота
        element_for_screen = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_for_screen)))
        path_for_save = "app/wallets/" + wallet + ".png"
    # Можно использовать asyncio.to_thread если считаете это необходимым, но обычно это не требуется для снятия скриншота
        element_for_screen.screenshot(path_for_save)
    
    # Ожидаем появления элемента для извлечения суммы
        element_for_sum = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_for_sum)))
        sum = element_for_sum.text[1:]

        return 1, sum

    except Exception as err_:
        logging.error(f"Something went wrong: {err_}")
        return -1, 0

# async def wallet_balance(wallet):
#     driver = webdriver.Chrome()
#
#     url = f'https://debank.com/profile/{wallet}'
#     css_selector_for_sum = "#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9 > div.Portfolio_projectGrid__ZYks1 > div:nth-child(1) > div > div.ProjectCell_assetsItemName__dqjfm > div.ProjectCell_assetsItemWorth__o2_hJ"
#
#     try:
#         driver.get(url)
#         await asyncio.sleep(4)  # Simulating async wait
#         element_for_sum = await asyncio.to_thread(driver.find_element, By.CSS_SELECTOR, css_selector_for_sum)
#         sum = element_for_sum.text[1:]
#         return sum
#     except Exception as err_:
#         logging.error(f"Something went wrong: {err_}")
#         return 0
#     finally:
#         await asyncio.to_thread(driver.quit)
