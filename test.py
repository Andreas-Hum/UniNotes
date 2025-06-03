import pandas as pd
import re
import time
import urllib.parse
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIG
INPUT_XLSX = (
    "C:\\Users\Andreas Hummelmose\\OneDrive\\Skrivebord\\Git\\UniNotes\\priser.xlsx"
)
OUTPUT_XLSX = "tcgplayer_prices_with_totals.csv"
SCREENSHOT_DIR = "screenshots"
HEADLESS = False

# Setup headless Chrome
options = Options()
if HEADLESS:
    options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)


# Normalize common set name errors
def normalize_set_names(card_name):
    replacements = {"Fire Red & Leaf Green": "FireRed & LeafGreen"}
    for old, new in replacements.items():
        card_name = card_name.replace(old, new)
    return card_name


# Strip [Reverse Holo] and track printing
def clean_card_name(name):
    printing = "Reverse Holo" if "[Reverse Holo]" in name else "Normal"
    cleaned = re.sub(r"\[Reverse Holo\]", "", name).strip()
    return cleaned, printing


# Create TCGPlayer search URL
def to_search_url(card_name):
    encoded = urllib.parse.quote_plus(card_name)
    encoded = encoded.replace("%7C", "|")  # TCGPlayer uses '+' for spaces
    return f"https://www.tcgplayer.com/search/all/product??productLineName=pokemon&q={encoded}&view=grid"


# Add LP filters
def build_lp_url(product_url, printing):
    print_type = "Reverse+Holofoil" if "reverse" in printing.lower() else "Normal"
    return f"{product_url}?page=1&Language=English&Condition=Lightly+Played&Printing={print_type}"


# Scrape LP price (and screenshot)
def get_lp_price(original_card_name, printing, screenshot_name):
    normalized_name = normalize_set_names(original_card_name)
    search_url = to_search_url(normalized_name)
    driver.get(search_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[data-testid^='product-card__image']")
            )
        )
        anchor = driver.find_element(
            By.CSS_SELECTOR, "a[data-testid^='product-card__image']"
        )
        href = anchor.get_attribute("href")
        product_url = (
            "https://www.tcgplayer.com" + href if href.startswith("/") else href
        )
    except:
        return None

    # Go to LP listing
    lp_url = build_lp_url(product_url, printing)
    driver.get(lp_url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.price-points__upper__price")
            )
        )
        time.sleep(2)  # Let everything load

        page_source = driver.page_source
        if "Condition: Lightly Played" not in page_source:
            print("⚠️ LP condition not confirmed.")

        # Screenshot the page for record
        driver.save_screenshot(f"{SCREENSHOT_DIR}/{screenshot_name}.png")

        # Try both price elements
        price_elements = driver.find_elements(
            By.CSS_SELECTOR, "span.price-points__upper__price"
        )
        price_value = None

        if len(price_elements) > 0:
            try:
                price_value = float(price_elements[0].text.strip().replace("$", ""))
            except ValueError:
                pass

        if price_value is None and len(price_elements) > 1:
            try:
                price_value = float(price_elements[1].text.strip().replace("$", ""))
                print("ℹ️ Using fallback price (recent sale)")
            except ValueError:
                pass

        return price_value

    except:
        driver.save_screenshot(f"{SCREENSHOT_DIR}/{screenshot_name}_ERROR.png")
        return None


# Load from XLSX (Danish headers)
df = pd.read_excel(INPUT_XLSX, engine="openpyxl")
results = []

# Scrape each card
for idx, row in df.iterrows():
    original_name = str(row["Card Name"])
    quantity = int(row["Quantity"])
    cleaned_name, printing = clean_card_name(original_name)

    print(f"\n🔍 {cleaned_name} ({printing}) x{quantity}")
    screenshot_id = f"{idx}_{cleaned_name.replace(' ', '_')[:50]}"
    price = get_lp_price(cleaned_name, printing, screenshot_id)

    if price is not None:
        total = round(price * quantity, 2)
        print(f"✅ Price: ${price} → Total: ${total}")
    else:
        price = float("nan")
        total = float("nan")
        print("❌ Price not found.")

    results.append([original_name, quantity, price, total])

# Save results to Excel
results_df = pd.DataFrame(
    results, columns=["Card Name", "Quantity", "LP Price", "Total Price"]
)
results_df.to_excel(OUTPUT_XLSX, index=False)
print(f"\n✅ DONE. Results saved to: {OUTPUT_XLSX}")

# Cleanup
driver.quit()
