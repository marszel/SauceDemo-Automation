#Imports

from playwright.sync_api import sync_playwright, expect
import pytest
import re

#Test Data

URL = "https://www.saucedemo.com"

#Functions

def login(page, username, password):
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()

def add_product_to_cart(page, product_id_name):
    page.locator(f"[data-test='add-to-cart-{product_id_name}']").click()

def remove_product_from_cart(page, product_id_name):
    page.locator(f"[data-test='remove-{product_id_name}']").click()

def open_cart(page):
    page.locator("a.shopping_cart_link").click()

def verify_product_in_cart(page, expected_product_name):
    product_locator = page.locator("div.inventory_item_name", has_text=expected_product_name)
    expect(product_locator).to_be_visible()

def verify_empty_cart(page):
    expect(page.locator(".shopping_cart_badge")).to_be_hidden()

def verify_product_count(page, expected_count):
    expect(page.locator(".inventory_item_name")).to_have_count(expected_count)

def verify_product_visible(page, product_name):
    product_locator = page.locator(".inventory_item_name", has_text=product_name)
    expect(product_locator).to_be_visible()

def logout(page):
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()

#Tests

#TC_001
def test_successful_login(page):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

#TC_002, TC_003
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("invalid_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service")
    ]
)
def test_negative_logins(page, username, password, expected_error):
    page.goto(URL)
    login(page, username, password)
    expect(page.locator("[data-test='error']")).to_have_text(expected_error)

#TC_004
@pytest.mark.parametrize(
    "username, password",
    [
        ("standard_user", "secret_sauce"),
    ]
)
def test_successful_logout(page, username, password):
    page.goto(URL)
    login(page, username, password)
    logout(page)
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("#user-name")).to_be_visible()

#TC_005 to TC_010
@pytest.mark.parametrize(
    "name_from_list, id_from_list",
    [
        ("Sauce Labs Backpack", "sauce-labs-backpack"),
        ("Sauce Labs Bolt T-Shirt", "sauce-labs-bolt-t-shirt"),
        ("Sauce Labs Bike Light", "sauce-labs-bike-light"),
        ("Sauce Labs Fleece Jacket", "sauce-labs-fleece-jacket"),
        ("Sauce Labs Onesie", "sauce-labs-onesie"),
        ("Test.allTheThings() T-Shirt (Red)", "test.allthethings()-t-shirt-(red)")
    ]
)
def test_add_and_remove_product_from_cart(page, name_from_list, id_from_list):
    product_name = name_from_list
    product_id = id_from_list
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    verify_product_count(page, 6)
    verify_product_visible(page, product_name)
    add_product_to_cart(page, product_id)
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    open_cart(page)
    verify_product_in_cart(page, product_name)
    remove_product_from_cart(page, product_id)
    verify_empty_cart(page)

#TC_011 to TC_014
@pytest.mark.parametrize(
    "sort_option, sort_type",
    [
        ("az", "text_asc"),
        ("za", "text_desc"),
        ("lohi", "price_asc"),
        ("hilo", "price_desc")
    ]
)
def test_dynamic_product_sorting(page, sort_option, sort_type):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    expect(page.locator(".inventory_item_name").first).to_be_visible()
    product_locator = page.locator(".inventory_item_name")
    initial_count = product_locator.count()
    page.locator(".product_sort_container").select_option(sort_option)
    expect(product_locator).to_have_count(initial_count)
    if "text" in sort_type:
        displayed_titles = product_locator.all_text_contents()
        if sort_type == "text_asc":
            assert displayed_titles == sorted(displayed_titles)
        else:
            assert displayed_titles == sorted(displayed_titles, reverse=True)
    elif "price" in sort_type:
        price_locator = page.locator(".inventory_item_price")
        raw_prices = price_locator.all_text_contents()
        displayed_prices = [float(price.replace("$", "")) for price in raw_prices]
        if sort_type == "price_asc":
            assert displayed_prices == sorted( displayed_prices)
        else:
            assert displayed_prices == sorted(displayed_prices, reverse=True)

#TC_015
def test_verify_product_details_page_content_and_navigation(page):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    expect(page.locator(".inventory_item_name").first).to_be_visible()
    first_product_locator = page.locator(".inventory_item_name").first
    target_product_name = first_product_locator.text_content()
    first_product_locator.click()
    expect(page).to_have_url(re.compile(r"https://www\.saucedemo\.com/inventory-item\.html"))
    expect(page.locator(".inventory_details_name")).to_have_text(target_product_name)
    expect(page.locator(".inventory_details_img")).to_be_visible()
    expect(page.locator(".inventory_details_price")).to_be_visible()
    page.locator("[data-test='back-to-products']").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

#TC_016
def test_verify_complete_purchase_flow_for_multiple_items(page):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    add_product_to_cart(page, "sauce-labs-backpack")
    add_product_to_cart(page, "sauce-labs-bike-light")
    open_cart(page)
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")
    page.locator("[data-test='checkout']").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
    page.locator("[data-test='firstName']").fill("Katarzyna")
    page.locator("[data-test='lastName']").fill("Kowalska")
    page.locator("[data-test='postalCode']").fill("12-345")
    page.locator("[data-test='continue']").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    expect(page.locator(".inventory_item_name").first).to_have_text("Sauce Labs Backpack")
    expect(page.locator(".inventory_item_name").nth(1)).to_have_text("Sauce Labs Bike Light")
    expect(page.locator(".summary_subtotal_label")).to_have_text("Item total: $39.98")
    page.locator("[data-test='finish']").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
    expect(page.locator(".shopping_cart_badge")).to_be_hidden()

#TC_017
def test_verify_application_state_reset_via_sidebar_panel(page):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    expect(page.locator(".inventory_item_name").first).to_be_visible()
    first_product_id = "sauce-labs-backpack"
    add_product_to_cart(page, first_product_id)
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    page.locator("#react-burger-menu-btn").click()
    page.locator("#reset_sidebar_link").click()
    expect(page.locator(".shopping_cart_badge")).to_be_hidden()
    page.reload()
    expect(page.locator(f"[data-test='add-to-cart-{first_product_id}']")).to_be_visible()
