# Coupon Management System

A full-stack Coupon Management application built with **Python** and **FastAPI**. It features a rule-based discount engine, a REST API, and a simple web interface (UI) for Admins to create coupons and Customers to shop and apply the best discounts automatically.

## 🚀 Project Overview
This system solves the problem of finding the "Best Coupon" for a user's shopping cart. It allows:
* **Admins** to create coupons with complex rules (minimum cart value, specific user tiers, date ranges).
* **Customers** to shop, view their cart, and automatically get the highest discount available.
* **Developers** to interact with the core logic via a Swagger API.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI (Backend API)
* **Templating:** Jinja2 (Frontend UI)
* **Server:** Uvicorn
* **Storage:** In-Memory (Python Dictionaries/Lists)
* **Validation:** Pydantic

## ⚙️ How to Run

### 1. Prerequisites
Ensure you have Python installed. You can verify this by running:
```bash
python --version
# Should be Python 3.10 or higher
```

### 2. Setup
Clone the repository and install the dependencies.

Step 1: Create a virtual environment (Recommended)

```bash

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
Step 2: Install dependencies

```bash

pip install fastapi uvicorn jinja2 aiofiles
```

### 3. Start the Application
Run the server using Uvicorn:

```bash

uvicorn main:app --reload
```
The application will start at: http://127.0.0.1:8000

🔑 Demo Credentials (Admin)
To test the Admin features immediately, use the hardcoded demo credentials required by the assignment:

**Email:** hire-me@anshumat.org

**Password:** HireMe@2025!

**Note:** You can also Sign Up as a new user to test the "Customer" flow.

### 📱 Features & Usage
**1. Web Interface (UI)**
**Login Page (/):** Toggle between Login and Sign Up. Redirects users based on their role (Admin -> Dashboard, Customer -> Shop).

**Admin Dashboard (/admin):** Create new coupons with rules like "Flat Amount" or "Percentage", start/end dates, and eligibility criteria.

**Shop (/shop):** A simulation of an e-commerce cart. Add items and click "Find Best Coupon" to trigger the backend logic.

**2. API Endpoints**
You can interact with the raw API via the automatic Swagger documentation at: http://127.0.0.1:8000/docs

**POST /coupons:** Create a coupon.

**POST /applicable-coupons:** The core logic engine. Inputs a User + Cart and returns the best specific coupon.

**POST /login & /signup:** Authentication endpoints.

### ⚠️ Important Note
Persistence: This project uses In-Memory Storage (Python dictionaries) as allowed by the assignment requirements.

If you restart the server, all created coupons and new users will be reset.

The hardcoded Admin credentials will always work.


### 📂 Project Structure
```bash

coupon-system/
├── main.py          # Application entry point & API routes
├── models.py        # Pydantic data models (Schemas)
├── logic.py         # Discount calculation & eligibility rules
├── templates/       # HTML files for the UI
│   ├── login.html
│   ├── admin.html
│   └── shop.html
└── README.md        # Project documentation
```
🤖 AI Usage Disclosure
I utilized AI tools (Gemini) to assist with the development of this project. Specifically:

**Schema Design:** Clarifying how to nest Pydantic models for the complex eligibility JSON structure.

**Logic Refinement:** Improving the set intersection logic for category-based coupon rules.

**Frontend Templates:** Generating the HTML/CSS boilerplate for the Admin and Shop pages to ensure a clean UI without using a heavy frontend framework.