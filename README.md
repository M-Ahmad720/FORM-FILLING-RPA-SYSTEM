# RPA - Automated Form Submission System

An RPA (Robotic Process Automation) tool that reads data from a CSV or Excel file and automatically fills and submits a web-based HR portal form using Selenium and Streamlit.

---

## Features

- Upload CSV or Excel files through a clean web interface
- Automatically parses and displays file data before submission
- Fills all form fields including date pickers, dropdowns, and text areas
- Handles multiple entries in a loop — one form submission per row
- Auto-restarts browser session if it expires during execution
- Built with Python, Selenium, and Streamlit

---

## Project Structure

```
rpa_project/
│
├── app.py                  # Streamlit frontend - file upload and submission trigger
├── portal_automation.py    # Selenium automation - login, navigation, and form filling
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## Prerequisites

- Python 3.11 or higher
- Google Chrome browser installed
- Internet access (for ChromeDriver auto-download)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/rpa_project.git
cd rpa_project
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

Before running the project, open `portal_automation.py` and update the following:

```python
# Portal URL
driver.get("YOUR_PORTAL_URL_HERE")

# Login credentials
username_field.send_keys("YOUR_USERNAME")
password_field.send_keys("YOUR_PASSWORD")
```

> **Note:** Never commit your credentials to GitHub. Consider using a `.env` file and `python-dotenv` for secure credential management.

---

## Usage

**1. Start the Streamlit app**

```bash
streamlit run app.py
```

**2. Open your browser**

The app will automatically open at `http://localhost:8501`

**3. Upload your file**

Upload a `.csv` or `.xlsx` file with the following columns:

| Column Name | Description |
|---|---|
| Complaince Date | Date of compliance (format: DD-Mon-YY) |
| Responsible Department | Department name |
| Observation Detail | Detail of the observation |
| Impact | Impact description |
| Verification Date | Date of verification |
| Type of Observation | Type (e.g. Internal Audit, Safety Walk) |
| Safety Requirements | Safety requirement category |
| Responsible Name | Name of responsible person |
| Target Date | Target completion date |
| Rating | Rating value (e.g. D, E) |

**4. Submit**

Click the **Submit to Portal** button. Chrome will open automatically and start filling the form entry by entry.

---

## Dependencies

```
selenium
webdriver-manager
pandas
openpyxl
streamlit
```

---

## How It Works

1. User uploads a CSV or Excel file via the Streamlit interface
2. The app parses and displays the data for review
3. On clicking Submit, `run_automation()` is called
4. The script logs into the portal, navigates to the form, and fills each row one by one
5. After each entry, it clicks Save then Create to submit and reset the form
6. If the browser session is lost, it automatically re-logs in and continues

---

## Security Notice

- Do **not** hardcode credentials in your code before pushing to GitHub
- Add a `.env` file for credentials and add it to `.gitignore`
- Example `.gitignore` entry:

```
.env
venv/
__pycache__/
```

---

## License

This project is for internal use only.
