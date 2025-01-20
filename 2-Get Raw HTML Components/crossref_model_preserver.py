# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import os

# Set up Chrome with your local ChromeDriver
chrome_driver_path = r"D:\Archives\Misc\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

def save_progress(progress_data):
    with open('expansion_progress.txt', 'w') as f:
        f.write('\n'.join(progress_data['processed_model_boxes']))

def load_progress():
    if os.path.exists('expansion_progress.txt'):
        with open('expansion_progress.txt', 'r') as f:
            processed_models = f.read().splitlines()
            return {'processed_model_boxes': processed_models}
    return {'processed_model_boxes': []}

def expand_model_box(driver, model_box):
    """Completely expand a single model-box and all its nested elements"""
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
                    driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", button)
                    driver.execute_script("arguments[0].click();", button)
                    expanded_count += 1
                except Exception as e:
                    print(f"Failed to expand button in {model_name}: {e}")
            
            if expanded_count == 0:
                attempt += 1  # Only increment attempt if we couldn't expand any buttons

        print(f"Finished expanding {model_name}")
        return True

    except Exception as e:
        print(f"Error expanding model box: {e}")
        return False

def preserve_model_box(model_box):
    """Preserve the entire model box structure"""
    try:
        model_name = model_box.find_element(By.CSS_SELECTOR, "span.model-title").text
        html_content = model_box.get_attribute('outerHTML')
        
        # Save each model in its own HTML file
        filename = f"models/{model_name.replace(' ', '_')}.html"
        os.makedirs('models', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return filename
    except Exception as e:
        print(f"Error preserving model box: {e}")
        return None

def get_crossref_models():
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    progress = load_progress()
    preserved_models = []

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

        model_boxes = models_section.find_elements(By.CSS_SELECTOR, "span.model-box")
        print(f"Found {len(model_boxes)} model boxes to process")

        for i, model_box in enumerate(model_boxes, 1):
            try:
                model_name = model_box.find_element(By.CSS_SELECTOR, "span.model-title").text

                if model_name in progress['processed_model_boxes']:
                    print(f"Skipping already processed model: {model_name}")
                    continue

                print(f"Processing model {i}/{len(model_boxes)}: {model_name}")

                driver.execute_script("arguments[0].scrollIntoView(true);", model_box)

                if expand_model_box(driver, model_box):
                    # Preserve the entire model box structure
                    saved_file = preserve_model_box(model_box)
                    if saved_file:
                        preserved_models.append(saved_file)
                        progress['processed_model_boxes'].append(model_name)
                        save_progress(progress)
                        print(f"Successfully preserved {model_name} to {saved_file}")

            except Exception as e:
                print(f"Error processing model box: {e}")
                continue

        print("Processing complete. Browser will remain open for 30 seconds for verification.")
        time.sleep(30)
        return preserved_models

    except TimeoutException:
        print("Timeout waiting for page to load")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

# Execute and save the results
if __name__ == "__main__":
    print("Starting to fetch and preserve models...")
    print("Note: Will resume from last saved progress if available")
    models = get_crossref_models()

    if models:
        print(f"Successfully processed {len(models)} models")
    else:
        print("No models data was collected")
