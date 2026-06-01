# 🔐 Cybercrime Reporting System

A secure, full-stack web application built with **Flask & MySQL** for reporting, managing, and tracking cybercrime cases with evidence handling and email notifications.

---

## 📸 Features

- 👤 **Dual Role Login** — Separate portals for Users and Admin
- 📝 **Case Registration** — Users can file cybercrime complaints with full details
- 📎 **Evidence Upload** — Supports images, videos, audio, PDFs (up to 20 files)
- 📧 **Email Notification** — Auto-sends confirmation email with Reference ID on registration
- 🔍 **Case Tracker** — Users can track case status by Reference ID or Name
- 🛡️ **Admin Dashboard** — Full case management with search, status updates, and delete
- 📄 **Report Card** — Printable official receipt generated after case submission
- 🗄️ **MySQL Database** — Auto-initializes database and table on first run

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/FLASK-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MYSQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## 📁 Project Structure

```
CCRS/
├── app.example.py        # Main Flask app (use as template — add your credentials)
├── templates/
│   ├── login.html        # Login page (User & Admin)
│   ├── user.html         # Case registration form
│   ├── admin.html        # Admin dashboard
│   ├── tracker.html      # Case tracker for users
│   ├── view.html         # Detailed case view for admin
│   └── report_card.html  # Printable case receipt
├── static/
│   └── uploads/          # Evidence files (ignored by git)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/just-gautam/cybercrime-reporting-system.git
cd cybercrime-reporting-system
```

### 2. Install dependencies
```bash
pip install flask mysql-connector-python python-dotenv
```

### 3. Setup MySQL (XAMPP)
- Start **Apache** and **MySQL** in XAMPP
- The app auto-creates the `cybercrime_db` database on first run

### 4. Configure credentials
- Copy `app.example.py` → rename to `app.py`
- Fill in your email and passwords:
```python
server.login("your_email@gmail.com", "your_app_password")
```

### 5. Run the app
```bash
python app.py
```
Visit: `http://localhost:5001`

---

## 🔑 Default Login Credentials

| Role  | Password   |
|-------|------------|
| Admin | Set in app.py |
| User  | Set in app.py |

---

## 📋 Crime Categories Supported

Online Fraud · Phishing · Ransomware · Identity Theft · Hacking · Cyberstalking · Data Breach · Child Exploitation · Social Media Crime · Financial Fraud · Other

---

## 👨‍💻 Developer

**Gautam Bhardwaj**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gautam-bhardwaj-697619369)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/just-gautam)

---

## 📄 License

This project is for educational purposes only.
