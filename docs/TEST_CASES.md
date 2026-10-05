# Test case Specification - SauceDemo Automation

## TC_001 to TC_003: Verify user authentication with various data.
* **Preconditions:**
1. The web service is running and available.
2. Login fields and the button are visible.
* **Steps:**
1. Open the login page ("https://saucedemo.com").
2. Enter the "Username" from the table.
3. Enter the "Password" from the table.
4. Click the "Login" button.

| Case ID | Username | Password | Expected Result / Error Message |
| :--- | :--- | :--- | :--- |
| TC_001 | `standard_user` | `secret_sauce` | Successful login. Redirect to the inventory catalog view. |
| TC_002 | `locked_out_user`| `secret_sauce` | Access denied. Error text displays: "Epic sadface: Sorry, this user has been locked out." |
| TC_003 | `invalid_user` | `wrong_password`| Access denied. Error text displays: "Epic sadface: Username and password do not match..." |
* **Expected Result:**
1. The application behavior matches the "Expected Result/Error Message".

## TC_004: Verify successful user logout
* **Preconditions:**
1. Successful login and active session on the inventory page.
* **Steps:**
1. Click the burger menu button to expand the navigation panel.
2. Click the "Logout" link.
* **Expected Result:**
1. The active session is destroyed. The application securely redirects back to the login page view.

## TC_005 to TC_010: Verify adding and removing a single product from cart.
* **Preconditions:**
1. Successful login and active session on the inventory page.
2. The shopping cart is empty (no badge visible).
* **Steps:**
1. Find the product using the "Product Name" from the table.
2. Click the "Add to cart" button inside that specific product container.
3. Check that the shopping cart badge changed to "1".
4. Click the shopping cart icon to open the cart page.
5. Verify that the product name in the cart matches the "Product Name" from the table.
6. Click the "Remove" button next to the product name.
7. Check the shopping cart badge state.

| Case ID | Product Name | Product ID (id_from_list) |
| :--- | :--- | :--- |
| TC_005 | Sauce Labs Backpack | sauce-labs-backpack |
| TC_006 | Sauce Labs Bolt T-Shirt | sauce-labs-bolt-t-shirt |
| TC_007 | Sauce Labs Bike Light | sauce-labs-bike-light |
| TC_008 | Sauce Labs Fleece Jacket | sauce-labs-fleece-jacket |
| TC_009 | Sauce Labs Onesie | sauce-labs-onesie |
| TC_010 | Test.allTheThings() T-Shirt (Red) | test.allthethings()-t-shirt-(red) |
* **Expected Results:**
1. After Step 2, the shopping cart badge text changes to "1".
2. After Step 4, the product is visible inside the cart list view with the correct name.
3. After Step 6, the product is removed from the cart page and the cart badge component becomes hidden.

## TC_011 to TC_014: Verify dynamic product catalog sorting.
* **Preconditions:**
1. Successful login and active session on the inventory page.
2. The sorting dropdown selector is fully visible and interactive.
* **Steps:**
1. Click the sorting dropdown.
2. Select the option using "Option Value" from the table.
3. Validate the full product grid order sequence.

| Case ID | Option Value | Selection Text Label | Expected Sorting Logic |
| :--- | :--- | :--- | :--- |
| TC_011 | `az` | "Name (A to Z)" | Alphabetical order sequence (A to Z) |
| TC_012 | `za` | "Name (Z to A)" | Alphabetical order sequence (Z to A) |
| TC_013 | `lohi` | "Price (low to high)"| Numerical monetary value sequence, ascending |
| TC_014 | `hilo` | "Price (high to low)"| Numerical monetary value sequence, descending |
* **Expected Result:**
1. The select layout updates to the chosen sorting option.
2. The product list instantly rearranges dynamically. The dataset order strictly satisfies the "Expected Sorting Logic" without hardcoded item values.

## TC_015: Verify product details page content and navigation.
* **Preconditions:**
1. Successful login and active session on the inventory page.
* **Steps:**
1. Click on the name link "Sauce Labs Backpack".
2. Check the browser page URL.
3. Verify the visibility of the product image, name, description text, and price.
4. Click the "Back to products" button.
* **Expected Results:**
1. The application routes to the item view page layout.
2. All product information components are displayed correctly with no missing data.
3. The user successfully navigates back to the main inventory view.

## TC_016: Verify complete purchase flow for multiple items.
* **Preconditions:**
1. Successful login and active session.
2. Add multiple distinct products to the shopping cart.
3. Open the cart page view (cart badge tracking equals the added items count).
* **Steps:**
1. Click the "Checkout" button.
2. Populate the required input fields: First Name, Last Name, and Postal Code.
3. Click the "Continue" button.
4. Verify the transaction overview summary screen (product names, payment identifier, shipping method, and math calculation).
5. Click the "Finish" button.
6. Verify the confirmation header text on the final screen.
* **Expected Result:**
1. After Step 1, the browser redirects to the checkout information form.
2. After Step 3, the browser redirects to the overview page.
3. The item total price is calculated correctly.
4. After Step 5, the final success page displays the header: "Thank you for your order!". The shopping cart badge resets and disappears.

## TC_017: Verify application state reset via sidebar panel.
* **Preconditions:**
1. Successful login and active session on the inventory page.
2. Add products to the cart until the cart badge displays an active number.
* **Steps:**
1. Click the burger menu button to expand the navigation panel.
2. Click the "Reset App State" link.
3. Observe the shopping cart badge and the product action buttons.
* **Expected Result:**
1. The sidebar panel opens smoothly with all navigation links visible.
2. The internal application session state resets completely.
3. The shopping cart badge disappears instantly from the screen, and all active "Remove" buttons revert to "Add to cart".