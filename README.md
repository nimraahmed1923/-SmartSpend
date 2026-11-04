# SmartSpend – Expense Tracking and Monthly Budget Management System

## About the Project

SmartSpend is a Python-based expense tracking and monthly budget management application. It helps users record their daily expenses, manage their monthly budget, and understand where their money is being spent.

The application provides a dashboard with spending summaries, category-wise analysis, budget allocation, progress bars, and alerts.

## Features

- Add, view, edit, and delete expenses.
- Set and manage a monthly budget.
- Track total spending and remaining budget.
- View category-wise expense summaries.
- Divide the monthly budget into 70% expense allocation and 30% savings allocation.
- Monitor spending through dynamic progress bars.
- Receive alerts when approaching or exceeding budget limits.
- View recent expenses on the dashboard.

## Technologies Used

- Python – Core programming logic
- Streamlit – Frontend and dashboard
- FastAPI – Backend API
- JSON – Data storage
- Requests – Frontend and backend communication

## Project Structure

```text
SmartSpend/
│
├── app.py
├── fastapi_app.py
├── main.py
├── storage.py
├── requirements.txt
├── README.md
├── budget.json
└── expenses.json
```

## How to Run the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend

```bash
python -m uvicorn fastapi_app:app --reload
```

### 3. Start the Streamlit Frontend

Open another terminal and run:

```bash
python -m streamlit run app.py
```

### 4. Open the Application

The Streamlit application will open in your browser.

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Project Objective

The main objective of SmartSpend is to make expense tracking and monthly budget management easier. It helps users understand their spending habits, control unnecessary expenses, and maintain a planned savings allocation.
