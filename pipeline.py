from database import save_product
from scraper import get_scraped_products


def run_pipeline():
    products = get_scraped_products()

    if products is None or products.empty:
        print("No products found.")
        return

    for _, product in products.iterrows():
        save_product(
            product["external_id"],
            product["name"],
            product["price"],
        )

    print(f"Saved {len(products)} product observations.")


if __name__ == "__main__":
    run_pipeline()
