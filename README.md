# Receipt & Expense Tracker

An AI-powered Vision-based Receipt and Expense Tracker built using Python, Streamlit, and Google Gemini Vision.

The application allows users to upload a receipt image and automatically extract important expense information such as merchant name, purchased items, prices, taxes, total amount, payment method, and expense category.

---

## 1. Project Overview

Manual expense tracking requires users to enter receipt information one transaction at a time.

This project uses Vision AI to automate the process.

The basic workflow is:

```text
Receipt Image
     |
     v
Streamlit Upload
     |
     v
Gemini Vision AI
     |
     v
Receipt Information Extraction
     |
     v
Expense Categorization
     |
     v
Amount Validation
     |
     v
Structured Expense Result
```

---

# 2. Features

* Receipt image upload
* AI-powered receipt analysis
* Merchant information extraction
* Date and time extraction
* Item and quantity extraction
* Price extraction
* Subtotal extraction
* Discount detection
* GST, CGST, SGST and IGST detection
* Total amount extraction
* Payment method detection
* Automatic expense categorization
* Receipt validation
* Confidence estimation
* Missing information handling
* Streamlit web interface
* Secure API key management

---

# 3. Technology Stack

| Technology       | Purpose                 |
| ---------------- | ----------------------- |
| Python           | Application development |
| Streamlit        | Web interface           |
| Google Gemini    | Vision AI               |
| Google GenAI SDK | Gemini API integration  |
| Git              | Version control         |
| GitHub           | Repository hosting      |

---

# 4. Project Structure

```text
receipt-expense-tracker/
│
├── .streamlit/
│   └── secrets.toml
│
├── venv/
│
├── app.py
├── prompts.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 5. app.py

The following is the main Streamlit application:

```python
import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Receipt & Expense Tracker",
    page_icon="🧾",
    layout="centered"
)


# --------------------------------
# Gemini Client
# --------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# --------------------------------
# Application Header
# --------------------------------

st.title("Receipt & Expense Tracker")

st.caption(
    "Snap it. Track it. Understand your spending."
)

st.write(
    "Upload a receipt image and let AI extract "
    "the expense information automatically."
)


# --------------------------------
# Receipt Upload
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload your receipt",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)


# --------------------------------
# Receipt Analysis
# --------------------------------

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Receipt",
        use_container_width=True
    )

    if st.button(
        "Analyze Receipt",
        type="primary"
    ):

        with st.spinner(
            "Analyzing receipt..."
        ):

            try:

                # Read uploaded image
                image_bytes = (
                    uploaded_file.getvalue()
                )

                # Send image and prompt
                response = client.models.generate_content(
                    model="gemini-2.5-flash",

                    contents=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=uploaded_file.type
                        ),

                        SYSTEM_PROMPT
                    ]
                )

                # --------------------------------
                # Display Result
                # --------------------------------

                st.success(
                    "Receipt analyzed successfully."
                )

                st.subheader(
                    "Receipt Details"
                )

                st.write(
                    response.text
                )

            except Exception as error:

                st.error(
                    "Unable to analyze the receipt."
                )

                st.write(
                    str(error)
                )
```

---

# 6. prompts.py

The system prompt controls how Gemini behaves when analyzing receipts.

```python
SYSTEM_PROMPT = """
You are an AI-powered Receipt & Expense Tracker Assistant.

Your main responsibility is to analyze receipt images
and extract accurate expense information.

PERSONA:

You are:

- Helpful
- Accurate
- Organized
- Clear
- Trustworthy

Your responses should be simple and easy to understand.

--------------------------------
RECEIPT INFORMATION
--------------------------------

Extract the following information when visible:

1. Merchant name
2. Merchant address
3. Receipt number
4. Invoice number
5. Date
6. Time
7. Currency
8. Purchased items
9. Quantity
10. Unit price
11. Item total
12. Subtotal
13. Discount
14. Tax
15. CGST
16. SGST
17. IGST
18. GSTIN
19. Total amount
20. Payment method

--------------------------------
EXPENSE CATEGORIES
--------------------------------

Classify the expense into one of these categories:

- Food & Dining
- Groceries
- Transportation
- Shopping
- Healthcare
- Education
- Entertainment
- Utilities
- Travel
- Bills
- Personal Care
- Electronics
- Other

--------------------------------
IMPORTANT RULES
--------------------------------

1. Never invent information.

2. If information is missing,
   return "Not detected".

3. If text is unclear,
   return "Uncertain".

4. Preserve the original currency.

5. Check the mathematical consistency
   of subtotal, discount, tax and total.

6. Mention any detected inconsistency.

7. If the image is not a receipt,
   return:

   "This image does not appear to be a receipt."

--------------------------------
OUTPUT FORMAT
--------------------------------

Merchant:
Date:
Time:
Receipt Number:
Currency:

Items:

- Item Name
- Quantity
- Unit Price
- Total Price

Subtotal:
Discount:
Tax:
CGST:
SGST:
IGST:
Total:

Payment Method:

Expense Category:

Validation:

Confidence:

Keep the output structured,
clear and easy to understand.
"""
```

---

# 7. requirements.txt

Create a file named `requirements.txt`:

```text
streamlit
google-genai
```

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 8. .gitignore

Create a `.gitignore` file:

```text
venv/
__pycache__/
*.pyc

.streamlit/secrets.toml

.env
.env.*
```

This prevents your virtual environment and API key from being uploaded to GitHub.

---

# 9. secrets.toml

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace `YOUR_GEMINI_API_KEY` with your actual API key.

Do not upload this file to GitHub.

---

# 10. Installation

First clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/receipt-expense-tracker.git
```

Move into the project:

