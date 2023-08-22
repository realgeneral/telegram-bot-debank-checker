import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from loguru import logger as logging


async def async_screenshot(wallet):
    driver = webdriver.Chrome()
    print("screen")
    url = f'https://debank.com/profile/{wallet}'
    css_selector_for_click = "#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9 > div.AssetsOnChain_totalChain__2zo3y > div.AssetsOnChain_item__qONfR.flex_flexRow__2Uu_s.AssetsOnChain_unfoldBtn__PWA-9"
    css_selector_for_screen = '#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9'
    css_selector_for_sum = "#root > div > div.DesktopFrame_mainContainer__2V8Re > div.container_mainSubContainer__39U6P > div.DesktopContainer_main__MG15v.container_pageCenterSubContainer__3encx > div > div.Portfolio_collect__j-mVa.card_suspend__2DfyT.card_card__i5VM9 > div.Portfolio_projectGrid__ZYks1 > div:nth-child(1) > div > div.ProjectCell_assetsItemName__dqjfm > div.ProjectCell_assetsItemWorth__o2_hJ"

    try:
        driver.get(url)
        await asyncio.sleep(4)  # Simulating async wait

        try:
            element_to_click = await asyncio.to_thread(driver.find_element, By.CSS_SELECTOR, css_selector_for_click)
            element_to_click.click()
        finally:
            await asyncio.sleep(2)
            element_for_screen = await asyncio.to_thread(driver.find_element, By.CSS_SELECTOR, css_selector_for_screen)
            path_for_save = "app/wallets/" + wallet + ".png"
            await asyncio.to_thread(element_for_screen.screenshot, path_for_save)

            element_for_sum = await asyncio.to_thread(driver.find_element, By.CSS_SELECTOR, css_selector_for_sum)
            sum = element_for_sum.text[1:]

            return 1, sum
    except Exception as err_:
        logging.error(f"Something went wrong: {err_}")
        return -1, 0
    finally:
        await asyncio.to_thread(driver.quit)


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