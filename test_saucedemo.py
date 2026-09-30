#Imports

from playwright.sync_api import sync_playwright, expect
import pytest

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

def test_successful_login(page):
    page.goto(URL)
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

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