# python scraper.py --manufacturer "Mazda" --model "CX-5"

import argparse
import json
import time
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger
from playwright.sync_api import Page, sync_playwright

HEADLESS_MODE = False
HOME_LINK = "https://autodiler.me"

CUR_DIR = Path(__file__).parent
OUTPUT_DIR = CUR_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULT_FILENAME = OUTPUT_DIR / "result.jsonl"

USER_DATA_DIR = CUR_DIR / "user_data_dir"
EXT_DIR = CUR_DIR / "uBlock0.chromium"


def input_filter(
    page: Page,
    manufacturer: str = "",
    model: str = "",
    body: str = "",
    fuel: str = "",
    mileage_min: str = "",
    mileage_max: str = "",
    engine_displ_min: str = "",
    engine_displ_max: str = "",
    year_min: str = "",
    year_max: str = "",
    price_min: str = "",
    price_max: str = "",
    transmission: str = "",
    city: str = "",
):
    # manufacturer
    if manufacturer != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[0]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        page.keyboard.type(manufacturer, delay=75)
        time.sleep(2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == manufacturer:
                item.click()
                break

    # model
    if model != "":
        time.sleep(1)
        filter_field = page.query_selector_all("div.polja-pretrage-item")[1]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        page.keyboard.type(model, delay=75)
        time.sleep(2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == model:
                item.click()
                break

    # body
    if body != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[2]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        page.keyboard.type(body, delay=75)
        time.sleep(2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == body:
                item.click()
                break

    # fuel
    if fuel != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[3]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == fuel:
                item.click()
                break

    # mileage
    if mileage_min != "" and mileage_max != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[4]
        inputs = filter_field.query_selector_all("input")
        inputs[0].click(delay=100, click_count=2)
        inputs[0].type(mileage_min, delay=100)
        inputs[1].click(delay=100, click_count=2)
        inputs[1].type(mileage_max, delay=100)

    # engine displacement
    if engine_displ_min != "" and engine_displ_max != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[5]
        inputs = filter_field.query_selector_all("input")
        inputs[0].click(delay=100, click_count=2)
        inputs[0].type(engine_displ_min, delay=100)
        inputs[1].click(delay=100, click_count=2)
        inputs[1].type(engine_displ_max, delay=100)

    # year
    if year_min != "" and year_max != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[6]
        range_items = filter_field.query_selector_all("div.select-range-item")
        range_items[0].click(delay=100, click_count=2)
        page.keyboard.type(year_min, delay=100)
        time.sleep(2)
        items = range_items[0].query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == year_min:
                item.click()
                break

        range_items[1].click(delay=100, click_count=2)
        page.keyboard.type(year_max, delay=100)
        time.sleep(2)
        items = range_items[1].query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == year_max:
                item.click()
                break

    # price
    if price_min != "" and price_max != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[7]
        inputs = filter_field.query_selector_all("input")
        inputs[0].click(delay=100, click_count=2)
        inputs[0].type(price_min, delay=100)
        inputs[1].click(delay=100, click_count=2)
        inputs[1].type(price_max, delay=100)

    # transmission
    if transmission != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[8]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == transmission:
                item.click()
                break

    # city
    if city != "":
        filter_field = page.query_selector_all("div.polja-pretrage-item")[9]
        filter_field.query_selector("div>label").click(delay=100, click_count=2)
        page.keyboard.type(city, delay=75)
        time.sleep(2)
        items = filter_field.query_selector_all("li.select-dropdown-item")
        for item in items:
            if item.inner_text().strip() == city:
                item.click()
                break


def get_filters_from_args():
    parser = argparse.ArgumentParser(description="Filter car data based on parameters.")
    parser.add_argument(
        "--manufacturer",
        type=str,
        default="",
        help="Manufacturer of the car",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="",
        help="Model of the car",
    )
    parser.add_argument(
        "--body",
        type=str,
        default="",
        help="Body type of the car",
    )
    parser.add_argument(
        "--fuel",
        type=str,
        default="",
        help="Fuel type of the car",
    )
    parser.add_argument(
        "--mileage_min",
        type=str,
        default="",
        help="Minimum mileage",
    )
    parser.add_argument(
        "--mileage_max",
        type=str,
        default="",
        help="Maximum mileage",
    )
    parser.add_argument(
        "--engine_displ_min",
        type=str,
        default="",
        help="Minimum engine displacement",
    )
    parser.add_argument(
        "--engine_displ_max",
        type=str,
        default="",
        help="Maximum engine displacement",
    )
    parser.add_argument(
        "--year_min",
        type=str,
        default="",
        help="Minimum year of manufacture",
    )
    parser.add_argument(
        "--year_max",
        type=str,
        default="",
        help="Maximum year of manufacture",
    )
    parser.add_argument(
        "--price_min",
        type=str,
        default="",
        help="Minimum price",
    )
    parser.add_argument(
        "--price_max",
        type=str,
        default="",
        help="Maximum price",
    )
    parser.add_argument(
        "--transmission",
        type=str,
        default="",
        help="Transmission type",
    )
    parser.add_argument(
        "--city",
        type=str,
        default="",
        help="City where the car is located",
    )
    args = parser.parse_args()

    # Use the arguments
    print("Manufacturer:", args.manufacturer)
    print("Model:", args.model)
    print("Body:", args.body)
    print("Fuel:", args.fuel)
    print("Mileage Min:", args.mileage_min)
    print("Mileage Max:", args.mileage_max)
    print("Engine Displacement Min:", args.engine_displ_min)
    print("Engine Displacement Max:", args.engine_displ_max)
    print("Year Min:", args.year_min)
    print("Year Max:", args.year_max)
    print("Price Min:", args.price_min)
    print("Price Max:", args.price_max)
    print("Transmission:", args.transmission)
    print("City:", args.city)

    return (
        args.manufacturer,
        args.model,
        args.body,
        args.fuel,
        args.mileage_min,
        args.mileage_max,
        args.engine_displ_min,
        args.engine_displ_max,
        args.year_min,
        args.year_max,
        args.price_min,
        args.price_max,
        args.transmission,
        args.city,
    )


def main():
    filters = get_filters_from_args()

    with sync_playwright() as playwright, playwright.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        headless=HEADLESS_MODE,
        args=[
            f"--disable-extensions-except={EXT_DIR}",
            f"--load-extension={EXT_DIR}",
        ],
    ) as browser:
        browser.set_default_timeout(120000)
        page: Page = browser.new_page()

        logger.info("navigate to home link")
        page.goto(HOME_LINK)

        logger.info("fill filters")
        input_filter(page, *filters)

        logger.info("click search button")
        page.query_selector("button.filter-buttons-search").click()
        time.sleep(10)

        product_list = []

        while True:
            logger.info("fetch product details")
            soup = BeautifulSoup(page.content(), "html.parser")
            product_divs = soup.select("div.oglasi-item-tekst")
            for product_div in product_divs:
                title = product_div.select_one("h3").text.strip()
                spec_value_elems = product_div.select(
                    "span.oglasi-item-description_spec-value"
                )
                mileage = spec_value_elems[0].text.strip()
                year = spec_value_elems[1].text.strip()
                fuel = spec_value_elems[2].text.strip()
                price = product_div.select_one("div.cena").text.strip()
                link = product_div.select_one("a.oglasi-item-heading").attrs["href"]

                product_list.append(
                    {
                        "title": title,
                        "mileage": mileage,
                        "year": year,
                        "fuel": fuel,
                        "price": price,
                        "link": HOME_LINK + link,
                    }
                )

            logger.info("find next page button")
            pagination_items = page.query_selector_all("li.ads-pagination__item")
            if len(pagination_items) > 0:
                last_btn = pagination_items[-1]
                if last_btn.inner_text().strip() == "sledeća":
                    logger.info("next page button found")
                    logger.info("click next page button")
                    page_link = last_btn.query_selector("a").get_attribute("href")
                    page_link = HOME_LINK + page_link
                    page.goto(page_link)
                    time.sleep(3)
                    continue

            logger.info("no more pages")
            break

        with RESULT_FILENAME.open("w", encoding="utf-8") as file:
            for product in product_list:
                file.write(json.dumps(product, ensure_ascii=False) + "\n")

        logger.info(f"result saved to {RESULT_FILENAME}")


if __name__ == "__main__":
    main()
