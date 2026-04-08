# 🛡️ Cybercrime Reporting System

A web-based platform built with **Flask** and **MySQL** that allows citizens to report cybercrime incidents online and enables administrators to manage and track cases efficiently.

---

## 📌 Features

### 👤 User Side
- Secure login with role-based access
- Register a cybercrime complaint online
- Upload multiple evidence files (images, videos, documents)
- Receive email confirmation with a unique Reference ID
- Track case status using Reference ID or Name

### 🔐 Admin Side
- View all registered complaints in a dashboard
- Search cases by Name or Reference ID
- Update case status (Pending / In Progress / Resolved)
- View full case details with evidence preview
- Delete cases from the system

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Database | MySQL (via XAMPP) |
| Frontend | HTML, CSS, JavaScript |
| Email | SMTP (Gmail) |
| Security | Python-dotenv for secrets |

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/just-gautam/cybercrime-reporting-system.git
cd cybercrime-reporting-system
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Create a `.env` file
```
SECRET_KEY=your_secret_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password
USER_PASSWORD=your_user_password
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=cybercrime_db
```

### 4. Start XAMPP and run the app
```bash
python3 app.py
```

### 5. Open in browser
```
http://127.0.0.1:5001
```

---

## 🔒 Security Notes
- All sensitive credentials are stored in `.env` (never uploaded to GitHub)
- Passwords are managed via environment variables
- File uploads are stored locally in `static/uploads/`

---

## 📄 License
This project is for educational purposes only.

---

**© 2026 Cybercrime Management System — Digital Integrity Division**
