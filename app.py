import os
import mysql.connector
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # This reads your .env file

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

# --- CONFIGURATION FOR FILE UPLOADS ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- MYSQL CONFIGURATION (XAMPP DEFAULT) ---
db_config = {
    'host': os.environ.get("DB_HOST"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'database': os.environ.get("DB_NAME")
}

def get_db_connection():
    """Establishes connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

# 1. DATABASE INITIALIZATION
def init_db():
    try:
        # Step A: Connect to MySQL server (WITHOUT database name) to ensure DB exists
        conn = mysql.connector.connect(
            host=db_config['host'], 
            user=db_config['user'], 
            password=db_config['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        conn.close()

        # Step B: Create the table using the specific database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address TEXT,
                email VARCHAR(255) NOT NULL,
                mobile VARCHAR(20),
                incident_date VARCHAR(50),
                financial_loss VARCHAR(100),
                crime_type VARCHAR(255) NOT NULL,
                description TEXT,
                evidence TEXT,
                date VARCHAR(50),
                reference_id VARCHAR(100) UNIQUE NOT NULL,
                status VARCHAR(50) DEFAULT 'Pending'
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ MySQL Database & Table Initialized.")
    except Exception as e:
        print(f"❌ Initialization Error: {e}")

# 2. HELPER FUNCTIONS
def send_email_notification(receiver_email, ref_id, name):
    msg = EmailMessage()
    msg.set_content(f"Dear {name},\n\nYour cybercrime case has been registered successfully.\nReference ID: {ref_id}\n\nPlease keep this ID for future inquiries.")
    msg['Subject'] = 'Cybercrime Case Registration Successful'

    try:
        EMAIL = os.environ.get("EMAIL_ADDRESS")
        PASSWORD = os.environ.get("EMAIL_PASSWORD")
        msg['From'] = EMAIL
        msg['To'] = receiver_email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Email Error: {e}")
        return False

# 3. ROUTES
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    role = request.form.get("role")
    password = request.form.get("password")
    
    if role == "admin":
        username = request.form.get("username", "").strip().lower()
        if username == os.environ.get("ADMIN_USERNAME") and password == os.environ.get("ADMIN_PASSWORD"):
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        return "Invalid Admin Credentials ❌"
    
    elif role == "user":
        if password == os.environ.get("USER_PASSWORD"):
           session["role"] = "user"
           session["user_name"] = request.form.get("username")
           session["user_email"] = request.form.get("email")
           action = request.form.get("user_action")
           if action == "register":
             return redirect(url_for("user_dashboard"))
           return redirect(url_for("case_tracker"))
        return "Invalid User Password ❌"
    
    return redirect(url_for("login_page"))

@app.route("/tracker")
def case_tracker():
    if session.get("role") != "user": return redirect(url_for("login_page"))
    return render_template("tracker.html")

@app.route("/view_case_user")
def view_case_user():
    if session.get("role") != "user": return redirect(url_for("login_page"))
    ref_id = request.args.get("ref_id")
    name = request.args.get("name")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 

    if ref_id:
        cursor.execute("SELECT * FROM cases WHERE reference_id = %s", (ref_id.strip(),))
    elif name:
        cursor.execute("SELECT * FROM cases WHERE name LIKE %s", ('%' + name.strip() + '%',))
    
    case = cursor.fetchone()
    conn.close()

    if not case:
        return render_template("tracker.html", error="No case found ❌")
    return render_template("tracker.html", case=case)
    
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin": return redirect(url_for("login_page"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cases ORDER BY id DESC")
    cases = cursor.fetchall()
    conn.close()
    return render_template("admin.html", cases=cases)

@app.route("/view_case/<ref_id>")
def view_case(ref_id):
    if session.get("role") != "admin": return redirect(url_for("login_page"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cases WHERE reference_id = %s", (ref_id,))
    case = cursor.fetchone()
    conn.close()
    return render_template("view.html", case=case) if case else ("Not found", 404)

@app.route("/user")
def user_dashboard():
    if session.get("role") != "user": return redirect(url_for("login_page"))
    return render_template("user.html")

@app.route("/register", methods=["POST"])
def register_case():
    if session.get("role") != "user": return redirect(url_for("login_page"))

    incident_date_str = request.form.get("incident_date")
    user_email = request.form.get("email")
    user_name = request.form.get("name")
    ref_id = datetime.now().strftime("%Y%m%d%H%M%S")
    date_filed = datetime.now().strftime("%Y-%m-%d")

    # Handling multiple file uploads
    uploaded_files = request.files.getlist("evidence_image") 
    saved_filenames = []
    for file in uploaded_files:
        if file and file.filename != '':
            unique_name = f"{ref_id}_{file.filename.replace(' ', '_')}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
            saved_filenames.append(unique_name)

    combined_evidence = f"URL: {request.form.get('evidence_url', 'No Link')} | Files: {', '.join(saved_filenames)}"

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO cases (name, address, email, mobile, incident_date, 
               financial_loss, crime_type, description, evidence, date, reference_id, status) 
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = (user_name, request.form.get("address"), user_email, request.form.get("mobile"),
            incident_date_str, request.form.get("financial_loss"), request.form.get("crime_type"),
            request.form.get("description"), combined_evidence, date_filed, ref_id, "Pending")
    
    cursor.execute(query, data)
    conn.commit()
    conn.close()
    
    send_email_notification(user_email, ref_id, user_name)
    
    # Form data dictionary for the report card template
    case_details = {
        'name': user_name, 'address': request.form.get("address"), 'email': user_email,
        'mobile': request.form.get("mobile"), 'incident_date': incident_date_str,
        'financial_loss': request.form.get("financial_loss"), 'crime_type': request.form.get("crime_type"),
        'description': request.form.get("description"), 'evidence': combined_evidence,
        'date': date_filed, 'reference_id': ref_id, 'status': "Pending"
    }
    return render_template("report_card.html", case=case_details)

@app.route("/update_status/<ref_id>", methods=["POST"])
def update_status(ref_id):
    if session.get("role") != "admin": return redirect(url_for("login_page"))
    new_status = request.form.get("status")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET status = %s WHERE reference_id = %s", (new_status, ref_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/delete_case/<ref_id>", methods=["POST"])
def delete_case(ref_id):
    if session.get("role") != "admin": return redirect(url_for("login_page"))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases WHERE reference_id = %s", (ref_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    init_db()
    # Using port 5001 to avoid default MacOS AirPlay port conflicts
    app.run(debug=True, port=5001)