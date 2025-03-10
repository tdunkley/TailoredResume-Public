from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# ✅ Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# ✅ Import required modules
try:
    from modules.file_management.file_manager import ensure_directory_exists, extract_and_rename_csv, cleanup_downloads, move_file
    from modules.best_practices.file_management import enforce_naming_convention, validate_file, cleanup_temp_files
    from modules.utils.path_manager import PATHS
    print("✅ Successfully imported file management modules.")
except ImportError as e:
    print(f"❌ Error importing file management modules: {e}")
    sys.exit(1)

# ✅ Define Paths
DOWNLOAD_DIR = PATHS.get("huntr_downloads")
EXTRACT_DIR = PATHS.get("huntr_extracted")
FINAL_CSV_NAME = "huntr_export.csv"
EXPECTED_PREFIX = "USER_FULL_DATA_DOWNLOAD"

# ✅ Ensure paths are absolute
DOWNLOAD_DIR = str(os.path.abspath(DOWNLOAD_DIR))
EXTRACT_DIR = str(os.path.abspath(EXTRACT_DIR))

# ✅ Ensure directories exist
ensure_directory_exists(DOWNLOAD_DIR)
ensure_directory_exists(EXTRACT_DIR)

# ✅ Initialize WebDriver
options = FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", DOWNLOAD_DIR)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)
driver = webdriver.Firefox(options=options)
driver.maximize_window()

try:
    driver.get("https://huntr.co/track/boards")
    time.sleep(3)
    
    if "login" in driver.current_url:
        driver.get("https://huntr.co/login")
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_field.send_keys("tdunkley@gmail.com")
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_field.send_keys("el34!Q6M$g6gs0BA")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log In')]")))
        login_button.click()
        WebDriverWait(driver, 15).until(lambda d: "track/boards" in d.current_url)

    driver.get("https://huntr.co/settings")
    time.sleep(5)
    
    download_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Download my data')]")))
    existing_files = set(os.listdir(DOWNLOAD_DIR))
    download_button.click()
    
    WebDriverWait(driver, 120).until_not(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Processing your export')]")))
    
    max_wait_time = 180
    start_time = time.time()
    downloaded_zip = None

    while time.time() - start_time < max_wait_time:
        new_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(EXPECTED_PREFIX) and f.endswith(".zip")]
        if new_files:
            downloaded_zip = os.path.join(DOWNLOAD_DIR, new_files[0])
            break
        time.sleep(5)

    if not downloaded_zip:
        raise TimeoutException("⏳ Download file not found after waiting period!")

    # ✅ Check if the file already exists and handle accordingly
    if os.path.exists(downloaded_zip):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        renamed_zip = f"{downloaded_zip}_{timestamp}.zip"
        os.rename(downloaded_zip, renamed_zip)
        downloaded_zip = renamed_zip
        print(f"⚠️ File already existed. Renamed to: {renamed_zip}")

    extracted_csv = extract_and_rename_csv(downloaded_zip, extract_to=EXTRACT_DIR, renamed_file=FINAL_CSV_NAME)
    extracted_csv = enforce_naming_convention(extracted_csv)
    
    if not validate_file(extracted_csv):
        raise FileNotFoundError("❌ Validated file not found.")

    cleanup_temp_files()
    cleanup_downloads(DOWNLOAD_DIR, keep_recent=3)

    # ✅ Ensure all downloads are completed before closing the browser
    while any(f.endswith(".part") for f in os.listdir(DOWNLOAD_DIR)):
        print("⏳ Waiting for downloads to complete...")
        time.sleep(5)
    print("✅ All downloads completed. Proceeding to close browser.")

except (NoSuchElementException, TimeoutException, FileNotFoundError) as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()