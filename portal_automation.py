from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

# COMPLIANCE DATE

def fill_compliance_date(driver, wait, date_str):
    field_id = "P2_COMP_DATE"
    cal_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"button[aria-controls='{field_id}_input']")
    ))
    cal_button.click()
    time.sleep(1)

    try:
        date_str = str(date_str).strip()
        if len(date_str.split("-")[2]) == 2:
            date_obj = datetime.strptime(date_str, "%d-%b-%y")
        else:
            date_obj = datetime.strptime(date_str, "%d-%b-%Y")
    except Exception as e:
        print(f"WARNING: Compliance Date parse error: {e}")
        return

    Select(wait.until(EC.presence_of_element_located(
        (By.ID, f"{field_id}_month")))).select_by_value(str(date_obj.month - 1))
    time.sleep(0.5)
    Select(driver.find_element(By.ID, f"{field_id}_year")
           ).select_by_visible_text(str(date_obj.year))
    time.sleep(0.5)

    day_cell = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"td[data-date='{date_obj.strftime('%Y-%m-%d')}'] span")
    ))
    day_cell.click()
    time.sleep(0.5)

    now = datetime.now()
    hour_12 = now.hour % 12 or 12
    ampm = "AM" if now.hour < 12 else "PM"
    minute = now.minute
    if minute < 8:      minute_val = 0
    elif minute < 23:   minute_val = 15
    elif minute < 38:   minute_val = 30
    elif minute < 53:   minute_val = 45
    else:               minute_val = 0

    try:
        Select(driver.find_element(By.ID, f"{field_id}_hours")).select_by_value(str(hour_12))
        time.sleep(0.3)
        Select(driver.find_element(By.ID, f"{field_id}_minutes")).select_by_value(str(minute_val))
        time.sleep(0.3)
        Select(driver.find_element(By.ID, f"{field_id}_ampm")).select_by_value(ampm)
        time.sleep(0.3)
    except Exception as e:
        print(f"WARNING: Time set error: {e}")

    done_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"button.a-DatePicker--close[aria-controls='{field_id}_input']")
    ))
    done_btn.click()
    time.sleep(1)
    print(f"Compliance Date = {date_str} + current time done")


# DIALOG DATE - Verification and Target

def fill_dialog_date(driver, wait, field_id, date_str):
    cal_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"button[aria-controls='{field_id}_input']")
    ))
    cal_button.click()
    time.sleep(1.5)

    try:
        date_str = str(date_str).strip()
        if len(date_str.split("-")[2]) == 2:
            date_obj = datetime.strptime(date_str, "%d-%b-%y")
        else:
            date_obj = datetime.strptime(date_str, "%d-%b-%Y")
    except Exception as e:
        print(f"WARNING: Dialog Date parse error: {e}")
        return

    dialog_id = f"{field_id}_dialog"
    wait.until(EC.visibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)

    Select(wait.until(EC.presence_of_element_located(
        (By.ID, f"{field_id}_month")))).select_by_value(str(date_obj.month - 1))
    time.sleep(0.5)
    Select(driver.find_element(By.ID, f"{field_id}_year")
           ).select_by_visible_text(str(date_obj.year))
    time.sleep(0.5)

    day_cell = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"#{dialog_id} td[data-date='{date_obj.strftime('%Y-%m-%d')}'] span")
    ))
    day_cell.click()
    time.sleep(1)

    wait.until(EC.invisibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)
    print(f"{field_id} = {date_str} done")


# LOV - With search button

def fill_lov_with_search_button(driver, wait, button_id, dialog_id, search_value):
    lov_button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
    lov_button.click()
    time.sleep(1.5)

    wait.until(EC.visibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)

    search_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, f"#{dialog_id} input.a-PopupLOV-search")
    ))
    search_input.clear()
    search_input.send_keys(search_value)
    time.sleep(0.5)

    search_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"#{dialog_id} button.a-PopupLOV-doSearch")
    ))
    search_btn.click()
    time.sleep(1.5)

    first_result = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"#{dialog_id} ul.a-IconList li.a-IconList-item:first-child")
    ))
    first_result.click()
    time.sleep(1)

    wait.until(EC.invisibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)


# LOV - Incremental search

def fill_lov_incremental(driver, wait, button_id, dialog_id, search_value):
    lov_button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
    lov_button.click()
    time.sleep(1.5)

    wait.until(EC.visibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)

    search_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, f"#{dialog_id} input.a-PopupLOV-search")
    ))
    search_input.clear()
    search_input.send_keys(search_value)
    time.sleep(2)

    first_result = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f"#{dialog_id} ul.a-IconList li.a-IconList-item:first-child")
    ))
    first_result.click()
    time.sleep(1)

    wait.until(EC.invisibility_of_element_located((By.ID, dialog_id)))
    time.sleep(0.5)


# FORM FILL

