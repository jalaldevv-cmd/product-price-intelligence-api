from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd

URL = "https://scrapifydatalabs.com/playground/js-rendered"


def scrape_products(page):
    products = []

    try:
        page.goto(URL, timeout=10000)
        page.wait_for_selector('#js-product-list[data-ready="true"]')
    except PlaywrightTimeoutError:
        print("Page took too long to load.")
        return []

    product_cards = page.locator(".product-card")

    for i in range(product_cards.count()):
        card = product_cards.nth(i)

        external_id = card.get_attribute("data-product-id")
        name = card.locator(".product-title").inner_text()
        price = card.locator(".product-price").inner_text()

        products.append(
            {
                "external_id": external_id,
                "name": name,
                "price": price,
            }
        )

    return products


def clean_products(products):
    if not products:
        print("No products to clean.")
        return

    data = pd.DataFrame(products)

    data["price"] = data["price"].str.replace("$", "", regex=False).astype(float)

    data = data.drop_duplicates()

    return data


def get_scraped_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        products = scrape_products(page)

        browser.close()

    return clean_products(products)
