from playwright.sync_api import sync_playwright
from playwright.sync_api import ElementHandle
import time
import pandas as pd

# url_ = "https://poshmark.com/closet/smexyfun"
url_ = input("Please Enter the url: ")

while True:
    items_num = int(input("Please Enter the number of items for extraction: "))
    if items_num < 48:
        print("Please enter minimum item number 48 and more")
        continue
    else:
        break

items_num = int(items_num / 48)


def start_items(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(
        headless=False,
        slow_mo=50,
    )
    page = browser.new_page()
    page.goto(url_, timeout=60000)

    category_list = ["Men", "Women", "Kids"]
    data = []

    count = 0
    count_f = 48

    for i in range(items_num):
        if i != 0:
            count = count + 48
            count_f = count_f + 48

        items = page.locator("xpath=//div[@class='card card--small']").all()

        for j in range(count, count_f):
            description = (
                items[j]
                .locator("xpath=//div[@class='item__details']/div/a")
                .text_content()
                .strip()
            )
            # if description not in data:
            sold_price = (
                items[j]
                .locator(
                    "xpath=//div[@class='item__details']//div[2]//span[contains(@class,'bold')]"
                )
                .text_content()
                .strip()
            )

            old_price_element = items[j].locator(
                "xpath=//div[@class='item__details']//div[2]//span[contains(@class,'lt')]"
            )
            old_price_elements = old_price_element.all()
            if len(old_price_elements) > 0:
                old_price = old_price_elements[0].text_content().strip()
            else:
                old_price = "N/A"

            category_element = items[j].locator(
                "xpath=//div[@class='item__details']//div[2]/div[2]//a[contains(@class,'pipe__size')]"
            )
            category_elements = category_element.all()
            if len(category_elements) > 0:
                category = (
                    category_elements[0]
                    .get_attribute("href")
                    .split("/")[2]
                    .split("-")[0]
                )
                if category in category_list:
                    category = category
                else:
                    category = ""
            else:
                category = ""

            brand_element = items[j].locator(
                "xpath=//div[@class='item__details']//div[2]/div[2]//a[contains(@class,'pipe__brand')]"
            )
            brand_elements = brand_element.all()
            if len(brand_elements) > 0:
                brand = brand_elements[0].text_content().strip()
            else:
                brand = ""

            status_element = items[j].locator(
                "xpath=//i[contains(@class,'sold-tag')]/span"
            )
            status_elements = status_element.all()
            if len(status_elements) > 0:
                Status = status_elements[0].text_content().strip()
            else:
                Status = "Not Sold"

            sold_platform = "Poshmark"

            # j +=1
            print(
                j + 1,
                brand,
                description,
                category,
                Status,
                sold_price,
                old_price,
                sold_platform,
            )
            data.append(
                [
                    j + 1,
                    brand,
                    description,
                    category,
                    Status,
                    sold_price,
                    old_price,
                    sold_platform,
                ]
            )

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(20)

    df = pd.DataFrame(
        data,
        columns=[
            "Item No",
            "Brand Name",
            "Description",
            "Category",
            "Status",
            "Sold Price",
            "Old Price",
            "Sold Platform",
        ],
    )
    df.to_excel("output.xlsx", index=False)


with sync_playwright() as playwright:
    start_items(playwright)
