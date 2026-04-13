# 🚀 QA AI Automation System

## 📌 Overview

This project is an AI-powered QA automation system designed to simulate and validate user flows such as login, checkout, and payment processes. It uses browser automation to execute test steps and capture screenshots for each stage.

---

## 🧠 Features

* Automated end-to-end testing
* Step-by-step screenshot capture
* Supports multiple flows (e.g., USD, MYR)
* Backend API-driven architecture
* Simple frontend UI for triggering flows

---

## 🏗️ Project Structure

```
QA_AI_Automation/
│
├── backend/              # Flask backend (API + execution logic)
│   ├── app.py           # Entry point
│   ├── config.py        # Configurations
│   └── engine/          # Core automation logic
│
├── frontend/            # UI (HTML, CSS, JS)
│
├── storage/
│   └── runs/            # Stores screenshots of test runs
│
├── test_cases.py        # Script to trigger automation
├── requirements.txt     # Python dependencies
├── RESTART.bat          # Clean restart script
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** Python (Flask)
* **Automation:** Playwright
* **Frontend:** HTML, CSS, JavaScript
* **Storage:** Local filesystem

---

## 📦 Prerequisites

Ensure the following are installed:

### 1. Python

* Version: **3.9+**
* Check:

```
python --version
```

---

### 2. Git

* Required for cloning the repository

---

### 3. Playwright Browsers

After installing dependencies, run:

```
playwright install
```

---

## ⚡ Installation & Setup

### Step 1: Clone Repository

```
git clone https://github.com/yuzvendhrachahal-dev/QA_Automation.git
cd QA_AI_Automation
```

---

### Step 2: Create Virtual Environment

```
python -m venv venv
```

Activate:

**Windows**

```
test\Scripts\activate
```

---

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```
# Example
API_KEY=your_api_key_here
---

## ▶️ Running the Project

### Option 1: Using Restart Script (Recommended)

```
RESTART.bat
```

This will:

* Clear Python cache
* (Optional) Clear previous test screenshots
* Start the backend server

---

### Option 2: Manual Run

```
python -m backend.app
```

---

### Backend will run at:

```
http://127.0.0.1:5000
```

---

## 🌐 Running Frontend

Open the file:

```
frontend/index.html
```

OR use VS Code Live Server.

---

## 🧪 Running Test Cases

```
python test_cases.py
```

---

## 📂 Output

Test execution results (screenshots) are stored in:

```
storage/runs/
```

Each run generates a unique folder with step-by-step screenshots.

---

## 🔄 Restart Behavior

`RESTART.bat` performs:

* Python cache cleanup
* Deletes old test run screenshots
* Starts the backend server

---

## Example Test case
----
Open URL

click success homas
click astroved temple services
wait until page is loaded
click astroved temple services for ketu
wait until page is loaded

click abishekam
wait 3
click homa
wait 3
click pooja
wait 3

click add to cart
wait 2
click keep shopping

Click 9 Days
click add to cart
wait 2
click keep shopping

Click 11 Days
click add to cart
wait 2
click keep shopping

Click 21 Days
click add to cart
wait 2
click keep shopping

Click 30 Days
click add to cart
wait 2
click keep shopping

Click 48 Days
click add to cart
wait 2
click keep shopping

Click 90 Days
click add to cart
wait 2
click keep shopping

Click 108 Days
click add to cart
wait 2
click keep shopping

Click 180 Days
click add to cart
wait 2
click keep shopping

Click 365 Days
click add to cart
wait 2
click keep shopping

home
wait until page is loaded

-----

## ⚠️ Important Notes

* `.env` file is not included for security reasons
* Ensure Playwright is installed properly
* This setup is for development (not production-ready)
* Run from project root directory