```bash
cd receipt-expense-tracker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 11. Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The terminal will show something similar to:

```text
Local URL: http://localhost:8501
Network URL: http://10.x.x.x:8501
```

Open the Local URL in your browser.

---

# 12. Application Workflow

```text
User
 |
 | Upload Receipt
 v
Streamlit
 |
 | Image
 v
Gemini Vision
 |
 | Analyze Image
 v
Prompt Engineering
 |
 | Extract Information
 v
Receipt Data
 |
 +---------------------+
 |                     |
 v                     v
Category           Validation
 |                     |
 +----------+----------+
            |
            v
      Expense Result
```

---

# 13. Example AI Output

For example, if the user uploads a grocery receipt:

```text
Merchant:
ABC Supermarket

Date:
2026-10-01

Time:
18:42

Receipt Number:
INV10245

Currency:
INR

Items:

- Milk | Quantity: 2 | Unit Price: ₹30 | Total: ₹60
- Bread | Quantity: 1 | Unit Price: ₹45 | Total: ₹45

Subtotal:
₹105

Discount:
₹5

Tax:
₹0

CGST:
Not detected

SGST:
Not detected

IGST:
Not detected

Total:
₹100

Payment Method:
UPI

Expense Category:
Groceries

Validation:
Consistent

Confidence:
96%
```

The actual output depends on the information available in the uploaded receipt.

---

# 14. Expense Categories

The system supports:

```text
Food & Dining
Groceries
Transportation
Shopping
Healthcare
Education
Entertainment
Utilities
Travel
Bills
Personal Care
Electronics
Other
```

---

# 15. Error Handling

The application handles common problems such as:

```text
Invalid image
Missing receipt information
Unreadable receipt
Non-receipt image
Invalid API key
API errors
Network errors
```

For example:

```text
This image does not appear to be a receipt.
```

or:

```text
Merchant:
Not detected
```

The system is instructed not to invent information.

---

# 16. Security

The Gemini API key is stored using Streamlit Secrets.

The API key should never be written directly inside `app.py`.

Correct:

```python
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
```

Incorrect:

```python
client = genai.Client(
    api_key="my-secret-api-key"
)
```

The following should not be committed:

```text
.streamlit/secrets.toml
.env
venv/
```

---

# 17. Privacy

Receipts can contain sensitive information such as:

* Customer names
* Addresses
* Phone numbers
* Transaction information
* Merchant information
* Payment details

Users should avoid uploading documents containing unnecessary sensitive information.

A production version should implement appropriate security controls, access control, encryption, and data-retention policies.

---

# 18. Future Enhancements

The current application can be extended into a complete expense-management platform.

### Expense Database

Add:

```text
SQLite
MySQL
PostgreSQL
MongoDB
```

to permanently store transactions.

### Dashboard

Add:

```text
Total Expenses
Monthly Expenses
Daily Expenses
Category Breakdown
Largest Expense
Spending Trends
```

### Charts

Add visualizations such as:

```text
Pie Chart
Bar Chart
Line Chart
Category-wise Spending
Monthly Spending
```

### Budget Management

Allow users to define budgets:

```text
Food Budget: ₹5,000
Transport Budget: ₹2,000
Shopping Budget: ₹3,000
```

The system can then compare actual spending with the budget.

### Expense Search

Allow users to search:

```text
Find all grocery expenses.

Show expenses above ₹1,000.

Show my expenses from September.

Show all UPI transactions.
```

### Natural Language Expense Assistant

Users could ask:

```text
How much did I spend this month?

What is my biggest expense?

How much did I spend on food?

How much GST did I pay?

Show my shopping expenses.
```

### Export

Allow users to export data as:

```text
CSV
Excel
PDF
```

### WhatsApp Summary

Generate a simple spending summary that can be shared through WhatsApp.

Example:

```text
Monthly Expense Summary

Total Spent: ₹12,450

Food: ₹3,200
Groceries: ₹2,850
Transport: ₹1,600
Shopping: ₹2,100
Other: ₹2,700

Transactions: 32
```

---

# 19. Use Cases

This system can be used by:

* Students
* Employees
* Families
* Small businesses
* Individual users
* Expense management applications
* Receipt digitization systems

---

# 20. Learning Outcomes

This project demonstrates practical experience with:

* Python
* Streamlit
* Generative AI
* Vision AI
* Prompt Engineering
* API Integration
* Image Processing
* Data Extraction
* Expense Classification
* Validation
* Git
* GitHub
* Secure API-key management

---

# 21. Project Roadmap

### Phase 1

Completed:

* Streamlit application
* Receipt upload
* Gemini Vision integration
* Receipt information extraction
* Expense categorization
* Basic validation

### Phase 2

Planned:

* Database
* Expense history
* Dashboard
* Charts
* Search and filtering

### Phase 3

Planned:

* Budget management
* Spending alerts
* CSV/Excel export
* Natural-language queries
* WhatsApp summaries

### Phase 4

Planned:

* User authentication
* Cloud deployment
* Multi-user support
* Advanced analytics

---

# 22. Contributing

Contributions are welcome.

Fork the repository:

```bash
git clone https://github.com/YOUR-USERNAME/receipt-expense-tracker.git
```

Create a branch:

```bash
git checkout -b feature/new-feature
```

Add your changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Add new feature"
```

Push:

```bash
git push origin feature/new-feature
```

Then create a Pull Request.

---

# 23. Project Status

Current status:

```text
Prototype
```

The current version focuses on:

```text
Receipt Upload
       ↓
Vision AI Analysis
       ↓
Information Extraction
       ↓
Expense Categorization
       ↓
Validation
       ↓
Result Display
```

The next stage is to add persistent storage and an expense analytics dashboard.

---


---

# 25. License

This project is developed for educational and demonstration purposes.

A suitable open-source license can be added if the repository is intended for public reuse.
