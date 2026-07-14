# 🤖 AI Powered QA Automation Testing Platform

An enterprise-grade AI-assisted QA Automation platform built using **Python**, **Flask**, **Playwright**, and modern browser automation techniques.

The application enables QA engineers to execute human-readable test cases against any website, automatically performs browser interactions using Playwright, captures step-by-step screenshots, validates execution results, and generates comprehensive QA reports.

Designed to simplify UI testing by allowing users to write natural language test steps instead of complex automation scripts.

---

# 🚀 Features

- AI-assisted UI automation workflow
- Human-readable test case execution
- Playwright browser automation
- Automatic screenshot capture for every test step
- Step-by-step execution reports
- Event validation support
- Browser navigation automation
- Dynamic report generation
- Cross-platform execution (Windows / Linux)
- Flask REST API backend
- Lightweight web interface
- Production deployment support

---

# 🏗 System Architecture

```

                +---------------------------+
                |      Web Frontend         |
                | HTML • CSS • JavaScript   |
                +-------------+-------------+
|
Natural Language Test Cases
|
▼
+---------------------------+
| Flask Backend API |
+-------------+-------------+
|
▼
+---------------------------+
| Test Execution Engine |
+-------------+-------------+
|
▼
+---------------------------+
| Playwright Automation |
+-------------+-------------+
|
+-------------------+-------------------+
| |
▼ ▼
Browser Automation Screenshot Capture
|
▼
Execution Report
```

---

# 📂 Project Structure

```
QA_Automation/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── engine/
│   │    ├── automation_engine.py
│   │    ├── parser.py
│   │    └── ...
│   │
│   ├── templates/
│   │    └── index.html
│   │
│   └── static/
│        ├── app.js
│        └── style.css
│
├── storage/
│   └── runs/
│        └── <Run ID>/
│             ├── step_1.png
│             ├── step_2.png
│             └── ...
│
├── test_cases.py
├── requirements.txt
├── RESTART.bat
└── README.md
```

---

# ⚙️ Tech Stack

## Backend

- Python
- Flask
- Playwright
- Requests

## Frontend

- HTML5
- CSS3
- JavaScript

## Browser Automation

- Microsoft Playwright

## Deployment

- Ubuntu Server
- Nginx (Deployment Ready)

---

# 🤖 AI Assisted Test Execution

Instead of writing traditional automation scripts, users provide human-readable test instructions.

Example:

```
Open URL

Click Free Astrology

Click Free Horoscope

Wait until page is loaded

Click Zodiac

Wait 3

Home
```

The application parses these instructions and converts them into Playwright browser automation commands.

Internally they are translated into actions such as:

```
page.goto()

page.click()

page.wait_for_load_state()

page.go_back()

page.screenshot()
```

This significantly reduces manual scripting effort for UI testing.

---

# 📸 Screenshot Generation

During execution the engine automatically captures screenshots after every important action.

Example:

```
storage/

└── runs/

      └── 96d66ee5/

            step_1.png

            step_2.png

            step_3.png

            ...
```

These screenshots are embedded into the generated QA report.

---

# 📊 Execution Workflow

```
User submits test

↓

Backend receives request

↓

Playwright launches browser

↓

Website opens

↓

Each step executed sequentially

↓

Screenshot captured

↓

Execution status validated

↓

QA report generated
```

---

# ⚡ Key Features

- Human-readable test execution
- Browser automation using Playwright
- Screenshot evidence generation
- Dynamic execution reports
- Event validation
- Modular backend architecture
- REST API driven workflow
- Cross-platform compatibility
- Deployment-ready architecture

---

# 🌐 Deployment

The application has been successfully deployed on Ubuntu Server.

Public URL

```
https://qa-autm.astroved.com/frontend/
```

The deployment supports browser-based execution without requiring any local setup for end users.

---

# ▶️ Running Locally

## Clone Repository

```bash
git clone https://github.com/yuzvendhrachahal-dev/QA_Automation.git

cd QA_Automation
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright Browsers

```bash
playwright install
```

---

## Configure Environment

Create a `.env` file and configure the required application settings.

---

## Run Application

```bash
python -m backend.app
```

Open:

```
http://127.0.0.1:5000
```

---

# 📌 API

```
POST /run
```

Executes the submitted test case and returns:

- Test Status
- Execution Results
- Screenshots
- Validation Report

---

# 🧠 Key Concepts Demonstrated

- AI Assisted Automation
- Browser Automation
- Playwright
- Flask API Development
- REST API Design
- UI Test Automation
- Screenshot Evidence Generation
- Natural Language Test Execution
- Cross-platform Deployment
- Automation Framework Design

---

# 🚀 Future Enhancements

- LLM-powered test case generation
- Natural language to Playwright conversion
- Parallel test execution
- PDF report generation
- Dashboard with execution history
- CI/CD integration
- Docker support
- Authentication & Role-based Access
- Cloud storage for reports

---

# 👨‍💻 Author

**Nivash R N**

Associate AI Engineer

- GitHub: https://github.com/RNNivash
- LinkedIn: https://linkedin.com/in/nivash-r-n
