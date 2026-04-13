# 🚀 QA AI Automation System

## 📌 Overview

This project is an AI-powered QA automation system designed to simulate and validate user flows such as login, checkout, and payment processes. It leverages browser automation to execute test steps and capture visual evidence for each stage.

---

## 🧠 Key Features

* Automated end-to-end test execution
* Step-by-step screenshot capture
* Modular backend architecture
* Lightweight frontend interface
* Support for multiple test scenarios (e.g., USD, MYR flows)

---

## 🏗️ Project Structure

```
QA_AI_Automation/
│
├── backend/              # Core backend (Flask APIs)
│   ├── app.py           # Entry point
│   ├── config.py        # Configurations
│   └── engine/          # Automation & execution logic
│
├── frontend/            # UI (HTML, CSS, JS)
│
├── storage/
│   └── runs/            # Stores test execution screenshots
│
├── test_cases.py        # Script to trigger test cases
├── requirements.txt     # Dependencies
├── RESTART.bat          # Clean restart script
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** Python (Flask)
* **Automation:** Playwright
* **Frontend:** HTML, CSS, JavaScript
* **Storage:** Local file system

---

## ▶️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/yuzvendhrachahal-dev/QA_Automation.git
cd QA_AI_Automation
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file in root directory and add required keys:

```
# Example
API_KEY=your_api_key_here
```

---

### 5. Run the Application

```
RESTART.bat
```

Backend will run at:

```
http://127.0.0.1:5000
```

---

### 6. Open Frontend

Open:

```
frontend/index.html
```

---

## 📂 Output

* Test results and screenshots are stored in:

```
storage/runs/
```

---

## 🔄 Restart Behavior

The `RESTART.bat` script:

* Clears Python cache
* (Optional) Clears previous test runs
* Starts the backend server

---

## ⚠️ Notes

* `.env` file is not included for security reasons
* Ensure Playwright dependencies are installed if required
* This is a development setup (not production optimized)

---

## 🚀 Future Enhancements

* CI/CD integration
* Cloud storage for test artifacts
* Advanced reporting dashboard
* AI-based test generation

---

## 👤 Maintainer

Nivash R N

---