def fill_form(driver, wait, row):
    print(f"Filling form for: {row.get('Responsible Name', '')}")

    # Wait for form to load
    wait.until(EC.presence_of_element_located((By.ID, "P2_COMP_DATE_input")))
    time.sleep(1)

    # 1. Compliance Date + current time
    fill_compliance_date(driver, wait, str(row.get("Complaince Date", "")).strip())
    print("Compliance Date + Time filled successfully")

    # 2. Responsible Department
    fill_lov_incremental(driver, wait,
                         button_id="P2_RESP_DEPT_lov_btn",
                         dialog_id="PopupLov_2_P2_RESP_DEPT_dlg",
                         search_value=str(row.get("Responsible Department", "")).strip())
    print("Responsible Department filled successfully")

    # 3. Observation Detail
    obs_field = wait.until(EC.presence_of_element_located((By.ID, "P2_OBSERV_DETAIL")))
    obs_field.clear()
    obs_field.send_keys(str(row.get("Observation Detail", "")).strip())
    time.sleep(1)
    print("Observation Detail filled successfully")

    # 4. Impacts
    imp_field = wait.until(EC.presence_of_element_located((By.ID, "P2_IMPACTS")))
    imp_field.clear()
    imp_field.send_keys(str(row.get("Impact", "")).strip())
    time.sleep(1)
    print("Impacts filled successfully")

    # 5. Verification Date
    fill_dialog_date(driver, wait, "P2_VERF_DATE",
                     str(row.get("Verification Date", "")).strip())
    print("Verification Date filled successfully")

    # 6. Type of Observation
    fill_lov_with_search_button(driver, wait,
                                button_id="P2_TYPE_OF_OBSERV_lov_btn",
                                dialog_id="PopupLov_2_P2_TYPE_OF_OBSERV_dlg",
                                search_value=str(row.get("Type of Observation", "")).strip())
    print("Type of Observation filled successfully")

    # 7. Safety Requirements
    fill_lov_with_search_button(driver, wait,
                                button_id="P2_SAFTY_REQ_lov_btn",
                                dialog_id="PopupLov_2_P2_SAFTY_REQ_dlg",
                                search_value=str(row.get("Safety Requirements", "")).strip())
    print("Safety Requirements filled successfully")

    # 8. Responsible Name
    fill_lov_incremental(driver, wait,
                         button_id="P2_RESP_BY_lov_btn",
                         dialog_id="PopupLov_2_P2_RESP_BY_dlg",
                         search_value=str(row.get("Responsible Name", "")).strip())
    print("Responsible Name filled successfully")

    # 9. Target Date
    fill_dialog_date(driver, wait, "P2_TAR_DATE",
                     str(row.get("Target Date", "")).strip())
    print("Target Date filled successfully")

    # 10. Rating
    fill_lov_with_search_button(driver, wait,
                                button_id="P2_RATING_lov_btn",
                                dialog_id="PopupLov_2_P2_RATING_dlg",
                                search_value=str(row.get("Rating", "")).strip())
    print("Rating filled successfully")

    # Click Save button
    save_button = wait.until(EC.element_to_be_clickable((By.ID, "B208450801380139083")))
    save_button.click()
    print("Save button clicked")

    # Wait for next page and click Create button
    time.sleep(3)
    create_button = wait.until(EC.element_to_be_clickable((By.ID, "B145595537551445625")))
    create_button.click()
    print("Create button clicked")

    # Wait for form to reload for next entry
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.ID, "P2_COMP_DATE_input")))
    time.sleep(1)
    print("Form is ready for next entry")


# LOGIN

def login_to_portal():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)

    driver.get("enter your url")
    time.sleep(1)
    print("Portal opened successfully")

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "P9999_USERNAME")))
    username_field.clear()
    time.sleep(1)
    username_field.send_keys("USER NAME ")
    time.sleep(1)
    print("Username entered")

    password_field = driver.find_element(By.NAME, "P9999_PASSWORD")
    password_field.clear()
    time.sleep(1)
    password_field.send_keys("PASSWORD")
    time.sleep(1)
    print("Password entered")

    sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, "B7098192448691739")))
    sign_in_button.click()
    time.sleep(1)
    print("Sign In clicked")

    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    print("Page reloaded")

    cms_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Complaint Management System']/..")
    ))
    cms_link.click()
    time.sleep(1)
    print("Complaint Management System opened")

    menu_button = wait.until(EC.element_to_be_clickable((By.ID, "t_Button_navControl")))
    menu_button.click()
    time.sleep(1)
    print("Navigation menu opened")

    nc_entry_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='NC ENTRY TEST']")
    ))
    nc_entry_link.click()
    time.sleep(2)
    print("NC ENTRY TEST form opened")

    return driver, wait


# MAIN LOOP

def run_automation(df):
    driver, wait = login_to_portal()

    total = len(df)
    for index, row in df.iterrows():
        print(f"\n{'='*40}")
        print(f"Processing entry {index + 1} of {total}")
        print(f"{'='*40}")

        # Check if browser session is still active
        try:
            driver.title
        except Exception:
            print("Browser session lost - logging in again...")
            driver, wait = login_to_portal()

        try:
            fill_form(driver, wait, row)
        except Exception as e:
            print(f"ERROR on entry {index + 1}: {e}")

            # Check session again after error
            try:
                driver.title
            except Exception:
                print("Session expired - restarting browser...")
                try:
                    driver.quit()
                except:
                    pass
                driver, wait = login_to_portal()

            print("Skipping to next entry...")
            continue

    print("\nAll entries have been submitted successfully!")
    try:
        driver.quit()
    except:
        pass


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("test.csv")
    run_automation(df)
