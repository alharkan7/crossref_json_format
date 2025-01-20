"""
Crossref API JSON Format Scraper

This script scrapes the Crossref API documentation from their Swagger UI to create
a comprehensive JSON model of their API structure. It uses Selenium WebDriver to
interact with the dynamic content of the Swagger UI and extract all model definitions.

The script handles the expansion of nested model definitions and saves progress
to allow for resumption if the process is interrupted.

Requirements:
    - Chrome WebDriver
    - Selenium
    - Chrome browser

Usage:
    1. Update chrome_driver_path if necessary
    2. Run the script: python crossref_json_model.py
    3. The script will create:
       - crossref_models_expanded.json: Contains the full JSON model
       - expansion_progress.json: Tracks progress for resumption

Author: Your Name
License: MIT
"""

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import json
import time
import os

# Set up Chrome with WebDriver
# TODO: Use webdriver_manager instead of local ChromeDriver for better portability
chrome_driver_path = r"D:\Archives\Misc\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

def save_progress(progress_data):
    """
    Save the current progress of model box processing to a JSON file.
    
    Args:
        progress_data (dict): Dictionary containing processed model box information
    """
    with open('expansion_progress.json', 'w') as f:
        json.dump(progress_data, f)

def load_progress():
    """
    Load previously saved progress from JSON file.
    
    Returns:
        dict: Dictionary containing previously processed model box information
              or empty dict with initialized 'processed_model_boxes' list
    """
    if os.path.exists('expansion_progress.json'):
        with open('expansion_progress.json', 'r') as f:
            return json.load(f)
    return {'processed_model_boxes': []}

def expand_model_box(driver, model_box):
    """
    Completely expand a single model-box and all its nested elements.
    
    Args:
        driver (webdriver): Selenium WebDriver instance
        model_box (WebElement): The model box element to expand
        
    Returns:
        bool: True if expansion was successful, False otherwise
    
    Note:
        This function recursively expands all nested elements within the model box
        and includes retry logic for reliability.
    """
    try:
        # Get model name for logging
        model_name = model_box.find_element(By.CSS_SELECTOR, "span.model-title").text
        print(f"Expanding model box: {model_name}")

        # First, expand the main model box button if it's collapsed
        try:
            main_button = model_box.find_element(By.CSS_SELECTOR, "button.model-box-control[aria-expanded='false']")
            if main_button:
                driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", main_button)
                driver.execute_script("arguments[0].click();", main_button)
                # time.sleep(1)  # Wait for expansion
        except:
            print(f"Main button already expanded or not found for {model_name}")

        # Keep expanding until no more unexpanded elements
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            # Find all buttons that need expanding
            buttons = model_box.find_elements(By.CSS_SELECTOR, "button.model-box-control[aria-expanded='false']")
            if not buttons:
                break  # No more buttons to expand
                
            print(f"Found {len(buttons)} buttons to expand in {model_name}")
            expanded_count = 0
            
            for button in buttons:
                try:
                    # # Scroll button into view
                    # driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    # time.sleep(0.5)
                    
                    # Set aria-expanded to true and click
                    driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", button)
                    driver.execute_script("arguments[0].click();", button)
                    expanded_count += 1
                    # time.sleep(0.5)
                except Exception as e:
                    print(f"Failed to expand button in {model_name}: {e}")
            
            if expanded_count == 0:
                attempt += 1  # Only increment attempt if we couldn't expand any buttons
            
            # time.sleep(1)  # Wait for any new elements to load

        print(f"Finished expanding {model_name}")
        return True

    except Exception as e:
        print(f"Error expanding model box: {e}")
        return False

def extract_properties(model_box):
    """
    Extract properties from a model box, including nested objects.
    
    Args:
        model_box (WebElement): The model box element to extract properties from
        
    Returns:
        dict: Dictionary containing extracted properties
    """
    properties = {}
    rows = model_box.find_elements(By.CSS_SELECTOR, "tr.property-row")

    for row in rows:
        try:
            # Get the property name and check if it's required
            name_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)")
            prop_name = name_cell.text.split('*')[0].strip()  # Remove the * if present
            
            # Get the type cell which may contain nested objects
            type_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            
            # Check if this is a nested object by looking for a model-box-control button
            nested_button = type_cell.find_elements(By.CSS_SELECTOR, "button.model-box-control")
            
            if nested_button:
                # This is a nested object
                nested_props = extract_properties(type_cell)
                properties[prop_name] = nested_props
            else:
                # This is a simple property
                prop_type = type_cell.find_element(By.CSS_SELECTOR, "span.prop-type").text
                properties[prop_name] = prop_type

        except Exception as e:
            print(f"Error processing property row: {e}")
            continue

    return properties

def get_crossref_models():
    """
    Fetch Crossref API models from Swagger UI and save to JSON file.
    
    Returns:
        dict: Dictionary containing fetched models
    """
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    progress = load_progress()

    try:
        print("Navigating to Crossref API documentation...")
        url = "https://api.crossref.org/swagger-ui/index.html#/"
        driver.get(url)

        time.sleep(5)  # Give more time for initial page load

        print("Waiting for Models section to load...")
        wait = WebDriverWait(driver, 30)
        models_section = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#swagger-ui > section > div.swagger-ui > div:nth-child(2) > div:nth-child(4) > section"
        )))

        driver.execute_script("arguments[0].scrollIntoView(true);", models_section)
        # time.sleep(2)

        model_boxes = models_section.find_elements(By.CSS_SELECTOR, "span.model-box")
        print(f"Found {len(model_boxes)} model boxes to process")

        if os.path.exists('crossref_models_expanded.json'):
            with open('crossref_models_expanded.json', 'r', encoding='utf-8') as f:
                models_data = json.load(f)
        else:
            models_data = {}

        for i, model_box in enumerate(model_boxes, 1):
            try:
                model_name = model_box.find_element(By.CSS_SELECTOR, "span.model-title").text

                if model_name in progress['processed_model_boxes']:
                    print(f"Skipping already processed model: {model_name}")
                    continue

                print(f"Processing model {i}/{len(model_boxes)}: {model_name}")

                driver.execute_script("arguments[0].scrollIntoView(true);", model_box)
                # time.sleep(1)

                if expand_model_box(driver, model_box):
                    # time.sleep(1)  # Wait longer for expansion to complete
                    
                    # Extract properties including nested objects
                    properties = extract_properties(model_box)
                    models_data[model_name] = properties
                    progress['processed_model_boxes'].append(model_name)

                    save_progress(progress)
                    with open('crossref_models_expanded.json', 'w', encoding='utf-8') as f:
                        json.dump(models_data, f, ensure_ascii=False, indent=2)

                    print(f"Successfully processed {model_name}")
                    # time.sleep(1)

            except Exception as e:
                print(f"Error processing model box: {e}")
                continue

        print("Processing complete. Browser will remain open for 30 seconds for verification.")
        time.sleep(30)
        return models_data

    except TimeoutException:
        print("Timeout waiting for page to load")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

# Execute and save the results
print("Starting to fetch models...")
print("Note: Will resume from last saved progress if available")
models = get_crossref_models()

if models:
    print(f"Successfully processed {len(models)} models")
else:
    print("No models data was collected")