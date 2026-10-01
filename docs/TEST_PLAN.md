# Master Test Plan - SauceDemo Automation Project

## 1. Test Plan Identifier
SD-PLAYWRIGHT-MTP-V1.0

## 2. Introduction & Purpose
This document describes the Test plan for SauceDemo automation project. The goal is to test all key functions of the shop using Python and Playwright.

## 3. Test Items
The test item is the SauceDemo web application, available at: https://www.saucedemo.com/

## 4. Scope of Testing
### 4.1 Features in Scope
* Log in and log out (successful and negative paths)
* Add and remove products to/from the cart
* Full checkout process (End-to-End)
* Sort products by name and price
* Verify product details page
* Reset application state via sidebar menu

### 4.2 Out of Scope
* Security Testing
* Performance Testing
* Mobile UI compatibility Testing
* Integration with external payment gateways

## 5. Environmental Needs
* Operating System: Linux, Ubuntu 26.04
* Testing Frameworks and Tools: Python 3, Playwright, Pytest
* Target Browser: Chromium

## 6. Entry & Exit Criteria
### 6.1 Entry Criteria
* Access to the Internet
* Stability and availability of the test environment (SauceDemo website)
* Proper local testing environment configuration (.venv)

### 6.2 Exit Criteria
* All planned test cases are executed and passed (100% Pass Rate)
* Code pushed to the GitHub repository