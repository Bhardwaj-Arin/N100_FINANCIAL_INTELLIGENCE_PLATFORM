# N100 Financial Intelligence Platform

# Installation Guide

Version: 1.0.0

---

# Table of Contents

1. Introduction
2. System Requirements
3. Prerequisites
4. Project Structure
5. Clone the Repository
6. Create a Virtual Environment
7. Install Dependencies
8. Dataset Setup
9. Database Setup
10. Running the Application
11. Running Tests
12. Deployment
13. Common Issues & Troubleshooting
14. Updating the Project
15. Uninstalling the Project
16. Support

---

# 1. Introduction

This guide provides step-by-step instructions for installing and running the **N100 Financial Intelligence Platform**.

The platform is built using **Python**, **Streamlit**, **SQLite**, and several data science libraries. Following this guide will allow you to run the application locally and explore its financial analytics dashboard.

---

# 2. System Requirements

### Operating Systems

- Windows 10 / 11
- macOS
- Linux (Ubuntu or equivalent)

---

### Recommended Hardware

| Component | Requirement |
|------------|-------------|
| Processor | Intel i5 / AMD Ryzen 5 or higher |
| RAM | 8 GB minimum (16 GB recommended) |
| Storage | 2 GB free space |
| Internet | Required for cloning the repository |

---

### Software Requirements

- Python 3.10 or later
- Git
- Visual Studio Code (Recommended)
- Streamlit

---

# 3. Prerequisites

Verify the following software is installed.

### Python

```bash
python --version
```

Expected Output

```text
Python 3.10+
```

---

### Git

```bash
git --version
```

---

### Pip

```bash
pip --version
```

---

# 4. Project Structure

```
N100-Financial-Intelligence-Platform/

│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── components/
├── dashboards/
├── pages/
├── src/
├── data/
├── db/
├── docs/
├── notebooks/
├── reports/
└── tests/
```

---

# 5. Clone the Repository

Clone the GitHub repository.

```bash
git clone https://github.com/Bhardwaj-Arin/N100-Financial-Intelligence-Platform.git
```

Navigate to the project directory.

```bash
cd N100-Financial-Intelligence-Platform
```

---

# 6. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### macOS / Linux

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

# 7. Install Dependencies

Install all required packages.

```bash
pip install -r requirements.txt
```

Typical libraries include:

- streamlit
- pandas
- numpy
- plotly
- matplotlib
- openpyxl

---

# 8. Dataset Setup

Place the project datasets inside the appropriate data directories.

```
data/

├── raw/
└── processed/
```

The processed dataset used by the dashboard is:

```
master_features.csv
```

Ensure the dataset is available before running the application.

---

# 9. Database Setup

The platform uses **SQLite** for storing processed financial data.

Database files are located in:

```
db/
```

Example:

```
financial_platform.db

financial_data.db

nifty100.db
```

If a database initialization script is included, execute it before launching the application.

```
db/schema.sql
```

---

# 10. Running the Application

Start the Streamlit application.

```bash
streamlit run app.py
```

After execution, Streamlit will generate a local URL.

Example

```
http://localhost:8501
```

Open the URL in your web browser.

---

# 11. Running Tests

Navigate to the project directory.

Run all available tests.

```bash
pytest
```

or execute individual test files.

```bash
python tests/test_dashboard.py
```

The application should complete all tests without errors.

---

# 12. Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment Steps

1. Push the latest code to GitHub.
2. Log in to Streamlit Community Cloud.
3. Create a new application.
4. Select the repository.
5. Choose:

```
app.py
```

6. Deploy the application.

After deployment, verify:

- Dashboard
- Company Profile
- Rankings
- Investment Screener
- Portfolio Analytics
- Downloads
- Filters
- Charts

---

# 13. Common Issues & Troubleshooting

## ModuleNotFoundError

Install dependencies again.

```bash
pip install -r requirements.txt
```

---

## Streamlit Command Not Found

Install Streamlit.

```bash
pip install streamlit
```

---

## Missing Dataset

Verify

```
data/processed/master_features.csv
```

exists.

---

## Database Connection Error

Verify SQLite database files are present inside

```
db/
```

---

## Application Not Opening

Restart Streamlit.

```bash
streamlit run app.py
```

---

# 14. Updating the Project

Pull the latest version.

```bash
git pull origin main
```

Install any new dependencies.

```bash
pip install -r requirements.txt
```

Restart the application.

```bash
streamlit run app.py
```

---

# 15. Uninstalling the Project

Deactivate the virtual environment.

Windows

```bash
deactivate
```

macOS / Linux

```bash
deactivate
```

Delete the project folder if no longer required.

---

# 16. Support

For project-related issues:

- Verify dependencies are installed.
- Confirm the dataset and database files are available.
- Check the terminal output for detailed error messages.
- Refer to the project documentation for additional guidance.

---

# Installation Summary

The N100 Financial Intelligence Platform is designed to be simple to install and run. After cloning the repository, installing the required dependencies, configuring the dataset and SQLite database, and launching the Streamlit application, users can explore financial analytics through an interactive dashboard featuring company analysis, rankings, financial health scoring, investment screening, cash flow intelligence, and portfolio analytics.